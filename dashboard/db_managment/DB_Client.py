import psycopg2
from dotenv import load_dotenv
import os
import json 

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE = os.getenv('DB_TABLE')
DB_SCHEMA = os.getenv('DB_SCHEMA')

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
        cursor.execute(f'INSERT INTO {DB_TABLE} (device_id, device_timestamp, properties) VALUES (%s, %s, %s)', (data['device_id'], data['device_timestamp'], json.dumps(data['properties'])))
        self.db_client.commit()
        self.close_cursor(cursor)

    def get_data_from_db(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_events_counter')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data
    
    def get_devices_locations(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_locations')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data

    def get_devices_battery_level(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_battery_level')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data

    def get_devices_battery_temperature(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_battery_temperature')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data

    def get_devices_battery_usage_current_mA(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_battery_usage_current_mA')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data

    def get_devices_battery_usage_current_average_mA(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_battery_usage_current_average_mA')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data

    def get_devices_location_altitude_m(self):
        cursor = self.get_cursor()
        cursor.execute(f'SELECT * FROM {DB_SCHEMA}.devices_location_altitude_m')
        data = cursor.fetchall()
        self.close_cursor(cursor)
        return data