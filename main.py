from datetime import datetime, UTC
from src.fetch_data import fetch_ohlc
from src.save_data import save_to_json
from src.github_artifact_handler import download_all_artifacts
from dotenv import load_dotenv
import os

# Carrega o .env na raiz do projeto
load_dotenv()


# data = fetch_ohlc()
#
# if data:
#     timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
#     filename = f"bitcoin_ohlc_{timestamp}.json"
#     save_to_json(data, path="data/bronze", filename=filename)
# else:
#     print("⚠️ Nenhum dado retornado da API. Arquivo JSON não será criado.")


repo = "brunomcr/crypto-predict"
token = os.getenv("GITHUB_TOKEN")

download_all_artifacts(repo=repo, token=token)