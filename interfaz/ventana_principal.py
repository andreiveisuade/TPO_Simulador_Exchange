from dearpygui.dearpygui import *
from interfaz.cotizaciones.controlador_cotizaciones import inicializar_panel_cotizaciones, cargar_datos_iniciales
from interfaz.temas import aplicar_tema_global, aplicar_tema_titulo
from interfaz.grafico.integracion_grafico_velas import configurar_ventana_grafico

def crear_ventana_principal():
    # Ventana de Cotizaciones
    with window(label="Cotizaciones", width=850, height=415, pos=(0, 0), tag="ventana_cotizaciones"):
        # Título (usando formato especial para destacarlo)
        add_spacer(height=5)
        add_text("MERCADO DE CRIPTOMONEDAS", tag="titulo_cotizaciones", show=False)
        aplicar_tema_titulo("titulo_cotizaciones")
        
        # Panel de cotizaciones
        inicializar_panel_cotizaciones()
    
    # Ventana de Grafico - Ahora con tag para poder acceder desde el integrador
    with window(label="Grafico", width=678, height=688, pos=(850, 000), tag="ventana_grafico"):
        add_spacer(height=5)
        add_text("GRAFICO", tag="titulo_grafico")
        add_separator()
        
        # Configurar la ventana de gráfico de velas
        configurar_ventana_grafico()

    # Ventana de Portafolio
    with window(label="Portafolio", width=850, height=273, pos=(0, 415)):
        add_spacer(height=5)
        add_text("PORTAFOLIO", tag="titulo_portafolio")
        aplicar_tema_titulo("titulo_portafolio")
        add_separator()
        add_spacer(height=5)
        add_text("Información del portafolio (en desarrollo)")

    # Ventana de Trading
    with window(label="Trading", width=675, height=312, pos=(850, 688)):
        add_spacer(height=5)
        add_text("TRADING", tag="titulo_trading")
        aplicar_tema_titulo("titulo_trading")
        add_separator()
        add_spacer(height=5)
        add_text("Herramientas de trading (en desarrollo)")

    # Ventana de Historial
    with window(label="Historial", width=850, height=312, pos=(0, 688)):
        add_spacer(height=5)
        add_text("HISTORIAL DE OPERACIONES", tag="titulo_historial")
        aplicar_tema_titulo("titulo_historial")
        add_separator()
        add_spacer(height=5)
        add_text("Registro de operaciones (en desarrollo)")


def iniciar_ui():
    # Crear contexto
    create_context()
    set_global_font_scale(1.1)
    
    # Aplicar el tema global definido en temas.py
    tema_global = aplicar_tema_global()
    bind_theme(tema_global)
    
    # Crear las ventanas
    crear_ventana_principal()
    
    # Configurar y mostrar viewport
    create_viewport(title="Exchange Cripto", width=1528, height=1000)
    setup_dearpygui()
    show_viewport()
    
    # Cargar datos iniciales de cotizaciones
    cargar_datos_iniciales()
    
    # Iniciar el bucle de eventos
    start_dearpygui()
    destroy_context()