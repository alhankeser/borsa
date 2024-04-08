import os
from datetime import datetime, timedelta
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

BUCKET_NAME = os.getenv("GOOGLE_BUCKET_NAME")
PROJECT_NAME = os.getenv("GOOGLE_PROJECT_NAME")

def get_minute(on_date=None, minutes_ago=0):
    now = datetime.now()
    if not on_date:
        return now.strftime("%Y-%m-%dT%H:%M:00Z")
    else:
        current_time = now.strftime("%H:%M")
        on_date_datetime = datetime.strptime(on_date, "%Y-%m-%dT%H:%M:%SZ")
        combined_datetime = datetime.combine(on_date_datetime, datetime.strptime(current_time, "%H:%M").time())
        return combined_datetime.strftime("%Y-%m-%dT%H:%M:00Z")
    
def get_day(days_ago=0):
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT00:00:00Z")

def as_datetime(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

def upload_to_cloud(source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME, user_project=PROJECT_NAME)
    blob = bucket.blob(f"{destination_blob_name}.parquet")
    blob.upload_from_filename(source_file_name)
