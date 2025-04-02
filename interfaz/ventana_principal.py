from dearpygui.dearpygui import *

# acá adentro hay que poner las funciones para crear las ventanas correspondientes y sus funciones
def crear_ventana_principal():

    with window(label="Cotizaciones", width=1728, height=445, pos=(0, 0)):
        add_text("Panel de Cotizaciones (vacío)")

    with window(label="Portafolio", width=1728, height=243, pos=(0, 445)):
        add_text("Panel de Portafolio (vacío)")

    with window(label="Trading", width=575, height=284, pos=(0, 688)):
        add_text("Panel de Trading (vacío)")

    with window(label="Historial", width=1153, height=284, pos=(575, 688)):
        add_text("Panel de Historial (vacío)")


def iniciar_ui():
    create_context()
    crear_ventana_principal()
    create_viewport(title="Exchange Cripto", width=1728, height=972)
    setup_dearpygui()
    show_viewport()
    start_dearpygui()
    destroy_context()
