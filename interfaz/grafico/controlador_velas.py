"""
Controlador - Conecta el modelo con la vista y maneja la lógica de la aplicación.
Versión que integra los gráficos directamente con DearPyGui.
"""

import dearpygui.dearpygui as dpg
import interfaz.grafico.modelo_velas as modelo
import interfaz.grafico.vista_velas as vista
from api.consulta_api_datos import obtener_velas_ohlc

# Variable para almacenar el estado del gráfico actual
estado_grafico = {
    "textura_actual": None,
    "imagen_actual": None,
    "par_actual": None,
    "intervalo_actual": None
}

def inicializar():
    """
    Inicializa el controlador y prepara los recursos necesarios.
    """
    # Crear registry para texturas si no existe
    if not dpg.does_item_exist("texture_registry"):
        with dpg.texture_registry(tag="texture_registry"):
            pass

def actualizar_grafico_velas(par, intervalo, periodos_ma=None, tema='dark', parent="area_grafico"):
    """
    Actualiza el gráfico de velas con los datos más recientes y lo muestra directamente.
    
    Args:
        par (str): Par de trading (ej: BTCUSDT)
        intervalo (str): Intervalo de tiempo
        periodos_ma (list, optional): Lista de períodos para medias móviles
        tema (str): Tema del gráfico ('dark' o 'light')
        parent (str): Tag del contenedor padre donde mostrar el gráfico
        
    Returns:
        bool: True si se actualizó correctamente, False en caso contrario
    """
    # Obtener datos desde la API existente
    datos_velas = obtener_velas_ohlc(par, intervalo)
    
    # Si no hay datos, retornar False
    if not datos_velas:
        print(f"No se pudieron obtener datos para {par} en intervalo {intervalo}")
        return False
    
    # Mostrar información de debug
    print(f"Datos recibidos para {par}:")
    print(f"Cantidad de velas: {len(datos_velas)}")
    if datos_velas:
        print(f"Primera vela: {datos_velas[0]}")
    
    # Convertir datos a DataFrame
    df = modelo.convertir_datos_a_dataframe(datos_velas)
    
    # Verificar si el DataFrame está vacío
    if df.empty:
        print(f"Error: DataFrame vacío después de convertir datos para {par}")
        return False
    
    # Generar configuración de indicadores si es necesario
    indicadores = None
    if periodos_ma:
        indicadores = {'ma': periodos_ma}
    
    # Generar identificadores únicos para la textura y la imagen
    if estado_grafico["par_actual"] != par or estado_grafico["intervalo_actual"] != intervalo:
        # Si cambió el par o intervalo, crear nuevos identificadores
        tag_textura = f"textura_{vista.generar_id_grafico(par, intervalo)}"
        tag_imagen = f"imagen_{vista.generar_id_grafico(par, intervalo)}"
        
        # Actualizar estado
        if estado_grafico["imagen_actual"] and dpg.does_item_exist(estado_grafico["imagen_actual"]):
            dpg.delete_item(estado_grafico["imagen_actual"])
        
        estado_grafico["textura_actual"] = tag_textura
        estado_grafico["imagen_actual"] = tag_imagen
        estado_grafico["par_actual"] = par
        estado_grafico["intervalo_actual"] = intervalo
    else:
        # Usar los mismos identificadores para actualizar
        tag_textura = estado_grafico["textura_actual"]
        tag_imagen = estado_grafico["imagen_actual"]
    
    # Crear y mostrar el gráfico
    resultado = vista.mostrar_grafico_directo(
        df, par, intervalo, tag_textura, 
        tag_imagen=tag_imagen, parent=parent,
        indicadores=indicadores, tema=tema
    )
    
    return resultado is not None

def obtener_lista_pares(base_asset='USDT', limite=10):
    """
    Obtiene la lista de pares disponibles para mostrar en la interfaz.
    
    Args:
        base_asset (str): Activo base (ej: USDT, BTC)
        limite (int): Número máximo de pares a retornar
        
    Returns:
        list: Lista de símbolos de pares
    """
    return modelo.obtener_pares_disponibles(base_asset, limite)

def obtener_lista_intervalos():
    """
    Obtiene la lista de intervalos disponibles para mostrar en la interfaz.
    
    Returns:
        list: Lista de intervalos disponibles
    """
    return modelo.obtener_intervalos_disponibles()