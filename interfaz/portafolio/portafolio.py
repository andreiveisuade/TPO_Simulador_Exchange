import dearpygui.dearpygui as dpg
import requests

# Función para obtener precios de CoinGecko
def obtener_precios():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = requests.get(url, params=params)
    return response.json()

# Callback para actualizar la tabla de criptos
def actualizar_precios():
    precios = obtener_precios()
    dpg.delete_item("tabla_precios", children_only=True)
    
    for cripto in precios:
        with dpg.table_row(parent="tabla_precios"):
            dpg.add_text(cripto['name'])
            dpg.add_text(f"${cripto['current_price']:.2f}")
            dpg.add_text(f"{cripto['price_change_percentage_24h']:.2f}%")

# Crear ventana principal
def interfaz_portafolio():
    dpg.create_context()
    with dpg.window(label="Portafolio de Criptomonedas", width=800, height=600):
        dpg.add_button(label="Actualizar Precios", callback=actualizar_precios)
        
        with dpg.table(header_row=True, resizable=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label="Criptomoneda")
            dpg.add_table_column(label="Precio USD")
            dpg.add_table_column(label="Cambio 24h")
            
            with dpg.table_row(tag="tabla_precios"):
                pass  # Contenido dinámico agregado por `actualizar_precios`

    dpg.create_viewport(title='Simulador Exchange', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

