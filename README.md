from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# ------------------
# 首頁
# ------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>🚀 SCN 主節點已啟動</h1>
    <h2>狀態：運行中 (KDI Active)</h2>
    """

# ------------------
# 心跳
# ------------------
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}

# ------------------
# 封包格式
# ------------------
class Packet(BaseModel):
    wallet: str
    data: str

# ------------------
# 封包驗證
# ------------------
@app.post("/verify")
async def verify(packet: Packet):
    return {
        "result": "success",
        "wallet": packet.wallet
    }
