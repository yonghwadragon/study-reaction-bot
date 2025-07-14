# api/slack/events.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # URL 검증 (Slack Event Subscription 초기 인증)
    if data.get("type") == "url_verification":
        challenge = data.get("challenge")
        return JSONResponse(content={"challenge": challenge})

    # 이후 Slack event 처리 영역
    return JSONResponse(content={})
