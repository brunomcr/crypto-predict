import requests


def fetch_ohlc(days=1, currency="usd"):

    url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"
    params = {
        "vs_currency": currency,
        "days": days
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"❌ Erro ao buscar dados OHLC: {e}")
        return None
