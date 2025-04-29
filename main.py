from datetime import datetime
from dotenv import load_dotenv
import os

from src.fetch_data import fetch_ohlc
from src.save_data import save_to_parquet
from src.github_artifact_handler import download_all_artifacts
from src.zip_data_handler import ZipDataHandler
from src.load_data import load_json_from_bronze, load_silver_data
from src.transform_data import transform_to_dataframe
from src.enrich_data import enrich_with_indicators
from src.feature_engineering import add_basic_features
from src.prepare_target import prepare_target

# 💼 Constantes
SILVER_DIR = "data/silver"
SILVER_FILENAME = "bitcoin_ohlc_silver.parquet"
SILVER_PATH = os.path.join(SILVER_DIR, SILVER_FILENAME)

GOLD_DIR = "data/gold"
GOLD_FILENAME = "bitcoin_ohlc_gold.parquet"

# 🔐 Carrega .env
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
repo = "brunomcr/crypto-predict"

# ⬇️ Baixa artefatos
print("⬇️ Baixando artefatos do GitHub...")
download_all_artifacts(repo=repo, token=token)

# 📆 Extrai artefatos e move .json para bronze
print("📆 Processando arquivos ZIP...")
handler = ZipDataHandler(
    downloads_dir="downloads",
    target_dir="data/bronze",
    tmp_dir="tmp_extract"
)
handler.process_all()

# 🔄 Bronze → Silver
print("🔄 Transformando camada Bronze para Silver...")
raw_data = load_json_from_bronze()

if not raw_data:
    print("⚠️ Nenhum dado encontrado na camada bronze.")
else:
    df_silver = transform_to_dataframe(raw_data)
    save_to_parquet(df_silver, path=SILVER_DIR, filename=SILVER_FILENAME)
    print(f"✅ Silver salvo em: {SILVER_PATH}")

    # 💰 Silver → Gold
    print("🦰 Gerando camada GOLD com indicadores técnicos e features...")
    try:
        df_silver = load_silver_data()  # Ou reutilize df_silver diretamente
        df_gold = enrich_with_indicators(df_silver)
        df_gold = add_basic_features(df_gold)  # ✅ Feature Engineering adicional
        df_gold = prepare_target(df_gold)  # ✅ Preparação do Target
        save_to_parquet(df_gold, path=GOLD_DIR, filename=GOLD_FILENAME)
        print(f"✅ Camada GOLD salva em: {os.path.join(GOLD_DIR, GOLD_FILENAME)}")
    except Exception as e:
        print(f"❌ Erro ao gerar camada GOLD: {e}")
