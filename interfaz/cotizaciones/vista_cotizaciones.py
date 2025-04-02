import dearpygui.dearpygui as dpg
from interfaz.temas import obtener_color_cambio, tema_tabla_cotizaciones

def crear_panel_cotizaciones(callback_actualizacion):
    """
    Crea el panel de cotizaciones dentro de la ventana principal.
    
    Args:
        callback_actualizacion: Función que se ejecutará al hacer clic en el botón de actualización.
    """
    try:
        print("Creando panel de cotizaciones...")
        
        # Panel de control
        with dpg.group(horizontal=True):
            dpg.add_text("Número de criptomonedas:")
            dpg.add_input_int(label="", default_value=20, min_value=1, max_value=100, tag="input_limite", width=100)
            dpg.add_button(label="Actualizar Datos", callback=callback_actualizacion, tag="btn_actualizar")
        
        dpg.add_spacer(height=10)
        
        # Tabla de cotizaciones con un tamaño definido y configuración mejorada
        with dpg.table(tag="tabla_cotizaciones", 
                       header_row=True, 
                       borders_innerH=True, 
                       borders_innerV=True, 
                       borders_outerH=True, 
                       borders_outerV=True, 
                       resizable=True, 
                       height=350, 
                       width=-1,
                       policy=dpg.mvTable_SizingFixedFit,  # Ajuste exacto para evitar movimiento
                       scrollY=True):  # Habilitar scroll vertical
            
            # Configurar columnas con ancho adecuado y alineadas correctamente
            dpg.add_table_column(label="#", width_fixed=True, width=60, init_width_or_weight=60)
            dpg.add_table_column(label="Nombre", width_fixed=True, width=180, init_width_or_weight=180)
            dpg.add_table_column(label="Precio", width_fixed=True, width=130, init_width_or_weight=130)
            dpg.add_table_column(label="1h%", width_fixed=True, width=90, init_width_or_weight=90)
            dpg.add_table_column(label="24h%", width_fixed=True, width=90, init_width_or_weight=90)
            dpg.add_table_column(label="7d%", width_fixed=True, width=90, init_width_or_weight=90)
            dpg.add_table_column(label="Volumen 24h", width_fixed=True, width=130, init_width_or_weight=130)
            dpg.add_table_column(label="Cap. Mercado", width_fixed=True, width=130, init_width_or_weight=130)
            dpg.add_table_column(label="Suministro", width_fixed=True, width=130, init_width_or_weight=130)
            
        # Aplicar tema específico a la tabla
        tema_tabla = tema_tabla_cotizaciones()
        dpg.bind_item_theme("tabla_cotizaciones", tema_tabla)
            
        print("Panel de cotizaciones creado con éxito")
            
    except Exception as e:
        print(f"Error al crear panel de cotizaciones: {e}")


def actualizar_tabla_ui(datos, formatear_precio, formatear_porcentaje, formatear_volumen):
    """
    Actualiza la tabla con los datos más recientes.
    
    Args:
        datos: Lista de diccionarios con datos de criptomonedas.
        formatear_precio: Función para formatear precios.
        formatear_porcentaje: Función para formatear porcentajes.
        formatear_volumen: Función para formatear volúmenes.
    """
    try:
        # Limpiar la tabla existente, pero solo las filas de datos reales
        children = dpg.get_item_children("tabla_cotizaciones", 1)  # 1 = contenido
        for child in children:
            if dpg.does_item_exist(child):  # Verificar que el item todavía existe
                alias = dpg.get_item_alias(child)
                if alias and alias.startswith("fila_datos_"):
                    dpg.delete_item(child)
        
        # Si no hay datos, mostrar mensaje
        if not datos:
            print("No hay datos para mostrar en la tabla")
            with dpg.table_row(parent="tabla_cotizaciones", tag="fila_sin_datos"):
                dpg.add_text("--")
                dpg.add_text("No hay datos disponibles", color=[255, 165, 0, 255])
                for _ in range(7):  # Para las columnas restantes
                    dpg.add_text("--")
            return
        
        # Añadir las filas de datos reales
        print(f"Añadiendo {len(datos)} filas a la tabla")
        for i, crypto in enumerate(datos):
            # Formatear los datos
            precio = formatear_precio(crypto['precio'])
            cambio_1h = formatear_porcentaje(crypto['cambio_1h'])
            cambio_24h = formatear_porcentaje(crypto['cambio_24h'])
            cambio_7d = formatear_porcentaje(crypto['cambio_7d'])
            volumen = formatear_volumen(crypto['volumen_24h'])
            
            # Formatear capitalización de mercado
            if isinstance(crypto['cap_mercado'], (int, float)):
                cap_mercado = formatear_volumen(crypto['cap_mercado'])
            else:
                cap_mercado = 'N/A'
                
            # Formatear suministro circulante
            if isinstance(crypto['suministro_circulante'], (int, float)):
                suministro = f"{crypto['suministro_circulante']:,.0f}"
            else:
                suministro = 'N/A'
            
            # Colores para los cambios porcentuales usando el sistema de temas
            color_1h = obtener_color_cambio(crypto['cambio_1h'])
            color_24h = obtener_color_cambio(crypto['cambio_24h'])
            color_7d = obtener_color_cambio(crypto['cambio_7d'])
            
            # Crear una fila con un tag único para poder eliminarla después
            with dpg.table_row(parent="tabla_cotizaciones", tag=f"fila_datos_{i}"):
                dpg.add_text(str(crypto['posicion']))
                dpg.add_text(crypto['nombre'])
                dpg.add_text(precio)
                dpg.add_text(cambio_1h, color=color_1h)
                dpg.add_text(cambio_24h, color=color_24h)
                dpg.add_text(cambio_7d, color=color_7d)
                dpg.add_text(volumen)
                dpg.add_text(cap_mercado)
                dpg.add_text(suministro)
    except Exception as e:
        print(f"Error al actualizar tabla: {e}")

def actualizar_estado_boton(actualizando):
    """
    Actualiza el estado del botón de actualización.
    
    Args:
        actualizando: Boolean que indica si se está actualizando o no.
    """
    texto = "Actualizando..." if actualizando else "Actualizar Datos"
    habilitado = not actualizando
    dpg.configure_item("btn_actualizar", label=texto, enabled=habilitado)