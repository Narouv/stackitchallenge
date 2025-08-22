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

def construct_payload(notification: Message, additional: int) -> dict:
    base_payload = {
        "content": f"**{notification.name}**\n{notification.description}\n\n**Type:** {notification.type}\n**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    send = get_and_remove_last_n_messages(additional)
    if len(send) > 0:
        base_payload['embeds'] = [construct_embed(entry.message) for entry in send]
    return base_payload

def get_and_remove_last_n_messages(n: int):
    if n < 1 or len(message_storage) == 0:
        return []
    messages_to_send = []

    for i in range(n):
        if len(message_storage):
            messages_to_send.append(message_storage.pop())

    print(f"Retrieved {len(messages_to_send)} messages, {len(message_storage)} remaining in storage")
    return messages_to_send

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
    if len(message_storage) > 10:
        message_storage.pop()
    message_storage.appendleft(msg)
    print(f"Stored message {msg.message.name}. Current backlog {len(message_storage)}")

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