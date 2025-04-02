from dearpygui.dearpygui import *
from interfaz.cotizaciones.controlador_cotizaciones import inicializar_panel_cotizaciones, cargar_datos_iniciales
from interfaz.temas import aplicar_tema_global, aplicar_tema_titulo

# acá adentro hay que poner las funciones para crear las ventanas correspondientes y sus funciones
def crear_ventana_principal():
    # Ventana de Cotizaciones
    with window(label="Cotizaciones", width=1728, height=445, pos=(0, 0), tag="ventana_cotizaciones"):
        # Título (usando formato especial para destacarlo)
        add_spacer(height=5)
        add_text("MERCADO DE CRIPTOMONEDAS", tag="titulo_cotizaciones")
        aplicar_tema_titulo("titulo_cotizaciones")
        add_separator() 
        add_spacer(height=5)
        
        # Panel de cotizaciones
        inicializar_panel_cotizaciones()

    # Ventana de Portafolio
    with window(label="Portafolio", width=1728, height=243, pos=(0, 445)):
        add_spacer(height=5)
        add_text("PORTAFOLIO", tag="titulo_portafolio")
        aplicar_tema_titulo("titulo_portafolio")
        add_separator()
        add_spacer(height=5)
        add_text("Información del portafolio (en desarrollo)")

    # Ventana de Trading
    with window(label="Trading", width=575, height=284, pos=(0, 688)):
        add_spacer(height=5)
        add_text("TRADING", tag="titulo_trading")
        aplicar_tema_titulo("titulo_trading")
        add_separator()
        add_spacer(height=5)
        add_text("Herramientas de trading (en desarrollo)")

    # Ventana de Historial
    with window(label="Historial", width=1153, height=284, pos=(575, 688)):
        add_spacer(height=5)
        add_text("HISTORIAL DE OPERACIONES", tag="titulo_historial")
        aplicar_tema_titulo("titulo_historial")
        add_separator()
        add_spacer(height=5)
        add_text("Registro de operaciones (en desarrollo)")


def iniciar_ui():
    # Crear contexto
    create_context()
    set_global_font_scale(1.25)
    
    # Aplicar el tema global definido en temas.py
    tema_global = aplicar_tema_global()
    bind_theme(tema_global)
    
    # Crear las ventanas
    crear_ventana_principal()
    
    # Configurar y mostrar viewport
    create_viewport(title="Exchange Cripto", width=1728, height=972)
    setup_dearpygui()
    show_viewport()
    
    # Cargar datos iniciales de cotizaciones
    cargar_datos_iniciales()
    
    # Iniciar el bucle de eventos
    start_dearpygui()
    destroy_context()