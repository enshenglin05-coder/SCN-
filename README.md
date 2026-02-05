from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    # 這裡回傳的是 UI 介面，建議加入基本的 Web3 連結按鈕
    return """
    <html>
        <body>
            <h1>🚀 SCN 主節點已啟動</h1>
            <p>狀態：運行中 (KDI Active)</p>
            <button onclick="connectWallet()">連結錢包</button>
            <script>
                async def connectWallet() {
                    if (window.ethereum) {
                        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                        alert('已連結: ' + accounts[0]);
                    }
                }
            </script>
        </body>
    </html>
    """
