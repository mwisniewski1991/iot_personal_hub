from minio import Minio
from dotenv import load_dotenv
import os
import io
import json

load_dotenv()

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_PORT = os.getenv('MINIO_PORT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

class MINIO_Client:
    def __init__(self):
        self.minio_client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        
    def get_minio_client(self):
        return self.minio_client
    
    def get_bucket_name(self):
        return self.minio_client.bucket_name

    def _dumped_data(self, data: dict):
        return json.dumps(data).encode('utf-8')
        # return io.BytesIO(json_data)

    def _streamed_data(self, data: dict):
        return io.BytesIO(self._dumped_data(data))

    def _get_device_id(self, data: dict):
        return data['device_id']

    def _get_timestamp(self, data: dict):
        return data['device_timestamp']

    def save_data_to_minio(self, data: dict):
        json_data = self._dumped_data(data)
        json_stream = self._streamed_data(data)

        self.minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=f'mobile/{self._get_device_id(data)}/{self._get_timestamp(data)}.json',
            data=json_stream,
            length=len(json_data),
            content_type='application/json'
        )
        