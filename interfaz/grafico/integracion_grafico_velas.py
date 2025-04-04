"""
Integración - Código para integrar el gráfico de velas en la aplicación principal.
Versión que renderiza los gráficos directamente sin guardar imágenes.
"""

import os
import dearpygui.dearpygui as dpg
# Importar el controlador directo en lugar del basado en imágenes
import interfaz.grafico.controlador_velas as controlador
import traceback

def configurar_ventana_grafico():
    """
    Configura los controles de gráfico en la ventana existente.
    Debe ser llamada después de crear la ventana principal.
    """
    # Inicializar el controlador
    controlador.inicializar()
    
    # Obtener listas para los selectores
    pares = controlador.obtener_lista_pares(limite=15)
    intervalos = controlador.obtener_lista_intervalos()
    
    # Configurar valores por defecto
    par_default = "BTCUSDT" if "BTCUSDT" in pares else pares[0] if pares else ""
    intervalo_default = "1h"
    
    # La ventana ya existe, solo configuramos sus contenidos
    parent = "ventana_grafico" if dpg.does_item_exist("ventana_grafico") else None
    if parent:
        # Limpiar texto provisional si existe
        for item in dpg.get_item_children(parent)[1]:
            if dpg.get_item_label(item) == "Información del gráfico (en desarrollo)":
                dpg.delete_item(item)
        
        # Área de controles
        with dpg.group(horizontal=True, parent=parent):
            # Selector de par
            dpg.add_combo(
                items=pares,
                default_value=par_default,
                width=150,
                tag="selector_par",
                callback=on_cambio_parametros
            )
            
            # Selector de intervalo
            dpg.add_combo(
                items=intervalos,
                default_value=intervalo_default,
                width=100,
                tag="selector_intervalo",
                callback=on_cambio_parametros
            )
            
            # Checkbox para medias móviles
            dpg.add_checkbox(
                label="MA(20)",
                tag="ma_20_check", 
                default_value=True,
                callback=on_cambio_parametros
            )
            
            dpg.add_checkbox(
                label="MA(50)",
                tag="ma_50_check", 
                default_value=False,
                callback=on_cambio_parametros
            )
            
            dpg.add_checkbox(
                label="MA(200)",
                tag="ma_200_check", 
                default_value=False,
                callback=on_cambio_parametros
            )
            
            # Botón de actualizar (ahora opcional ya que la actualización puede ser automática)
            dpg.add_button(
                label="Actualizar",
                callback=actualizar_grafico_callback,
                tag="boton_actualizar"
            )
        
        # Área para mostrar el gráfico
        with dpg.group(tag="area_grafico", parent=parent):
            dpg.add_text("Cargando gráfico...", tag="texto_cargando")
        
        # Generar gráfico inicial
        actualizar_grafico_callback()
    else:
        print("Error: La ventana 'ventana_grafico' no existe. Asegúrate de crearla primero.")

def on_cambio_parametros(sender, app_data):
    """
    Callback para cuando cambia cualquier parámetro del gráfico.
    Opcionalmente puede actualizar automáticamente el gráfico.
    """
    # Descomenta la línea siguiente si quieres actualización automática al cambiar parámetros
    # actualizar_grafico_callback()
    pass

def actualizar_grafico_callback():
    """
    Callback para actualizar el gráfico cuando se presiona el botón o cambian los selectores.
    """
    try:
        # Obtener valores seleccionados
        par = dpg.get_value("selector_par")
        intervalo = dpg.get_value("selector_intervalo")
        
        # Verificar que los valores son válidos
        if not par or not intervalo:
            print("Error: Par o intervalo no válidos")
            par = par or "BTCUSDT"
            intervalo = intervalo or "1h"
            print(f"Usando valores por defecto: {par}, {intervalo}")
        
        # Verificar qué medias móviles están seleccionadas
        periodos_ma = []
        try:
            if dpg.get_value("ma_20_check"):
                periodos_ma.append(20)
            if dpg.get_value("ma_50_check"):
                periodos_ma.append(50)
            if dpg.get_value("ma_200_check"):
                periodos_ma.append(200)
        except:
            # Si hay algún error al obtener valores de los checkboxes
            print("Advertencia: Error al leer selección de indicadores, usando valores predeterminados")
            periodos_ma = [20]  # Valor por defecto
        
        # Mostrar mensaje de carga
        if dpg.does_item_exist("texto_cargando"):
            dpg.configure_item("texto_cargando", show=True)
            dpg.set_value("texto_cargando", f"Cargando gráfico de {par} ({intervalo})...")
        
        print(f"Generando gráfico para {par} con intervalo {intervalo}")
        
        # Actualizar el gráfico directamente (sin guardar imágenes)
        exito = controlador.actualizar_grafico_velas(
            par, 
            intervalo, 
            periodos_ma=periodos_ma if periodos_ma else None,
            parent="area_grafico"
        )
        
        # Ocultar mensaje de carga si se actualizó correctamente
        if exito and dpg.does_item_exist("texto_cargando"):
            dpg.configure_item("texto_cargando", show=False)
        elif not exito and dpg.does_item_exist("texto_cargando"):
            # Mostrar mensaje de error
            dpg.set_value("texto_cargando", f"Error al cargar el gráfico de {par} ({intervalo})")
            dpg.configure_item("texto_cargando", color=[255, 100, 100, 255])
            
    except Exception as e:
        print(f"Error en actualizar_grafico_callback: {e}")
        traceback.print_exc()
        if dpg.does_item_exist("texto_cargando"):
            dpg.set_value("texto_cargando", f"Error inesperado: {str(e)}")
            dpg.configure_item("texto_cargando", color=[255, 100, 100, 255])

def ejemplo_uso_independiente():
    """
    Ejemplo de cómo usar este módulo de forma independiente (para pruebas).
    """
    # Configuración de DearPyGui
    dpg.create_context()
    dpg.create_viewport(title="Ejemplo Gráfico de Velas Directo", width=1000, height=800)
    
    # Crear ventana principal
    with dpg.window(label="Principal", width=1000, height=800, tag="ventana_principal"):
        dpg.add_text("Demostración de Gráfico de Velas (Renderizado Directo)")
    
    # Crear ventana de gráfico
    with dpg.window(label="Grafico", width=850, height=688, pos=(50, 50), tag="ventana_grafico"):
        dpg.add_text("GRÁFICO DE VELAS", tag="titulo_grafico")
        dpg.add_separator()
    
    # Configurar ventana de gráfico
    configurar_ventana_grafico()
    
    # Iniciar la aplicación
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

# Si se ejecuta este archivo directamente, mostrar ejemplo
if __name__ == "__main__":
    ejemplo_uso_independiente()