import requests

# Base URL para la API de Binance
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


# Función para obtener información detallada de CoinGecko
def obtener_info_cripto_coingecko():
    """
    Consulta la API de CoinGecko para obtener nombres, capitalización y suministro de criptomonedas.
    
    Returns:
        dict: Diccionario con información de las criptomonedas donde la clave es el símbolo (ticker).
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parametros = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }
    
    try:
        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()
        
        # Crear diccionario para acceso rápido
        info_cripto = {}
        for cripto in datos:
            simbolo = cripto['symbol'].upper()
            info_cripto[simbolo] = {
                'nombre': cripto['name'],
                'cap_mercado': cripto['market_cap'],
                'suministro_circulante': cripto['circulating_supply']
            }
        
        return info_cripto
    except Exception as e:
        print(f"Error al obtener datos de CoinGecko: {e}")
        return {}