from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests
import base64

app = Flask(__name__)
CORS(app)  # ✅ This enables CORS for all origins

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_access_token():
    url = 'https://oauth.fatsecret.com/connect/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'basic'
    }

    response = requests.post(url, headers=headers, data=data)
    print("🔐 OAuth response:", response.status_code, response.text)

    return response.json()['access_token']

@app.route('/')
def index():
    return render_template('script.html')  # must be in templates/script.html

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query')
        access_token = get_access_token()

        search_url = 'https://platform.fatsecret.com/rest/server.api'
        params = {
            'method': 'foods.search',
            'search_expression': query.strip().lower(),
            'format': 'json'
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(search_url, headers=headers, params=params)
        print("🔍 FatSecret response:", response.text)  # ← add this
        return jsonify(response.json())

    except Exception as e:
        print("🔥 Error in /search route:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/food_details', methods=['POST'])
def food_details():
    try:
        food_id = request.json.get('food_id')
        access_token = get_access_token()

        response = requests.get(
            'https://platform.fatsecret.com/rest/server.api',
            headers={'Authorization': f'Bearer {access_token}'},
            params={
                'method': 'food.get',
                'food_id': food_id,
                'format': 'json'
            }
        )

        print("🍽️ Food details response:", response.text)  # Log to confirm
        return jsonify(response.json())
    except Exception as e:
        print("🔥 Error in /food_details:", e)
        return jsonify({'error': str(e)}), 500




@app.route("/")
def home():
    return "Hello, production!"

# Note: no app.run() here! Gunicorn will handle that in production.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
