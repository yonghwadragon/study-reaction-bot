# api/slack/events/index.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
print("SLACK_BOT_TOKEN loaded:", bool(SLACK_BOT_TOKEN))

@app.get("/")
async def root():
    return {"message": "Hello from Slack bot!"}

@app.post("/")
@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    print("== SLACK EVENT RECEIVED ==")
    print(data)

    if data.get("type") == "url_verification":
        return JSONResponse(content={"challenge": data["challenge"]})

    if data.get("type") == "event_callback":
        event = data.get("event", {})
        print("== SLACK EVENT DATA ==")
        print(event)

        channel = event.get("channel")
        ts = event.get("ts")
        subtype = event.get("subtype")

        if subtype == "bot_message":
            return JSONResponse(content={"ok": True})

        if channel and ts:
            headers = {
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }

            payload1 = {
                "channel": channel,
                "timestamp": ts,
                "name": "white_check_mark"
            }

            payload2 = {
                "channel": channel,
                "timestamp": ts,
                "name": "+1"
            }

            async with httpx.AsyncClient() as client:
                res1 = await client.post(
                    "https://slack.com/api/reactions.add",
                    headers=headers,
                    json=payload1
                )
                print("Reaction 1 Response:", res1.json())

                res2 = await client.post(
                    "https://slack.com/api/reactions.add",
                    headers=headers,
                    json=payload2
                )
                print("Reaction 2 Response:", res2.json())

        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True})
