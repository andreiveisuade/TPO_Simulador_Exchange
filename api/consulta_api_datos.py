import requests

URL_BASE = "https://api.binance.com"


def obtener_precios_24h():
    """
    Consulta todos los pares de criptomonedas y sus datos de las últimas 24h.
    """
    url = f"{URL_BASE}/api/v3/ticker/24hr"
    respuesta = requests.get(url)
    return respuesta.json()


def obtener_precio_actual(par):
    """
    Consulta el precio actual de un par específico.
    Ejemplo de 'par': 'BTCUSDT', 'ETHUSDT', etc.
    """
    url = f"{URL_BASE}/api/v3/ticker/price"
    parametros = {"symbol": par}
    respuesta = requests.get(url, params=parametros)
    return respuesta.json()


def obtener_velas_ohlc(par, intervalo="1h", limite=100):
    """
    Consulta las velas OHLC de un par en un intervalo determinado.
    Ejemplo de 'intervalo': '1m', '5m', '1h', '1d', etc.
    """
    url = f"{URL_BASE}/api/v3/klines"
    parametros = {"symbol": par, "interval": intervalo, "limit": limite}
    respuesta = requests.get(url, params=parametros)
    return respuesta.json()
