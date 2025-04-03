# config.py (en la raíz del proyecto)

# Configuración de actualizaciones
INTERVALO_ACTUALIZACION = 30  # Tiempo en segundos entre actualizaciones automáticas
ACTUALIZACION_AUTOMATICA_HABILITADA = True  # Estado inicial de la actualización automática
LIMITE_CRIPTOMONEDAS_DEFAULT = 20  # Número predeterminado de criptomonedas a mostrar

ANCHO_VENTANA = 1728
ALTO_VENTANA = 972

datos_cotizaciones = []
actualizando = False
auto_actualizacion = ACTUALIZACION_AUTOMATICA_HABILITADA
hilo_auto_actualizacion = None
detener_auto_actualizacion = False