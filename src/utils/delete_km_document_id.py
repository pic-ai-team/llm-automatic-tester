import os
import requests
from dotenv import load_dotenv

load_dotenv()
AI_COMMANDER_ENDPOINT = os.getenv("AI_COMMANDER_ENDPOINT")


# 1. set the bot config, ex
# start_id = 220509000
start_id = 220509500
# start_id = 231294000
document_ids = [start_id + i for i in range(326)]


def delete_km_document_id(document_ids):
    url = f"{AI_COMMANDER_ENDPOINT}/km"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {"item_id": document_ids}

    response = requests.delete(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Document ID deleted successfully.")
    else:
        print(
            "Failed to delete Document ID  with status code: "
            f"{response.status_code} and message: {response.text}"
        )


delete_km_document_id(document_ids)
