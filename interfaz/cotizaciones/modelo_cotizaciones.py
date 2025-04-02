import time
from datetime import datetime, timedelta
from api.consulta_api_datos import *


def calcular_cambio_porcentual(velas, periodos=1):
    """
    Calcula el cambio porcentual de precio en un número determinado de periodos.
    
    Args:
        velas (list): Lista de velas OHLC.
        periodos (int): Número de periodos para calcular el cambio.
        
    Returns:
        float: Cambio porcentual.
    """
    if len(velas) <= periodos:
        return 0.0
        
    # Precio de cierre actual (última vela)
    precio_actual = float(velas[-1][4])
    
    # Precio de cierre hace 'periodos' velas
    precio_anterior = float(velas[-1 - periodos][4])
    
    # Cálculo del cambio porcentual
    cambio_porcentual = ((precio_actual - precio_anterior) / precio_anterior) * 100
    
    return round(cambio_porcentual, 2)


def obtener_datos_cotizacion(limite=50):
    """
    Obtiene y formatea datos de cotización para las principales criptomonedas.
    
    Args:
        limite (int): Número máximo de criptomonedas a incluir.
        
    Returns:
        list: Lista de diccionarios con datos formateados.
    """
    # Obtener información detallada de CoinGecko (incluye nombres y cap. de mercado)
    info_coingecko = obtener_info_cripto_coingecko()
    
    # Obtener todos los datos de 24h de Binance
    datos_24h = obtener_precios_24h()
    
    # Filtrar solo pares contra USDT
    pares_usdt = [dato for dato in datos_24h if dato['symbol'].endswith('USDT')]
    
    # Enriquecer datos de Binance con información de CoinGecko
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
    
    # Ordenar por capitalización de mercado (de mayor a menor)
    pares_usdt.sort(key=lambda x: float(x.get('cap_mercado', 0)), reverse=True)
    
    # Limitar al número especificado
    pares_top = pares_usdt[:limite]
    
    # Lista para almacenar datos procesados
    datos_procesados = []
    
    for i, par in enumerate(pares_top):
        simbolo = par['symbol']
        ticker = simbolo.replace('USDT', '')
        
        # Usar nombre completo de CoinGecko o el ticker si no está disponible
        nombre_completo = par.get('nombre_completo', ticker)
        
        # Datos básicos
        precio_actual = float(par['lastPrice'])
        cambio_24h = float(par['priceChangePercent'])
        volumen_24h = float(par['quoteVolume'])
        cap_mercado = par.get('cap_mercado', 'N/A')
        suministro_circulante = par.get('suministro_circulante', 'N/A')
        
        # Para cambio de 1h, necesitamos las velas de 1h
        try:
            velas_1h = obtener_velas_ohlc(simbolo, intervalo="1h", limite=2)
            cambio_1h = calcular_cambio_porcentual(velas_1h, 1)
        except Exception as e:
            cambio_1h = 0.0
            
        # Para cambio de 7d, necesitamos las velas diarias
        try:
            velas_1d = obtener_velas_ohlc(simbolo, intervalo="1d", limite=8)  # 8 para asegurar 7 días completos
            cambio_7d = calcular_cambio_porcentual(velas_1d, 7)
        except Exception as e:
            cambio_7d = 0.0
            
        # Crear diccionario con toda la información
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
        
        # Pausa breve para evitar llegar al límite de tasa de la API
        time.sleep(0.1)
    
    return datos_procesados


def formatear_precio(precio):
    """
    Formatea el precio según su magnitud.
    
    Args:
        precio (float): Precio a formatear.
        
    Returns:
        str: Precio formateado.
    """
    if precio >= 1000:
        return f"${precio:,.2f}"
    elif precio >= 1:
        return f"${precio:.2f}"
    elif precio >= 0.01:
        return f"${precio:.4f}"
    else:
        return f"${precio:.8f}"


def formatear_porcentaje(porcentaje):
    """
    Formatea un cambio porcentual.
    
    Args:
        porcentaje (float): Porcentaje a formatear.
        
    Returns:
        str: Porcentaje formateado.
    """
    if porcentaje > 0:
        return f"+{porcentaje:.2f}%"
    else:
        return f"{porcentaje:.2f}%"


def formatear_volumen(volumen):
    """
    Formatea el volumen con sufijos K, M, B según sea necesario.
    
    Args:
        volumen (float): Volumen a formatear.
        
    Returns:
        str: Volumen formateado.
    """
    if volumen >= 1_000_000_000:
        return f"${volumen / 1_000_000_000:.2f}B"
    elif volumen >= 1_000_000:
        return f"${volumen / 1_000_000:.2f}M"
    elif volumen >= 1_000:
        return f"${volumen / 1_000:.2f}K"
    else:
        return f"${volumen:.2f}"


def obtener_tabla_cotizaciones(limite=50):
    """
    Obtiene y formatea los datos para la tabla de cotizaciones.
    
    Args:
        limite (int): Número máximo de criptomonedas a incluir.
        
    Returns:
        list: Lista de diccionarios con datos formateados para visualización.
    """
    datos = obtener_datos_cotizacion(limite)
    return datos