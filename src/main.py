from typing import Union
from datetime import datetime
from requests import post
from pydantic import BaseModel
from fastapi import FastAPI, Response
import util

app = FastAPI()

webhook_url = util.getEnv("WEBHOOK_URL")

class Message(BaseModel):
    type: str
    name: str
    description: str

def send_to_webhook(notification):
    if not webhook_url:
        return None
    payload = {
        "embeds": [{
            "title": notification.name,
            "description": notification.description,
            "color": 0x00FFFF00,
            "fields": [
                {
                    "name": "Type",
                    "value": notification.type,
                    "inline": True
                },
                {
                    "name": "Timestamp", 
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": True
                }
            ],
        }]
    }
    try:
        response = post(webhook_url, json=payload, timeout=10)
        return response
    except Exception as e:
        return None

@app.post("/notify")
def read_root(response: Response, message: Message):
    print("REQUEST INCOMING")
    if message.type.lower() == "warning":
        webhook_response = send_to_webhook(message)
        
        if webhook_response and webhook_response.ok:
            return {"status": "sent", "message": "Notification forwarded to Discord"}
        else:
            return {"status": "webhook_failed", "message": "Failed to send to Discord"}
    else:
        return {"status": "filtered", "message": f"{message.type} notifications are not forwarded"}
