import requests


def fetch_ohlc(days=1, currency="usd"):
    """
    Busca dados OHLC (Open, High, Low, Close) do Bitcoin usando a API pública gratuita da CoinGecko.

    Parâmetros:
    :param days: Intervalo em dias. Aceita: 1, 7, 14, 30, 90, 180, 365 ou 'max'.
                 A granularidade é automática:
                 - 1 a 2 dias: 30 minutos
                 - 3 a 30 dias: 4 horas
                 - 31+ dias: 4 dias
    :param currency: Moeda de comparação, como 'usd', 'eur', 'brl', etc.

    Retorno:
    :return: Lista de candles no formato:
             [
                 [timestamp_ms, open, high, low, close],
                 ...
             ]
             Ou None, em caso de erro na requisição.
    """
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
