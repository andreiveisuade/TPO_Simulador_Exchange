# Configuración de actualizaciones
INTERVALO_ACTUALIZACION = 30  # segundos
ACTUALIZACION_AUTOMATICA_HABILITADA = True  # Estado inicial de la actualización automática
LIMITE_CRIPTOMONEDAS_DEFAULT = 20  # Número predeterminado de criptomonedas a mostrar en cotizaciones

ANCHO_VENTANA = 1728
ALTO_VENTANA = 972

datos_cotizaciones = []
actualizando = False
auto_actualizacion = True
hilo_auto_actualizacion = None
detener_auto_actualizacion = False