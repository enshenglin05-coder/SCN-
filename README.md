import uuid
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# 1. 定義接收資料的格式
class KDIRequest(BaseModel):
    sender: str
    receiver: str
    currency: str
    amount: float
    memo: str = ""

# 2. 這是首頁：讓你的 App 打開不再是空的，而是顯示 UI
@app.get("/", response_class=HTMLResponse)
def get_ui():
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCN 通道 - Web3 隱私移轉</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background-color: #0d1117; }
            .glass { background: rgba(23, 23, 23, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
        </style>
    </head>
    <body class="text-gray-200 min-h-screen flex items-center justify-center p-4">
        <div class="glass w-full max-w-md rounded-3xl p-8 shadow-2xl">
            <div class="text-center mb-8">
                <h1 class="text-3xl font-extrabold text-blue-500 tracking-tighter">SCN CHANNEL</h1>
                <p class="text-xs text-gray-500 mt-1">軍工級保密通道 | 零損耗移轉驗證</p>
            </div>
            <div class="mb-6 bg-black/40 p-4 rounded-2xl border border-blue-900/30">
                <label class="text-[10px] uppercase tracking-widest text-blue-400 font-bold">我的錢包地址</label>
                <p class="text-[11px] font-mono break-all text-gray-400">0x71C7656EC7ab88b098defB751B7401B5f6d8976F</p>
                <div class="mt-3 flex justify-between items-center">
                    <span class="text-sm text-gray-500">美元穩定幣餘額</span>
                    <span class="text-xl font-bold text-green-500">100.00 <span class="text-xs">USD</span></span>
                </div>
            </div>
            <div class="space-y-5">
                <input id="receiver" type="text" class="w-full bg-gray-800/50 border border-gray-700 p-4 rounded-xl text-sm font-mono" placeholder="接收者地址">
                <input id="amount" type="number" class="w-full bg-gray-800/50 border border-gray-700 p-4 rounded-xl text-sm font-bold" value="0">
                <textarea id="memo" rows="3" class="w-full bg-gray-800/50 border border-gray-700 p-4 rounded-xl text-sm" placeholder="輸入保密訊息..."></textarea>
                <button onclick="executeKDI()" id="btn" class="w-full bg-blue-600 hover:bg-blue-500 text-white py-4 rounded-2xl font-bold text-lg transition-all active:scale-95 shadow-lg shadow-blue-900/20">啟動多雲交岔驗證</button>
            </div>
            <div id="result" class="mt-6 hidden">
                <div class="bg-blue-900/20 border border-blue-500/50 p-4 rounded-2xl">
                    <p class="text-blue-400 text-xs font-bold">✓ 多雲驗證足跡已生成</p>
                    <p class="text-[10px] font-mono text-gray-400 mt-2 break-all" id="txid"></p>
                </div>
            </div>
            <div class="mt-12 text-center text-[10px] text-gray-700 uppercase tracking-widest">
                Sponsored by Global Cloud Nodes
            </div>
        </div>
        <script>
            async function executeKDI() {
                const btn = document.getElementById('btn');
                const api_url = "/verify"; // 因為在同一個網址，直接寫路徑即可
                const payload = {
                    sender: "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
                    receiver: document.getElementById('receiver').value,
                    currency: "SCN",
                    amount: parseFloat(document.getElementById('amount').value),
                    memo: document.getElementById('memo').value
                };
                btn.innerText = "驗證中...";
                try {
                    const response = await fetch(api_url, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    const data = await response.json();
                    document.getElementById('txid').innerText = "KDI-TX: " + data.kdi_tx;
                    document.getElementById('result').classList.remove('hidden');
                    btn.innerText = "驗證完成";
                } catch (e) {
                    alert("連線失敗");
                    btn.innerText = "重試";
                }
            }
        </script>
    </body>
    </html>
    """

# 3. 這是後台：處理數據移轉驗證
@app.post("/verify")
def kdi_verify(req: KDIRequest):
    return {
        "status": "success",
        "kdi_tx": str(uuid.uuid4()),
        "verified_at": int(time.time())
    }
