from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import logging
from hashlib import sha256
from db_managment.DB_Client import DB_Client
from minio_managment.MINIO_Client import MINIO_Client

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

def save_data_to_db(data: dict):
    db_client = DB_Client()
    db_client.save_data_to_db(data)
    db_client.close_db_client()

def save_data_to_minio(data: dict):
    minio_client = MINIO_Client()
    minio_client.save_data_to_minio(data)

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
        if sha256(api_key.encode()).hexdigest() != API_KEY:
            logger.error(f"Nieprawidłowy klucz API: {api_key}")
            return jsonify({"error": "Nieprawidłowy klucz API"}), 401
        
        data = request.get_json()
        logger.info(f"Otrzymano dane: {data}")
        
        try:
            save_data_to_db(data)
        except Exception as e:
            logger.error(f"Błąd zapisu do bazy danych: {str(e)}")
        
        try:
            save_data_to_minio(data)
        except Exception as e:
            logger.error(f"Błąd zapisu do MinIO: {str(e)}")
        
        return jsonify({"message": "Lokalizacja odbierana"})

    except Exception as e:
        logger.error(f"Błąd: {str(e)}")
        return jsonify({"error": str(e)}), 400
