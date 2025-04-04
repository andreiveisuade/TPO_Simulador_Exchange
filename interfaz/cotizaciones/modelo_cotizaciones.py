"""
Este archivo contiene toda la lógica de obtención y procesamiento de datos:

- Funciones para obtener información de criptomonedas desde las APIs
- Cálculo de cambios porcentuales
- Formateo de valores (precios, porcentajes, volúmenes)
"""

import time
from api.consulta_api_datos import *

def calcular_cambio_porcentual(velas, periodos=1):
    """Calcula el cambio porcentual de precio en un número determinado de periodos."""
    if len(velas) <= periodos:
        return 0.0
        
    precio_actual = float(velas[-1][4])
    precio_anterior = float(velas[-1 - periodos][4])
    cambio_porcentual = ((precio_actual - precio_anterior) / precio_anterior) * 100
    
    return round(cambio_porcentual, 2)

def obtener_datos_cotizacion(limite=50):
    """Obtiene datos de cotización para las principales criptomonedas."""
    # Obtener información de CoinGecko
    info_coingecko = obtener_info_cripto_coingecko()
    
    # Obtener datos de Binance
    datos_24h = obtener_precios_24h()
    pares_usdt = [dato for dato in datos_24h if dato['symbol'].endswith('USDT')]
    
    # Enriquecer datos con información de CoinGecko
    for par in pares_usdt:
        ticker = par['symbol'].replace('USDT', '')
        if ticker in info_coingecko:
            par['nombre_completo'] = info_coingecko[ticker]['nombre']
            par['cap_mercado'] = info_coingecko[ticker]['cap_mercado']
            par['suministro_circulante'] = info_coingecko[ticker]['suministro_circulante']
        else:
            par['nombre_completo'] = ticker
            par['cap_mercado'] = 0
            par['suministro_circulante'] = 0
    
    pares_usdt.sort(key=lambda par: float(par.get('cap_mercado', 0)), reverse=True)
    pares_top = pares_usdt[:limite]
    
    # Procesar datos
    datos_procesados = []
    for i, par in enumerate(pares_top):
        simbolo = par['symbol']
        ticker = simbolo.replace('USDT', '')
        nombre_completo = par.get('nombre_completo', ticker)
        
        # Datos básicos
        precio_actual = float(par['lastPrice'])
        cambio_24h = float(par['priceChangePercent'])
        volumen_24h = float(par['quoteVolume'])
        cap_mercado = par.get('cap_mercado', 'N/A')
        suministro_circulante = par.get('suministro_circulante', 'N/A')
        
        # Para cambio de 1h
        try:
            velas_1h = obtener_velas_ohlc(simbolo, intervalo="1h", limite=2)
            cambio_1h = calcular_cambio_porcentual(velas_1h, 1)
        except:
            cambio_1h = 0.0
            
        # Para cambio de 7d
        try:
            velas_1d = obtener_velas_ohlc(simbolo, intervalo="1d", limite=8)
            cambio_7d = calcular_cambio_porcentual(velas_1d, 7)
        except:
            cambio_7d = 0.0
            
        # Crear diccionario con la información
        crypto_data = {
            'posicion': i + 1,
            'nombre': f"{nombre_completo} ({ticker})",
            'ticker': ticker,
            'precio': precio_actual,
            'cambio_1h': cambio_1h,
            'cambio_24h': cambio_24h,
            'cambio_7d': cambio_7d,
            'volumen_24h': volumen_24h,
            'cap_mercado': cap_mercado,
            'suministro_circulante': suministro_circulante
        }
        
        datos_procesados.append(crypto_data)
        time.sleep(0.1)  # Pausa para evitar límites de la API
    
    return datos_procesados

def formatear_precio(precio):
    """Formatea el precio según su magnitud."""
    if precio >= 1000:
        return f"${precio:,.2f}"
    elif precio >= 1:
        return f"${precio:.2f}"
    elif precio >= 0.01:
        return f"${precio:.4f}"
    else:
        return f"${precio:.8f}"

def formatear_porcentaje(porcentaje):
    """Formatea un cambio porcentual."""
    if porcentaje > 0:
        return f"+{porcentaje:.2f}%"
    else:
        return f"{porcentaje:.2f}%"

def formatear_volumen(volumen):
    """Formatea el volumen con sufijos K, M, B."""
    if volumen >= 1_000_000_000:
        return f"${volumen / 1_000_000_000:.2f}B"
    elif volumen >= 1_000_000:
        return f"${volumen / 1_000_000:.2f}M"
    elif volumen >= 1_000:
        return f"${volumen / 1_000:.2f}K"
    else:
        return f"${volumen:.2f}"

def obtener_tabla_cotizaciones(limite=50):
    """Obtiene y formatea los datos para la tabla de cotizaciones."""
    return obtener_datos_cotizacion(limite)