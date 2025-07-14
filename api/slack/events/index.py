# api/slack/events/index.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

@app.get("/")
async def root():
    return {"message": "Hello from Slack bot!"}

@app.post("/")
@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # Slack URL verification
    if data.get("type") == "url_verification":
        return JSONResponse(content={"challenge": data["challenge"]})

    # Event Callback
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        channel = event.get("channel")
        ts = event.get("ts")
        subtype = event.get("subtype")

        # Bot이 쓴 메시지는 무시
        if subtype == "bot_message":
            return JSONResponse(content={"ok": True})

        # message.channels 이벤트일 때 reaction 추가
        if channel and ts:
            headers = {
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }

            # ✅ white_check_mark 추가
            payload1 = {
                "channel": channel,
                "timestamp": ts,
                "name": "white_check_mark"
            }

            # 👍 추가
            payload2 = {
                "channel": channel,
                "timestamp": ts,
                "name": "+1"
            }

            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://slack.com/api/reactions.add",
                    headers=headers,
                    json=payload1
                )
                await client.post(
                    "https://slack.com/api/reactions.add",
                    headers=headers,
                    json=payload2
                )

        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True})
