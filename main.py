from typing import Union
from datetime import datetime
from requests import post
from pydantic import BaseModel
from fastapi import FastAPI, Response

app = FastAPI()

webhook_url = "https://discord.com/api/webhooks/1408476544158142607/ARsHqqq5EJC9YaTLx6EaNataxPlcfD9Bu-dLHgpM6JHwF_bOPpuK7jYoIx-H3EqFcHlN"

class Message(BaseModel):
    type: str
    name: str
    description: str

def send_to_webhook(notification):
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
    response = post(webhook_url, json=payload)
    return response

@app.post("/notify")
def read_root(response: Response, message: Message):
    webhook = send_to_webhook(message)
    response.status_code = webhook.status_code
    if webhook.ok:
        return
    return webhook.json()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}