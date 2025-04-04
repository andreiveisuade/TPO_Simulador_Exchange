"""
Modelo - Se encarga de procesar los datos para los gráficos de velas.
Utiliza la API ya implementada en consulta_api_datos.py
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Importar las funciones de la API existente - Ajusta esta ruta a donde esté realmente tu módulo
from api.consulta_api_datos import *

def convertir_datos_a_dataframe(datos_velas):
    """
    Convierte los datos de velas de Binance a un DataFrame de pandas con formato para mplfinance.
    
    Args:
        datos_velas (list): Lista de datos de velas desde Binance
        
    Returns:
        pandas.DataFrame: DataFrame con columnas OHLCV y timestamps como índices
    """
    if not datos_velas:
        print("Advertencia: No hay datos de velas para convertir")
        return pd.DataFrame()
    
    # Imprimir una muestra para debug
    print(f"Ejemplo de datos de velas recibidos: {datos_velas[0]}")
    
    try:
        # Crear DataFrame a partir de los datos de velas
        # Estructura de Binance: [tiempo_apertura, open, high, low, close, volumen, ...]
        df = pd.DataFrame(datos_velas, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Convertir tipos de datos
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convertir timestamp a datetime (Binance usa milisegundos)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Establecer timestamp como índice (requerido por mplfinance)
        df = df.set_index('timestamp')
        
        # Seleccionar solo las columnas necesarias para mplfinance
        df = df[['open', 'high', 'low', 'close', 'volume']]
        
        # Verificar si hay valores NaN
        nan_count = df.isna().sum().sum()
        if nan_count > 0:
            print(f"Advertencia: El DataFrame contiene {nan_count} valores NaN")
        
        return df
    
    except Exception as e:
        print(f"Error al convertir datos a DataFrame: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def calcular_indicador_ma(df, periodo=20):
    """
    Calcula la media móvil simple para un DataFrame de velas.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos OHLCV
        periodo (int): Número de períodos para la media móvil
        
    Returns:
        pandas.Series: Serie con la media móvil calculada
    """
    if df.empty:
        return pd.Series()
    
    return df['close'].rolling(window=periodo).mean()

def obtener_pares_disponibles(base_asset='USDT', limite=10):
    """
    Obtiene los pares de trading disponibles con mayor volumen.
    
    Args:
        base_asset (str): Activo base (ej: USDT, BTC)
        limite (int): Número máximo de pares a retornar
        
    Returns:
        list: Lista de símbolos de pares
    """
    try:
        # Usar la función existente para obtener datos de 24h
        datos = obtener_precios_24h()
        
        # Filtrar por activo base y ordenar por volumen
        pares_filtrados = [
            item['symbol'] for item in datos 
            if item['symbol'].endswith(base_asset)
        ]
        
        # Ordenar por volumen (convertido a float)
        pares_ordenados = sorted(
            [item for item in datos if item['symbol'] in pares_filtrados],
            key=lambda x: float(x['volume']), 
            reverse=True
        )
        
        # Devolver los símbolos de los pares con mayor volumen
        return [item['symbol'] for item in pares_ordenados[:limite]]
    
    except Exception as e:
        print(f"Error al obtener pares disponibles: {e}")
        return []

def obtener_intervalos_disponibles():
    """
    Retorna los intervalos de tiempo disponibles en Binance.
    
    Returns:
        list: Lista de intervalos disponibles
    """
    return ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

def obtener_datos_mercado(simbolo):
    """
    Obtiene información adicional de mercado para un símbolo específico.
    
    Args:
        simbolo (str): Símbolo de la criptomoneda (ej: BTC)
        
    Returns:
        dict: Información de mercado o diccionario vacío si no hay datos
    """
    # Extraer el símbolo base del par (ej: de BTCUSDT obtener BTC)
    simbolo_base = simbolo.rstrip('USDT')
    
    # Obtener información de CoinGecko
    datos_mercado = obtener_info_cripto_coingecko()
    
    # Si el símbolo existe en los datos, retornarlo
    if simbolo_base in datos_mercado:
        return datos_mercado[simbolo_base]
    
    return {}