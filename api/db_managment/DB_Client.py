import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


class DB_Client:
    def __init__(self):
        self.db_client = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

    def get_db_client(self):    
        return self.db_client
    
    def close_db_client(self):
        self.db_client.close()

    def get_cursor(self):
        return self.db_client.cursor()
    
    def close_cursor(self, cursor):
        cursor.close()
        
    def save_data_to_db(self, data: dict):  
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO device_locations_test (device_id, latitude, longitude, timestamp_unix) VALUES (%s, %s, %s, %s)", (data['device_id'], data['latitude'], data['longitude'], data['timestamp_unix']))
        self.db_client.commit()
        self.close_cursor(cursor)
