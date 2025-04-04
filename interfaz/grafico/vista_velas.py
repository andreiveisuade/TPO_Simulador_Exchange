"""
Vista - Se encarga de la visualización directa de los gráficos de velas en DearPyGui.
Esta versión renderiza los gráficos directamente sin guardar imágenes intermedias.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
import dearpygui.dearpygui as dpg
from datetime import datetime

# Colores para los gráficos
COLOR_VERDE = [0, 1, 0, 1]  # RGBA para velas verdes (subida)
COLOR_ROJO = [1, 0, 0, 1]   # RGBA para velas rojas (bajada)
COLOR_VOLUMEN_VERDE = [0, 0.7, 0, 0.5]  # Volumen en verde
COLOR_VOLUMEN_ROJO = [0.7, 0, 0, 0.5]    # Volumen en rojo

def crear_figura_matplotlib(df, par, intervalo, indicadores=None, tema='dark'):
    """
    Crea una figura de Matplotlib con el gráfico de velas.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos OHLCV
        par (str): Par de trading (ej: BTCUSDT)
        intervalo (str): Intervalo de tiempo
        indicadores (dict): Diccionario con indicadores {tipo: parametros}
        tema (str): Tema del gráfico ('dark' o 'light')
        
    Returns:
        matplotlib.figure.Figure: Figura de matplotlib
    """
    if df.empty or len(df) < 2:
        print("No hay datos suficientes para graficar")
        return None
    
    # Configurar el estilo según el tema
    plt.style.use('dark_background' if tema == 'dark' else 'default')
    
    # Crear figura y subplots (uno para precios, otro para volumen)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4), 
                                   gridspec_kw={'height_ratios': [3, 1]},
                                   sharex=True)

    ax1.tick_params(axis='both', labelsize=6, width=0.3)
    ax2.tick_params(axis='both', labelsize=6, width=0.3)
    for spine in ax1.spines.values():
        spine.set_linewidth(0.017)
        spine.set_color('gray')
    for spine in ax2.spines.values():
        spine.set_linewidth(0.017)
        spine.set_color('gray')
    
    ax1.yaxis.tick_right()
    ax2.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax2.yaxis.set_label_position("right")
    
    ax1.ticklabel_format(useOffset=False)
    ax2.ticklabel_format(useOffset=False)
    
    # Preparar datos
    dates = df.index
    x_vals = mdates.date2num(dates)
    opens = df['open'].values
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    volumes = df['volume'].values
    
    # Calcular colores basados en dirección del precio
    colors = [COLOR_VERDE[0:3] if c >= o else COLOR_ROJO[0:3] for c, o in zip(closes, opens)]
    vol_colors = [COLOR_VOLUMEN_VERDE[0:3] if c >= o else COLOR_VOLUMEN_ROJO[0:3] for c, o in zip(closes, opens)]
    
    # ---- Dibujar gráfico de velas ----
    # Dibujar cuerpos
    width = 0.02
    rect_width = width * 0.2
    for i in range(len(df)):
        # Cuerpo de la vela
        height = abs(closes[i] - opens[i])
        bottom = min(closes[i], opens[i])
        rect = plt.Rectangle((x_vals[i] - rect_width/2, bottom), 
                            rect_width, height, 
                            color=colors[i], 
                            alpha=1, zorder=2)
        ax1.add_patch(rect)
        
        # Mecha (línea vertical)
        ax1.plot([x_vals[i], x_vals[i]], [lows[i], highs[i]], 
                color=colors[i], linewidth=1.5, zorder=1)
    
    # Ajustar eje X
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    if intervalo in ['1m', '5m', '15m', '30m', '1h', '2h', '4h']:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    # Rotar etiquetas del eje X
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Dibujar volumen
    ax2.bar(x_vals, volumes, width=width, color=vol_colors, alpha=0.7)
    ax2.set_ylabel('')
    
    # Asegurar que no aparezca notación científica
    ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1.get_yaxis().get_major_formatter().set_scientific(False)
    ax2.get_yaxis().get_major_formatter().set_scientific(False)

    # Indicadores técnicos
    if indicadores and 'ma' in indicadores:
        colors_ma = ['cyan', 'magenta', 'yellow', 'white']
        for i, periodo in enumerate(indicadores['ma']):
            if periodo < len(df):  # Verificar que hay suficientes datos
                ma = df['close'].rolling(window=periodo).mean()
                if not ma.isna().all():  # Verificar que hay datos válidos
                    ax1.plot(dates, ma, color=colors_ma[i % len(colors_ma)], 
                            linewidth=1.5, label=f'MA({periodo})')
    
    # Ajustar límites del gráfico
    ax1.grid(True, alpha=0.9, linewidth=0.015, color='gray')
    ax2.grid(True, alpha=0.9, linewidth=0.015, color='gray')
    
    # Ajustar diseño
    fig.tight_layout()
    
    return fig

def figura_a_texture(fig, tag_textura):
    """
    Convierte una figura de matplotlib a una textura de DearPyGui.
    
    Args:
        fig: Figura de matplotlib
        tag_textura: Tag para la textura en DearPyGui
        
    Returns:
        tuple: (width, height) de la textura
    """
    if fig is None:
        return None, None
    
    # Renderizar figura a un array
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    img_array = np.asarray(buf)
    
    # Obtener dimensiones
    height, width = img_array.shape[:2]
    
    # Convertir a formato que DearPyGui pueda entender (1D array)
    img_data = []
    for i in range(height):
        for j in range(width):
            pixel = img_array[i, j]
            img_data.extend([pixel[0], pixel[1], pixel[2], pixel[3]])
    
    # Crear o actualizar textura
    if not dpg.does_item_exist(tag_textura):
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, img_data, tag=tag_textura)
    else:
        dpg.set_value(tag_textura, img_data)
    
    # Liberar memoria
    plt.close(fig)
    
    return width, height

def mostrar_grafico_directo(df, par, intervalo, tag_textura, tag_imagen=None, 
                           parent=None, indicadores=None, tema='dark'):
    """
    Crea y muestra un gráfico de velas directamente en DearPyGui.
    
    Args:
        df (pandas.DataFrame): DataFrame con datos OHLCV
        par (str): Par de trading (ej: BTCUSDT)
        intervalo (str): Intervalo de tiempo
        tag_textura (str): Tag para la textura
        tag_imagen (str): Tag para la imagen (si ya existe)
        parent (str): Tag del contenedor padre
        indicadores (dict): Diccionario con indicadores
        tema (str): Tema del gráfico
        
    Returns:
        str: Tag de la imagen creada o actualizada
    """
    if df.empty:
        print("No hay datos para mostrar")
        return None
    
    try:
        # Crear figura con matplotlib
        fig = crear_figura_matplotlib(df, par, intervalo, indicadores, tema)
        if fig is None:
            return None
        
        # Convertir figura a textura
        width, height = figura_a_texture(fig, tag_textura)
        if width is None:
            return None
        
        # Si no existe la imagen, crearla
        if tag_imagen is None:
            tag_imagen = f"img_{tag_textura}"
        
        if not dpg.does_item_exist(tag_imagen):
            if parent:
                dpg.add_image(tag_textura, tag=tag_imagen, parent=parent)
            else:
                dpg.add_image(tag_textura, tag=tag_imagen)
        
        return tag_imagen
    
    except Exception as e:
        print(f"Error al crear el gráfico directo: {e}")
        import traceback
        traceback.print_exc()
        return None

def generar_id_grafico(par, intervalo):
    """
    Genera un ID único para el gráfico basado en el par e intervalo.
    
    Args:
        par (str): Par de trading
        intervalo (str): Intervalo de tiempo
        
    Returns:
        str: ID único para el gráfico
    """
    from datetime import datetime
    timestamp = int(datetime.now().timestamp())
    return f"grafico_{par}_{intervalo}_{timestamp}"