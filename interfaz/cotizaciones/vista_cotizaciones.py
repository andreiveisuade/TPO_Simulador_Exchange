"""
Este archivo gestiona la interfaz de usuario:

- Creación de la tabla y paneles
- Formato visual de los datos
- Actualización de elementos de UI
"""

import dearpygui.dearpygui as dpg
from datetime import datetime
import config

def crear_panel_cotizaciones(btn_actualizar_fn, chk_auto_actualizacion_fn):
    """Crea el panel en la interfaz de cotizaciones el panel de cotizaciones"""
    try:
        # Panel de control con límite y botón de actualización
        with dpg.group(horizontal=True):
            dpg.add_text("Número de criptomonedas:")
            dpg.add_input_int(label="", default_value=config.LIMITE_CRIPTOMONEDAS_DEFAULT, 
                            min_value=1, max_value=100, tag="input_limite", width=100)
            dpg.add_button(label="Actualizar Datos", callback=btn_actualizar_fn, 
                          tag="btn_actualizar")
        
        # Checkbox para actualización automática
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label=f"Actualización automática ({config.INTERVALO_ACTUALIZACION}s)", 
                default_value=config.ACTUALIZACION_AUTOMATICA_HABILITADA,
                callback=chk_auto_actualizacion_fn, 
                tag="chk_auto_actualizacion"
            )
            dpg.add_text("Última act: --:--:--", tag="txt_ultima_actualizacion")
        
        dpg.add_spacer(height=10)
        
        # Contenedor para la tabla
        dpg.add_child_window(tag="contenedor_tabla", no_scrollbar=True, height=350)
        
    except Exception as e:
        print(f"Error al crear panel de cotizaciones: {e}")

def truncar_texto(texto, longitud_maxima=25):
    """Trunca un texto si excede la longitud máxima"""
    if isinstance(texto, str) and len(texto) > longitud_maxima:
        return texto[:longitud_maxima-3] + "..."
    return texto

def obtener_color_cambio(valor):
    """Obtiene el color según el cambio porcentual"""
    if valor > 0:
        return [0, 255, 0, 255]  # Verde para valores positivos
    elif valor < 0:
        return [255, 0, 0, 255]  # Rojo para valores negativos
    else:
        return [255, 255, 255, 255]  # Blanco para valores neutros


def crear_tabla_cotizaciones(datos, formatear_precio, formatear_porcentaje, formatear_volumen):
    """Crea la tabla de cotizaciones con los datos proporcionados"""
    try:
        # Eliminar tabla si ya existe
        if dpg.does_item_exist("tabla_cotizaciones"):
            dpg.delete_item("tabla_cotizaciones")
            
        # Definir anchos de columnas
        anchos = {
            "#": 50,
            "Nombre": 250,
            "Precio": 100,
            "1h%": 80,
            "24h%": 80,
            "7d%": 80,
            "Volumen 24h": 120,
            "Cap. Mercado": 120,
            "Suministro": 120
        }
        
        # Calcular ancho total
        ancho_total = sum(anchos.values())
        
        # Crear tabla
        with dpg.table(tag="tabla_cotizaciones",
                       parent="contenedor_tabla",
                       header_row=True,
                       borders_innerH=True,
                       borders_innerV=True,
                       borders_outerH=True,
                       borders_outerV=True,
                       resizable=True,
                       height=320,
                       width=ancho_total,
                       policy=dpg.mvTable_SizingFixedFit,
                    #    scrollX=True,
                    #    scrollY=True,
                       freeze_columns=1):
            
            # Añadir columnas
            dpg.add_table_column(label="#", width=anchos["#"])
            dpg.add_table_column(label="Nombre", width=anchos["Nombre"])
            dpg.add_table_column(label="Precio", width=anchos["Precio"])
            dpg.add_table_column(label="1h%", width=anchos["1h%"])
            dpg.add_table_column(label="24h%", width=anchos["24h%"])
            dpg.add_table_column(label="7d%", width=anchos["7d%"])
            dpg.add_table_column(label="Volumen 24h", width=anchos["Volumen 24h"])
            dpg.add_table_column(label="Cap. Mercado", width=anchos["Cap. Mercado"])
            dpg.add_table_column(label="Suministro", width=anchos["Suministro"])
            
            # Si no hay datos, mostrar mensaje
            if not datos:
                with dpg.table_row():
                    dpg.add_text("--")
                    dpg.add_text("No hay datos disponibles", color=[255, 165, 0, 255])
                    for _ in range(7):
                        dpg.add_text("--")
                return
            
            # Añadir filas de datos
            for crypto in datos:
                # Obtener datos
                posicion = crypto.get('posicion', '--')
                nombre = truncar_texto(crypto.get('nombre', 'N/A'), 25)
                precio = formatear_precio(crypto.get('precio', 0))
                
                cambio_1h_val = crypto.get('cambio_1h', 0)
                cambio_24h_val = crypto.get('cambio_24h', 0)
                cambio_7d_val = crypto.get('cambio_7d', 0)
                
                cambio_1h = formatear_porcentaje(cambio_1h_val)
                cambio_24h = formatear_porcentaje(cambio_24h_val)
                cambio_7d = formatear_porcentaje(cambio_7d_val)
                
                volumen = formatear_volumen(crypto.get('volumen_24h', 0))
                
                # Formatear cap. mercado
                cap_mercado_val = crypto.get('cap_mercado', 'N/A')
                cap_mercado = formatear_volumen(cap_mercado_val) if isinstance(cap_mercado_val, (int, float)) else 'N/A'
                
                # Formatear suministro
                suministro_val = crypto.get('suministro_circulante', 'N/A')
                suministro = f"{suministro_val:,.0f}" if isinstance(suministro_val, (int, float)) else 'N/A'
                
                # Colores para cambios porcentuales
                color_1h = obtener_color_cambio(cambio_1h_val)
                color_24h = obtener_color_cambio(cambio_24h_val)
                color_7d = obtener_color_cambio(cambio_7d_val)
                
                # Crear fila
                with dpg.table_row():
                    dpg.add_text(str(posicion))
                    dpg.add_text(nombre)
                    dpg.add_text(precio)
                    dpg.add_text(cambio_1h, color=color_1h)
                    dpg.add_text(cambio_24h, color=color_24h)
                    dpg.add_text(cambio_7d, color=color_7d)
                    dpg.add_text(volumen)
                    dpg.add_text(cap_mercado)
                    dpg.add_text(suministro)
                    
    except Exception as e:
        print(f"Error al crear tabla: {e}")

def actualizar_hora_actualizacion():
    """Actualiza la hora de última actualización"""
    try:
        if dpg.does_item_exist("txt_ultima_actualizacion"):
            hora_actual = datetime.now().strftime("%H:%M:%S")
            dpg.set_value("txt_ultima_actualizacion", f"Última act: {hora_actual}")
    except Exception as e:
        print(f"Error al actualizar hora: {e}")

def actualizar_estado_boton(actualizando):
    """Actualiza el estado del botón de actualización"""
    if dpg.does_item_exist("btn_actualizar"):
        texto = "Actualizando..." if actualizando else "Actualizar Datos"
        dpg.configure_item("btn_actualizar", label=texto, enabled=not actualizando)

def actualizar_estado_auto_actualizacion(habilitado):
    """Actualiza el estado visual del checkbox de actualización automática"""
    if dpg.does_item_exist("chk_auto_actualizacion"):
        dpg.set_value("chk_auto_actualizacion", habilitado)