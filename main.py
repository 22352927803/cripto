from fastapi import FastAPI
import httpx
import time
import hmac
import hashlib
import os
from fastapi.middleware.cors import CORSMiddleware

# Defina suas credenciais da Binance em variáveis de ambiente
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

app = FastAPI()

# Permitir frontend acessar esta API (importante para testes locais)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/endereco-btc")
async def obter_endereco_btc():
    if not API_KEY or not API_SECRET:
        return {"erro": "Credenciais Binance não configuradas."}

    coin = "BTC"
    timestamp = int(time.time() * 1000)
    query_string = f"coin={coin}&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    url = f"https://api.binance.com/sapi/v1/capital/deposit/address?{query_string}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {"endereco": data.get("address")}
        else:
            return {"erro": "Erro ao consultar Binance", "detalhes": response.text}
