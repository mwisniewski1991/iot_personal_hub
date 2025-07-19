from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('device1_apikey')

# Konfiguracja loggingu
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO').upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
            logger.error(f"Nieprawidłowy klucz API: {api_key}")
            return jsonify({"error": "Nieprawidłowy klucz API"}), 401
        
        data = request.get_json()
        logger.info(f"Otrzymano dane: {data}")
        return jsonify({"message": "Lokalizacja odbierana"})

    except Exception as e:
        logger.error(f"Błąd: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)