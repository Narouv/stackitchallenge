from typing import Union
from datetime import datetime
from requests import post
from pydantic import BaseModel
from fastapi import FastAPI, Response, Query
from collections import deque
import util

app = FastAPI()

webhook_url = util.getEnv("WEBHOOK_URL")
forwarded_types = ["warning", "critical"]
saved_types = ["info", "fortnite"]

message_storage = deque()

class Message(BaseModel):
    type: str
    name: str
    description: str

class Color:
    Yellow = 0x00FFFF00
    Red = 0xFF000000
    Blue = 0x00FF0000
    Green = 0x0000FF00

class SavedMessage():
    def __init__(self, message: Message):
        self.id = id(self)
        self.message = message
        self.timestamp = datetime.now()

def construct_embed(message: Message) -> dict:
    return {
        "title": message.name,
        "description": message.description,
        "color": Color.Yellow,
        "fields": [
            {
                "name": "Type",
                "value": message.type,
                "inline": True
            },
            {
                "name": "Timestamp", 
                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "inline": True
            }
        ],
    }

def handle_additional_message(index: int):
    if index > message_storage.count():
        return None
    

def construct_payload(notification: Message, additional: int) -> dict:
    base_payload = {
        "content": f"**{notification.name}**\n{notification.description}\n\n**Type:** {notification.type}\n**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    if message_storage.count():
        base_payload["embeds"] = [handle_additional_message(i) for i in range(additional)]
    return base_payload

def send_to_webhook(notification: Message, additional: int = 0):
    if not webhook_url:
        return None
    payload = construct_payload(notification, additional)
    try:
        response = post(webhook_url, json=payload, timeout=10)
        return response
    except Exception as e:
        print(f"Exception: {e}")
        return None

def save_message(message: Message):
    msg = SavedMessage(message)
    if message_storage.count() > 10:
        message_storage.pop()
    message_storage.appendleft(msg)
    print(f"Stored message {msg.message.name}. Current backlog {message_storage.count()}")

@app.post("/notify")
def notify(response: Response, notification: Message, send_saved: int = Query(0, description="Number of saved messages to send along")):
    print("REQUEST INCOMING")
    if notification.type.lower() in forwarded_types:
        webhook_response = send_to_webhook(notification, send_saved)
        if webhook_response and webhook_response.ok:
            return {"status": "success", "message": "Notification forwarded to Discord"}
        else:
            response.status_code = webhook_response.status_code
            return {"status": "failed", "message": "Failed to send to Discord"}
    elif notification.type.lower() in saved_types:
        save_message(notification)
        return {"status": "filtered", "message": f"{notification.type} notifications are not forwarded"}
    else:
        return {"status": "ignored", "message": f"{notification.type} notifications are not known"}

@app.delete("/clear")
def clear_messages():
    count = len(message_storage)
    message_storage.clear()
    return {"status": "success", "message": f"cleared all {count} messages from backlog"}