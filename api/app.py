from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)

@app.route('/')
def home():
    """Strona główna z informacjami o API"""
    return jsonify({
        "message": "API do odbierania lokalizacji urządzeń mobilnych",
        "endpoint": "/mobile_location",
        "method": "POST",
        "description": "Wysyłaj dane lokalizacji w formacie JSON"
    })

@app.route('/mobile_location', methods=['POST'])
def mobile_location():
    """Odbieranie lokalizacji urządzenia mobilnego"""
    try:
        api_key = request.headers.get('X-API-Key')
        if api_key != API_KEY:
            return jsonify({"error": "Nieprawidłowy klucz API"}), 401
        
        data = request.get_json()
        print(data)
        return jsonify({"message": "Lokalizacja odbierana"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)