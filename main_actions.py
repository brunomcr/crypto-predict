from datetime import datetime, UTC
from src.fetch_data import fetch_ohlc
from src.save_data import save_to_json

data = fetch_ohlc()

if data:
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"bitcoin_ohlc_{timestamp}.json"
    save_to_json(data, path="data/bronze", filename=filename)
else:
    print("⚠️ Nenhum dado retornado da API. Arquivo JSON não será criado.")
