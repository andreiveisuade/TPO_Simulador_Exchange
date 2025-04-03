# interfaz/cotizaciones/controlador_cotizaciones.py (simplificado)
import threading
import time
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
    actualizar_estado_boton,
    actualizar_estado_auto_actualizacion
)

# Estado de la aplicación
INTERVALO_ACTUALIZACION = 30  # Segundos entre actualizaciones

# Variables globales
datos_cotizaciones = []
actualizando = False
auto_actualizacion = True
hilo_auto_actualizacion = None
detener_auto_actualizacion = False

def actualizar_datos_thread(limite):
    """Función para actualizar datos en un hilo separado"""
    global datos_cotizaciones, actualizando
    actualizando = True
    
    actualizar_estado_boton(True)
    
    try:
        # Obtener datos
        datos_cotizaciones = obtener_tabla_cotizaciones(limite)
        
        # Actualizar tabla
        actualizar_tabla_ui(
            datos_cotizaciones,
            formatear_precio,
            formatear_porcentaje,
            formatear_volumen
        )
        
    except Exception as e:
        print(f"Error al actualizar datos: {e}")
        
    # Restaurar estado
    actualizar_estado_boton(False)
    actualizando = False

def iniciar_actualizacion(sender, app_data, user_data):
    """Inicia el proceso de actualización en un hilo separado"""
    global actualizando
    if not actualizando:
        try:
            if dpg.does_item_exist("input_limite"):
                limite = dpg.get_value("input_limite")
            else:
                limite = 20  # Valor por defecto
                
            print(f"Iniciando hilo de actualización con límite: {limite}")
            thread = threading.Thread(target=actualizar_datos_thread, args=(limite,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error al iniciar actualización: {e}")

def _actualizacion_periodica():
    """Hilo para actualización periódica"""
    global detener_auto_actualizacion, auto_actualizacion
    
    while not detener_auto_actualizacion:
        # Esperar el intervalo
        for _ in range(INTERVALO_ACTUALIZACION):
            if detener_auto_actualizacion:
                break
            time.sleep(1)
            
        # Verificar si debe continuar
        if detener_auto_actualizacion or not auto_actualizacion:
            continue
            
        # Actualizar si no está en proceso
        if not actualizando:
            print("Ejecutando actualización automática...")
            iniciar_actualizacion(None, None, None)

def iniciar_actualizacion_automatica():
    """Inicia un hilo para actualizar periódicamente"""
    global hilo_auto_actualizacion, detener_auto_actualizacion
    
    detener_auto_actualizacion = False
    
    if hilo_auto_actualizacion is None or not hilo_auto_actualizacion.is_alive():
        hilo_auto_actualizacion = threading.Thread(target=_actualizacion_periodica)
        hilo_auto_actualizacion.daemon = True
        hilo_auto_actualizacion.start()
        print(f"Actualización automática iniciada (cada {INTERVALO_ACTUALIZACION} segundos)")

def cambiar_estado_auto_actualizacion(sender, app_data):
    """Callback para el checkbox de actualización automática"""
    global auto_actualizacion, detener_auto_actualizacion
    
    auto_actualizacion = app_data
    
    if auto_actualizacion:
        # Iniciar la actualización automática
        iniciar_actualizacion_automatica()
    else:
        # Solo desactivar la bandera, el hilo se detendrá automáticamente
        print("Actualización automática desactivada")

def inicializar_panel_cotizaciones():
    """Inicializa el panel de cotizaciones"""
    crear_panel_cotizaciones(
        callback_actualizacion=iniciar_actualizacion,
        callback_auto_actualizacion=cambiar_estado_auto_actualizacion
    )

def cargar_datos_iniciales():
    """Carga los datos iniciales de la tabla de cotizaciones"""
    try:
        print("Iniciando carga de datos iniciales...")
        iniciar_actualizacion(None, None, None)
        
        # Iniciar actualización automática
        if auto_actualizacion:
            iniciar_actualizacion_automatica()
            
    except Exception as e:
        print(f"Error al cargar datos iniciales: {e}")