import requests
from typing import Dict, List

# URLs
BINANCE_API = "https://api.binance.com/api/v3"
COINGECKO_API = "https://api.coingecko.com/api/v3"


def obtener_precio_actual(par) -> Dict:
    """Devuelve el precio actual de un par (ej: BTCUSDT)."""
    try:
        url = f"{BINANCE_API}/ticker/price"
        respuesta = requests.get(url, params={"symbol": par})
        respuesta.raise_for_status()
        return respuesta.json()
    except Exception as e:
        print("Error al obtener precio actual:", e)
        return {}


def obtener_precios_24h() -> List:
    """Devuelve los precios y cambios de las últimas 24h para todos los pares."""
    try:
        url = f"{BINANCE_API}/ticker/24hr"
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()
    except Exception as e:
        print("Error al obtener precios de 24h:", e)
        return []


def obtener_velas_ohlc(par, intervalo="1h", limite=100) -> List:
    """Devuelve datos OHLC (velas) para un par específico."""
    try:
        url = f"{BINANCE_API}/klines"
        params = {"symbol": par, "interval": intervalo, "limit": limite}
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()
        return respuesta.json()
    except Exception as e:
        print("Error al obtener velas:", e)
        return []


def obtener_info_cripto_coingecko() -> Dict:
    """Consulta del Market Cap desde CoinGecko."""
    try:
        url = f"{COINGECKO_API}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False,
        }
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()
        datos = respuesta.json()

        resultado = {}
        for cripto in datos:
            simbolo = cripto["symbol"].upper()
            resultado[simbolo] = {
                "nombre": cripto["name"],
                "cap_mercado": cripto["market_cap"],
                "suministro_circulante": cripto["circulating_supply"],
            }
        # print(resultado)
        return resultado
    except Exception as e:
        print("Error al obtener datos de CoinGecko:", e)
        return {}