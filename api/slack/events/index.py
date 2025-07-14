# api/slack/events/index.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 브라우저에서 확인용
@app.get("/")
async def root():
    return {"message": "Hello from Slack bot!"}

# ① Vercel이 내부적으로 “/” 로 넘겨줄 때 대응
@app.post("/")
# ② 혹시 원본 경로가 그대로 넘어오는 경우도 동시에 대응
@app.post("/api/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # Slack URL 검증
    if data.get("type") == "url_verification":
        return JSONResponse(content={"challenge": data["challenge"]})

    # (나중에 이벤트 처리 로직 추가)
    return JSONResponse(content={"ok": True})
