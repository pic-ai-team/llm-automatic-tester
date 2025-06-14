import os
import requests
from dotenv import load_dotenv
from google.cloud import storage
from typing import BinaryIO, List

load_dotenv()

AI_COMMANDER_ENDPOINT = os.getenv("AI_COMMANDER_ENDPOINT")
GCS_PUBLIC_BUCKET = os.getenv("GCS_PUBLIC_BUCKET")
GCS_DOCS_DIR = os.getenv("GCS_DOCS_DIR")


def check_file_exists(bucket_name: str, file_name: str):
    """
    Check if a file exists in a Google Cloud Storage bucket.

    :param bucket_name: Name of the GCS bucket
    :param file_name: Name of the file to check
    :return: True if the file exists, False otherwise
    """
    try:
        # Initialize a GCS client
        client = storage.Client()

        # Get the bucket
        bucket = client.bucket(bucket_name)

        # Check if the blob (file) exists
        blob = bucket.blob(file_name)
        return blob.exists()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def get_file_url(bucket_name: str, file_name: str):
    """
    Get the public URL of a file in a Google Cloud Storage bucket.

    :param bucket_name: Name of the GCS bucket
    :param file_name: Name of the file
    :return: Public URL of the file
    """
    try:
        # Initialize a GCS client
        client = storage.Client()

        # Get the bucket
        bucket = client.bucket(bucket_name)

        # Get the blob (file)
        blob = bucket.blob(file_name)

        # Generate the public URL
        if blob.exists():
            return f"https://storage.googleapis.com/{bucket_name}/{file_name}"
        print(f"The file '{file_name}' does not exist in the bucket '{bucket_name}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def upload_to_gcs_dir(
    local_file_path: str | BinaryIO,
    file_name: str,
    bucket_name: str = GCS_PUBLIC_BUCKET,
    dir_name: str = GCS_DOCS_DIR,
) -> str:
    # Set up GCS client
    client = storage.Client()

    # Upload file
    gcs_file_path = os.path.join(dir_name, file_name)
    blob = client.bucket(bucket_name).blob(gcs_file_path)

    file_type = file_name.split(".")[-1].lower()
    content_type = (
        f"image/{file_type}"
        if file_type in ["jpg", "jpeg", "png"]
        else "application/octet-stream"
    )

    if isinstance(local_file_path, str):
        blob.upload_from_filename(local_file_path, content_type=content_type)
    # elif isinstance(local_file_path, BinaryIO):
    #     blob.upload_from_file(local_file_path)
    else:  # BinaryIO is not catched. File type was tempfile.SpooledTemporaryFile ¯\_(ツ)_/¯
        blob.upload_from_file(local_file_path, content_type=content_type)

    # Generate public link
    url = blob.public_url
    url = requests.utils.unquote(url)
    return url


def analyze_the_files(folder_path):
    # this function below is used to analyze the files as KM into universal knowledge base

    start_id = 120625999  # Starting ID for km_collection_id and item_id

    files_list = os.listdir(folder_path)
    for i, file_name in enumerate(files_list):
        file_id = start_id + i
        print(file_id, file_name)
        file_url = get_file_url(GCS_PUBLIC_BUCKET, f"{GCS_DOCS_DIR}/{file_name}")
        data = {
            "km_collection_id": file_id,
            "item_id": file_id,
            "file_name": file_name,
            "file_url": file_url,
            "chunk_size": 500,
        }
        url = "http://0.0.0.0:8000/km"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"Successfully sent data for file: {file_name}")
            else:
                print(
                    f"{file_id}: Failed to send data for file: {file_name}, Status Code: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            print(
                f"{file_id}: An error occurred while sending data for file: {file_name}, Error: {e}"
            )
        # Check if the file exists in the GCS bucket


def connect_km_to_bot(bot_id: str, km_collection_ids: List[int]):
    url = f"{AI_COMMANDER_ENDPOINT}/bot_km"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {"bot_id": bot_id, "km_collection_id": km_collection_ids}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Bot connected to KM successfully.")
        return
    print(
        "Failed to connect bot to KM with status code:",
        response.status_code,
        "and message:",
        response.text,
    )


# Example usage
if __name__ == "__main__":
    # start_id = 220509500  # Starting ID for km_collection_id and item_id
    # start_id = 231294800  # Starting ID for km_collection_id and item_id
    start_id = 120625999  # Starting ID for km_collection_id and item_id

    local_datasheet_folder = "pdfs/private"
    analyze_the_files(local_datasheet_folder)
