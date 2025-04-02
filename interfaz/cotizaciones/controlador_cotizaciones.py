import threading
import dearpygui.dearpygui as dpg
from interfaz.cotizaciones.modelo_cotizaciones import (
    obtener_tabla_cotizaciones, 
    formatear_precio, 
    formatear_porcentaje, 
    formatear_volumen
)
from interfaz.cotizaciones.vista_cotizaciones import (
    crear_panel_cotizaciones,
    actualizar_tabla_ui,
    actualizar_estado_boton
)

# Estado de la aplicación (usando diccionario en lugar de variables globales)
estado = {
    "datos_cotizaciones": [],
    "actualizando": False
}

def actualizar_datos_thread(limite):
    """
    Función para actualizar datos en un hilo separado.
    
    Args:
        limite: Número máximo de criptomonedas a obtener.
    """
    # Actualizar estado
    estado["actualizando"] = True
    actualizar_estado_boton(True)
    
    print(f"Iniciando actualización de datos con límite {limite}...")
    
    try:
        # Obtener datos desde el modelo
        print("Obteniendo datos de cotizaciones...")
        estado["datos_cotizaciones"] = obtener_tabla_cotizaciones(limite)
        print(f"Datos obtenidos: {len(estado['datos_cotizaciones'])} criptomonedas")
        
        # Imprimir primera entrada para depuración
        if estado["datos_cotizaciones"] and len(estado["datos_cotizaciones"]) > 0:
            print(f"Primera criptomoneda: {estado['datos_cotizaciones'][0]}")
        
        # Actualizar la vista
        print("Actualizando tabla...")
        actualizar_tabla_ui(
            estado["datos_cotizaciones"],
            formatear_precio,
            formatear_porcentaje,
            formatear_volumen
        )
        print("Tabla actualizada")
        
    except Exception as e:
        print(f"Error al actualizar datos: {e}")
    
    # Restaurar estado
    actualizar_estado_boton(False)
    estado["actualizando"] = False

def iniciar_actualizacion(sender, app_data, user_data):
    """
    Inicia el proceso de actualización en un hilo separado.
    Callback para el botón de actualización.
    """
    if not estado["actualizando"]:
        try:
            limite = dpg.get_value("input_limite")
            print(f"Iniciando hilo de actualización con límite: {limite}")
            thread = threading.Thread(target=actualizar_datos_thread, args=(limite,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error al iniciar actualización: {e}")

def inicializar_panel_cotizaciones():
    """
    Inicializa el panel de cotizaciones.
    Crea la interfaz de usuario.
    """
    crear_panel_cotizaciones(iniciar_actualizacion)

def cargar_datos_iniciales():
    """
    Carga los datos iniciales de la tabla de cotizaciones.
    Se llama al iniciar la aplicación.
    """
    try:
        print("Iniciando carga de datos iniciales...")
        iniciar_actualizacion(None, None, None)
    except Exception as e:
        print(f"Error al cargar datos iniciales: {e}")