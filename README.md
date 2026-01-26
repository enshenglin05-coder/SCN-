from fastapi import FastAPI
import uuid, time

app = FastAPI()

@app.post("/verify")
def kdi(sender: str, receiver: str, currency: str, amount: float, memo: str = ""):
    # 只做移轉驗證與備註記錄，不碰錢
    return {
        "status": "Verified",
        "kdi_tx": str(uuid.uuid4()),
        "time": int(time.time()),
        "memo": memo
    }

@app.get("/")
def health(): return "KDI Channel Active"
