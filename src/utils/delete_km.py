import os
import requests
from typing import List
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv(override=True)

AI_COMMANDER_ENDPOINT = os.getenv("AI_COMMANDER_ENDPOINT")
GCS_PUBLIC_BUCKET = os.getenv("GCS_PUBLIC_BUCKET")
GCS_DOCS_DIR = os.getenv("GCS_DOCS_DIR")


def delete_km_document_id(document_ids: List[int]):
    url = f"{AI_COMMANDER_ENDPOINT}/km"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {"item_id": document_ids}

    response = requests.delete(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Document ID deleted successfully.")
        return
    print(
        "Failed to delete Document ID  with status code: "
        f"{response.status_code} and message: {response.text}"
    )


def delete_gcs_file(bucket_name: str, file_name: str):
    """
    Deletes a file from a GCS bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        file_name (str): Name of the file to delete in the bucket.
    """
    try:
        # Initialize the GCS client
        client = storage.Client()

        # Get the bucket
        bucket = client.bucket(bucket_name)

        # Get the blob (file) to delete
        blob = bucket.blob(file_name)

        # Delete the blob
        blob.delete()

        print(f"File '{file_name}' deleted successfully from bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Failed to delete file '{file_name}' from bucket '{bucket_name}': {e}")


# Example usage
if __name__ == "__main__":
    # delete_km_document_id(document_ids)
    delete_gcs_file(GCS_PUBLIC_BUCKET, f"{GCS_DOCS_DIR}/ADAM-5056S_DS.pdf")
