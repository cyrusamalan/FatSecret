from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests
import base64

app = Flask(__name__)
CORS(app)  # ✅ This enables CORS for all origins

CLIENT_ID = 'd1dc16bc0ff248d996719575cabf705c'
CLIENT_SECRET = 'c42e2819e65a4cae9014b0e9d05477e5'

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
            'search_expression': query,
            'format': 'json'
        }
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(search_url, headers=headers, params=params)
        return jsonify(response.json())

    except Exception as e:
        print("🔥 Error in /search route:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
