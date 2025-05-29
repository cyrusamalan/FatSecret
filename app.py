from flask import Flask, render_template, request, jsonify
import requests
import base64
from flask_cors import CORS
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('script.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets this PORT
    app.run(host='0.0.0.0', port=port)

CORS(app)  # ✅ allows cross-origin requests

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

    return response.json()['access_token']  # this is where the error is





@app.route('/search', methods=['POST'])
def search():
    try:
        print("📥 Incoming JSON:", request.json)
        query = request.json.get('query')
        print("🔍 Search query:", query)

        access_token = get_access_token()
        print("🔑 Access token:", access_token[:10] + "...")

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
        print("📦 FatSecret API status code:", response.status_code)
        print("📦 FatSecret API response:", response.text)

        return jsonify(response.json())
    except Exception as e:
        print("🔥 Error in /search route:", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

