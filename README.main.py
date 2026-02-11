from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# -------------------------
# UI 首頁
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>🚀 SCN 主節點已啟動</h1>
    <h2>狀態：運行中 (KDI Active)</h2>
    """

# -------------------------
# 心跳 API
# -------------------------
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}

# -------------------------
# 封包驗證模型
# -------------------------
class Packet(BaseModel):
    wallet: str
    data: str

# -------------------------
# 封包驗證 API
# -------------------------
@app.post("/verify")
async def verify(packet: Packet):
    # 這裡之後可加入 KDI 驗證邏輯
    return {
        "result": "success",
        "wallet": packet.wallet
    }
