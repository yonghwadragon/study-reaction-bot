# api/slack/events.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    if data.get("type") == "url_verification":
        return JSONResponse(content={"challenge": data.get("challenge")})
    # 나중에 event 처리 로직 추가
    return JSONResponse(content={})
