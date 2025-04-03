import dearpygui.dearpygui as dpg
from interfaz.temas import obtener_color_cambio, tema_tabla_cotizaciones
from datetime import datetime

def truncar_texto(texto, longitud_maxima=25):
    """Trunca un texto si excede la longitud máxima"""
    if isinstance(texto, str) and len(texto) > longitud_maxima:
        return texto[:longitud_maxima-3] + "..."
    return texto

def crear_panel_cotizaciones(callback_actualizacion, callback_auto_actualizacion=None):
    """
    Crea el panel de cotizaciones dentro de la ventana principal.
    """
    try:
        print("Creando panel de cotizaciones...")
        
        # Panel de control (usando grupos en lugar de add_same_line)
        with dpg.group(horizontal=True):
            dpg.add_text("Número de criptomonedas:")
            dpg.add_input_int(label="", default_value=20, min_value=1, max_value=100, tag="input_limite", width=100)
            dpg.add_button(label="Actualizar Datos", callback=callback_actualizacion, tag="btn_actualizar")
        
        # Segundo grupo para actualización automática
        if callback_auto_actualizacion:
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label="Actualización automática (30s)", 
                    default_value=True,
                    callback=callback_auto_actualizacion, 
                    tag="chk_auto_actualizacion"
                )
                dpg.add_text("Última act: --:--:--", tag="txt_ultima_actualizacion")
        
        dpg.add_spacer(height=10)
        dpg.add_child_window(tag="contenedor_tabla", autosize_x=True, height=350)

        if dpg.does_item_exist("tabla_cotizaciones"):
            dpg.delete_item("tabla_cotizaciones")

        with dpg.table(tag="tabla_cotizaciones",
                       parent="contenedor_tabla",
                       header_row=True,
                       borders_innerH=True,
                       borders_innerV=True,
                       borders_outerH=True,
                       borders_outerV=True,
                       resizable=True,
                       height=320,
                       width=1800,
                       policy=dpg.mvTable_SizingFixedFit,
                       scrollX=True,
                       scrollY=True):
            dpg.add_table_column(label="#", width=90)
            dpg.add_table_column(label="Nombre", width=960)
            dpg.add_table_column(label="Precio", width=300)
            dpg.add_table_column(label="1h%", width=200)
            dpg.add_table_column(label="24h%", width=200)
            dpg.add_table_column(label="7d%", width=200)
            dpg.add_table_column(label="Volumen 24h", width=120)
            dpg.add_table_column(label="Cap. Mercado", width=130)
            dpg.add_table_column(label="Suministro", width=130)

        print("Panel de cotizaciones creado con éxito")
            
    except Exception as e:
        print(f"Error al crear panel de cotizaciones: {e}")

def actualizar_tabla_ui(datos, formatear_precio, formatear_porcentaje, formatear_volumen):
    """
    Actualiza la tabla con los datos más recientes.
    """
    try:
        # Verificar primero si la tabla existe
        if not dpg.does_item_exist("tabla_cotizaciones"):
            print("Error: La tabla no existe")
            return
        
        # Limpiar tabla completamente
        try:
            children = dpg.get_item_children("tabla_cotizaciones", 1)  # 1 = contenido
            if children:
                for child in children:
                    if dpg.does_item_exist(child):
                        dpg.delete_item(child)
        except Exception as e:
            print(f"Advertencia al limpiar tabla: {e}")
        
        # Si no hay datos, mostrar mensaje
        if not datos:
            print("No hay datos para mostrar en la tabla")
            with dpg.table_row(parent="tabla_cotizaciones"):
                dpg.add_text("--")
                dpg.add_text("No hay datos disponibles", color=[255, 165, 0, 255])
                for _ in range(7):
                    dpg.add_text("--")
            return
        
        # Añadir las filas de datos reales
        print(f"Añadiendo {len(datos)} filas a la tabla")
        for i, crypto in enumerate(datos):
            # Evitar errores con datos faltantes
            posicion = crypto.get('posicion', i+1)
            nombre = crypto.get('nombre', 'N/A')
            precio_val = crypto.get('precio', 0)
            cambio_1h_val = crypto.get('cambio_1h', 0)
            cambio_24h_val = crypto.get('cambio_24h', 0)
            cambio_7d_val = crypto.get('cambio_7d', 0)
            volumen_val = crypto.get('volumen_24h', 0)
            cap_mercado_val = crypto.get('cap_mercado', 'N/A')
            suministro_val = crypto.get('suministro_circulante', 'N/A')
            
            # Formatear los datos
            precio = formatear_precio(precio_val)
            cambio_1h = formatear_porcentaje(cambio_1h_val)
            cambio_24h = formatear_porcentaje(cambio_24h_val)
            cambio_7d = formatear_porcentaje(cambio_7d_val)
            volumen = formatear_volumen(volumen_val)
            
            # Formatear capitalización de mercado
            if isinstance(cap_mercado_val, (int, float)):
                cap_mercado = formatear_volumen(cap_mercado_val)
            else:
                cap_mercado = 'N/A'
                
            # Formatear suministro circulante
            if isinstance(suministro_val, (int, float)):
                suministro = f"{suministro_val:,.0f}"
            else:
                suministro = 'N/A'
            
            # Colores para los cambios porcentuales
            color_1h = obtener_color_cambio(cambio_1h_val)
            color_24h = obtener_color_cambio(cambio_24h_val)
            color_7d = obtener_color_cambio(cambio_7d_val)
            
            # Crear fila
            try:
                with dpg.table_row(parent="tabla_cotizaciones"):
                    dpg.add_text(str(posicion))  # Columna #
                    nombre_mostrar = truncar_texto(nombre, 25)
                    dpg.add_text(nombre_mostrar)         # Columna Nombre
                    dpg.add_text(precio)         # Columna Precio
                    dpg.add_text(cambio_1h, color=color_1h)   # Columna 1h%
                    dpg.add_text(cambio_24h, color=color_24h) # Columna 24h%
                    dpg.add_text(cambio_7d, color=color_7d)   # Columna 7d%
                    dpg.add_text(volumen)        # Columna Volumen 24h
                    dpg.add_text(cap_mercado)    # Columna Cap. Mercado
                    dpg.add_text(suministro)     # Columna Suministro
            except Exception as e:
                print(f"Error al añadir fila {i}: {e}")
        
        # Actualizar hora de la última actualización
        try:
            if dpg.does_item_exist("txt_ultima_actualizacion"):
                hora_actual = datetime.now().strftime("%H:%M:%S")
                dpg.set_value("txt_ultima_actualizacion", f"Última act: {hora_actual}")
        except Exception as e:
            print(f"Error al actualizar hora: {e}")
            
    except Exception as e:
        print(f"Error general al actualizar tabla: {e}")

def actualizar_estado_boton(actualizando):
    """
    Actualiza el estado del botón de actualización.
    """
    if dpg.does_item_exist("btn_actualizar"):
        texto = "Actualizando..." if actualizando else "Actualizar Datos"
        habilitado = not actualizando
        dpg.configure_item("btn_actualizar", label=texto, enabled=habilitado)

def actualizar_estado_auto_actualizacion(habilitado):
    """
    Actualiza el estado visual del checkbox de actualización automática.
    """
    if dpg.does_item_exist("chk_auto_actualizacion"):
        dpg.set_value("chk_auto_actualizacion", habilitado)