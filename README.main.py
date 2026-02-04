import uuid
import time
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ======================
# FastAPI App
# ======================
app = FastAPI(title="SCN Main Node")

# ======================
# 前端靜態檔案
# frontend/
# └─ index.html
# ======================
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(
            "<h1>❌ 找不到 frontend/index.html</h1>"
            "<p>請確認你有上傳前端資料夾</p>"
        )

# ======================
# KDI Request 資料結構
# ======================
class KDIRequest(BaseModel):
    sender: str
    receiver: str
    currency: str = "SCN"
    amount: float = 0
    memo: str = ""

# ======================
# API：驗證交易
# ======================
@app.post("/verify")
def verify(req: KDIRequest):
    return JSONResponse({
        "status": "success",
        "kdi_tx": str(uuid.uuid4()),
        "verified_at": int(time.time()),
        "sender": req.sender,
        "receiver": req.receiver,
        "amount": req.amount,
    })

# ======================
# WebSocket：輕節點心跳
# ======================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/light")
async def websocket_light(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"💓 心跳：{data}")
            await websocket.send_json({
                "status": "ok",
                "ts": int(time.time())
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("❌ 輕節點斷線")

# ======================
# 前端提示頁
# ======================
@app.get("/generator", response_class=HTMLResponse)
def generator_hint():
    return """
    <h1>SCN 前端 UI 說明</h1>
    <p>請將以下檔案放入 frontend/ 資料夾：</p>
    <ul>
      <li>index.html</li>
      <li>app.js（可選）</li>
      <li>manifest.json（可選）</li>
    </ul>
    <p>完成後，直接開啟主網址即可看到 UI。</p>
    """
