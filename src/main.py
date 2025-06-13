import uvicorn
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI, HTTPException

load_dotenv()
AI_COMMANDER_ENDPOINT = os.getenv("AI_COMMANDER_ENDPOINT")
COMMON_BOT_ENDPOINT = os.getenv("COMMON_BOT_ENDPOINT")

USER_ID = "albert"
BOT_ID = "bot-23"
TRIES = 1


def send_question_answer():
    url = f"{COMMON_BOT_ENDPOINT}/{BOT_ID}/qa"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    # 3. for every_question in list of questions:
    for i in range(TRIES):
        # 1. generate a new new conversation id: every question will need a new conversation id
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        print("date and time:", date_time)
        payload = {
            "user_id": USER_ID,
            "company_id": USER_ID,
            "conversation_id": f"{USER_ID}_{USER_ID}_{BOT_ID}_{date_time}",
            "question": "hi",
            "event": "string",
            "uri": "",
            "uris": [],
            "language": "2",
            "prompt": "",
            "history": [],
            "stream": False,
        }
        # 2. send the request
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print(
                "Failed with status code:",
                response.status_code,
                "and message:",
                response.text,
            )
        # 3. check the answer with the ground truth - using text embedding similarity metric
        # 4. go to step no. a
        # 5. go to step no. 2


def connect_km_to_bot(km_collection_ids):
    url = f"{AI_COMMANDER_ENDPOINT}/bot_km"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {"bot_id": "bot-23", "km_collection_id": km_collection_ids}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Bot connected to KM successfully.")
    else:
        print(
            "Failed to connect bot to KM with status code:",
            response.status_code,
            "and message:",
            response.text,
        )


def disconnect_km_from_bot(km_collection_ids):
    url = f"{AI_COMMANDER_ENDPOINT}/bot_km"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    for km_collection_id in km_collection_ids:
        payload = {"bot_id": "bot-23", "km_collection_id": km_collection_id}
        response = requests.delete(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Bot disconnected from KM successfully.")
        else:
            print(
                "Failed to disconnect bot from KM with status code:",
                response.status_code,
                "and message:",
                response.text,
            )


# testing script algorithm:
# 1. set the bot config, ex
# start_id = 220509000 # 326
# start_id = 220509500  # 326
# start_id = 231294800  # 1
# start_id = 231294000 # 69
# start_id = 231294500  # 69
start_id = 120625999  # 1

# document_ids = [start_id + i for i in range(1)]
# connect_km_to_bot(document_ids)  # 2. connect the bot to the KM
# # send_question_answer()
# # disconnect_km_from_bot(document_ids)  # 4. disconnect the bot with the KM


app = FastAPI()


@app.post("/connect_km_to_bot/")
async def api_connect_km_to_bot(km_collection_ids: list[int]):
    try:
        connect_km_to_bot(km_collection_ids)
        return {"message": "Bot connected to KM successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/disconnect_km_from_bot/")
async def api_disconnect_km_from_bot(km_collection_ids: list[int]):
    try:
        disconnect_km_from_bot(km_collection_ids)
        return {"message": "Bot disconnected from KM successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send_question_answer/")
async def api_send_question_answer():
    try:
        send_question_answer()
        return {"message": "Question sent and answer received successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2020)
