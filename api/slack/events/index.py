# api/slack/events/index.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Slack bot!"}

@app.post("/")
async def slack_events(request: Request):
    data = await request.json()

    # Slack URL verification
    if data.get("type") == "url_verification":
        challenge = data.get("challenge")
        return JSONResponse(content={"challenge": challenge})

    # 여기에 이후 메시지 이벤트 처리 추가 예정
    return JSONResponse(content={"ok": True})
