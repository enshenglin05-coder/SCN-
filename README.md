import uuid
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# 1. 定義接收資料的格式from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import time
from typing import List

app = FastAPI()

# ======================
# 前端靜態檔案
# ======================
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>前端檔案不存在，請上傳 frontend/index.html</h1>")

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
# API: 驗證訊息
# ======================
@app.post("/verify")
def verify(req: KDIRequest):
    # 回傳驗證結果
    return JSONResponse({
        "status": "success",
        "kdi_tx": str(uuid.uuid4()),
        "verified_at": int(time.time())
    })

# ======================
# WebSocket: 心跳
# ======================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/light")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # 這裡可以紀錄心跳資訊或節點狀態
            print(f"心跳來自 {data.get('node_id')} at {data.get('ts')}")
            await websocket.send_json({"status": "ok", "ts": int(time.time())})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("輕節點斷線")

# ======================
# 範例前端生成器提示
# ======================
@app.get("/generator", response_class=HTMLResponse)
def generator_hint():
    return """
    <h1>請將 frontend/ 目錄上傳到雲端主節點</h1>
    <p>index.html + app.js + manifest.json 放在 frontend/，即可透過 / 路徑訪問前端 UI。</p>
    """
