"""
Este archivo conecta el modelo con la vista:

- Gestiona los hilos para actualización de datos
- Maneja eventos de la interfaz
- Controla el flujo de actualización automática
"""

import threading
import time
import dearpygui.dearpygui as dpg
import config
from interfaz.cotizaciones.modelo_cotizaciones import *
from interfaz.cotizaciones.vista_cotizaciones import *

def inicializar_panel_cotizaciones():
    """Inicializa el panel de cotizaciones"""
    # Crear panel con los manejadores
    crear_panel_cotizaciones(
        btn_actualizar_fn=btn_actualizar_handler,
        chk_auto_actualizacion_fn=chk_auto_actualizacion_handler
    )

def cargar_datos_iniciales():
    """Carga los datos iniciales de la tabla de cotizaciones"""
    try:
        print("Iniciando carga de datos iniciales...")
        btn_actualizar_handler()
        
        # Iniciar actualización automática si está habilitada
        if config.auto_actualizacion:
            iniciar_actualizacion_automatica()
    except Exception as e:
        print(f"Error al cargar datos iniciales: {e}")
        
def actualizar_datos_cotizaciones():
    """Función que actualiza los datos de cotizaciones"""
    config.actualizando = True
    actualizar_estado_boton(True)
    
    try:
        # Obtener límite de criptomonedas
        limite = dpg.get_value("input_limite") if dpg.does_item_exist("input_limite") else config.LIMITE_CRIPTOMONEDAS_DEFAULT
        
        # Obtener datos
        config.datos_cotizaciones = obtener_tabla_cotizaciones(limite)
        
        # Recrear la tabla con los nuevos datos
        crear_tabla_cotizaciones(
            config.datos_cotizaciones,
            formatear_precio,
            formatear_porcentaje,
            formatear_volumen
        )
        
        # Actualizar hora de actualización
        actualizar_hora_actualizacion()
    except Exception as e:
        print(f"Error al actualizar datos: {e}")
    
    actualizar_estado_boton(False)
    config.actualizando = False

def btn_actualizar_handler(sender=None, app_data=None, user_data=None):
    """Manejador para el botón de actualización"""
    if not config.actualizando:
        hilo = threading.Thread(target=actualizar_datos_cotizaciones, daemon=True)
        hilo.start()

def chk_auto_actualizacion_handler(sender, app_data):
    """Manejador para el checkbox de actualización automática"""
    config.auto_actualizacion = app_data
    
    if app_data and (config.hilo_auto_actualizacion is None or not config.hilo_auto_actualizacion.is_alive()):
        iniciar_actualizacion_automatica()

def bucle_actualizacion_automatica():
    """Hilo que ejecuta actualizaciones periódicas"""
    while not config.detener_auto_actualizacion:
        # Esperar el intervalo configurado
        for _ in range(config.INTERVALO_ACTUALIZACION):
            if config.detener_auto_actualizacion:
                break
            time.sleep(1)
        
        # Verificar si debe continuar actualizando
        if config.detener_auto_actualizacion or not config.auto_actualizacion:
            continue
        
        # Actualizar si no está en proceso
        if not config.actualizando:
            actualizar_datos_cotizaciones()

def iniciar_actualizacion_automatica():
    """Inicia el proceso de actualización automática"""
    config.detener_auto_actualizacion = False
    
    # Crear y lanzar el hilo solo si no existe o no está activo
    if config.hilo_auto_actualizacion is None or not config.hilo_auto_actualizacion.is_alive():
        hilo = threading.Thread(target=bucle_actualizacion_automatica, daemon=True)
        hilo.start()
        config.hilo_auto_actualizacion = hilo



def detener_servicios():
    """Detiene los hilos y servicios antes de cerrar la aplicación"""
    config.detener_auto_actualizacion = True