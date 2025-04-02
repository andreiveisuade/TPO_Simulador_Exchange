"""
Configuración de temas y estilos visuales para la aplicación.
Este archivo centraliza todos los colores y estilos utilizados en la interfaz.
"""
import dearpygui.dearpygui as dpg

# Colores principales
COLOR_FONDO_PRINCIPAL = [21, 26, 48]        # Azul oscuro para el fondo principal
COLOR_FONDO_SECUNDARIO = [30, 36, 58]       # Azul oscuro ligeramente más claro para fondos secundarios
COLOR_TEXTO_PRIMARIO = [220, 220, 220]      # Texto claro casi blanco
COLOR_TEXTO_SECUNDARIO = [180, 180, 180]    # Texto gris claro para información secundaria
COLOR_BORDE = [45, 50, 70]                  # Bordes ligeramente más claros que el fondo

# Colores de acento
COLOR_ACENTO_PRIMARIO = [240, 185, 11]      # Dorado/amarillo para elementos destacados
COLOR_ACENTO_SECUNDARIO = [103, 111, 193]   # Púrpura azulado para elementos secundarios

# Colores para gráficos y datos
COLOR_POSITIVO = [14, 203, 129]             # Verde para valores positivos/ganancias
COLOR_NEGATIVO = [246, 70, 93]              # Rojo para valores negativos/pérdidas
COLOR_NEUTRO = [100, 100, 100]              # Gris para valores neutros
COLOR_ALERTA = [255, 152, 0]                # Naranja para alertas

# Colores de tabla
COLOR_CABECERA_TABLA = [38, 43, 65]         # Cabeceras de tablas
COLOR_FILA_PAR = [27, 32, 54]               # Filas pares en tablas
COLOR_FILA_IMPAR = [32, 37, 59]             # Filas impares en tablas
COLOR_FILA_HOVER = [40, 45, 70]             # Color al pasar el cursor sobre una fila
COLOR_SELECCION = [50, 55, 80]              # Color de fila seleccionada

# Estilos de componentes específicos
ESTILO_BOTON = {
    "color_normal": [32, 37, 59],
    "color_hover": [45, 50, 70],
    "color_activo": [50, 55, 80],
    "color_texto": [220, 220, 220],
    "redondeado": 5
}

def aplicar_tema_global():
    """
    Aplica el tema global a toda la aplicación.
    Configura los colores y estilos básicos para todos los componentes.
    """
    with dpg.theme() as tema_global:
        with dpg.theme_component(dpg.mvAll):
            # Colores básicos
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COLOR_FONDO_PRINCIPAL, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COLOR_FONDO_SECUNDARIO, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, COLOR_TEXTO_PRIMARIO, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, COLOR_BORDE, category=dpg.mvThemeCat_Core)
            
            # Botones
            dpg.add_theme_color(dpg.mvThemeCol_Button, ESTILO_BOTON["color_normal"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, ESTILO_BOTON["color_hover"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, ESTILO_BOTON["color_activo"], category=dpg.mvThemeCat_Core)
            
            # Cabeceras y tablas
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, COLOR_FILA_HOVER, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, COLOR_SELECCION, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, COLOR_CABECERA_TABLA, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, COLOR_FILA_PAR, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, COLOR_FILA_IMPAR, category=dpg.mvThemeCat_Core)
            
            # Frames y bordes
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, ESTILO_BOTON["redondeado"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 1, category=dpg.mvThemeCat_Core)
            
             # Cambiar a fuente monoespaciada (generalmente más grande)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 16, 4, category=dpg.mvThemeCat_Core)
            
            # Incrementar el espaciado de texto para que parezca más grande
            dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 6, 6, category=dpg.mvThemeCat_Core)
            
    return tema_global

def obtener_color_cambio(valor):
    """
    Retorna el color adecuado según el valor de cambio (positivo, negativo o neutro).
    
    Args:
        valor (float): Valor del cambio.
        
    Returns:
        list: Color RGBA.
    """
    if valor > 0:
        return COLOR_POSITIVO
    elif valor < 0:
        return COLOR_NEGATIVO
    else:
        return COLOR_NEUTRO

def tema_tabla_cotizaciones():
    """
    Crea y retorna un tema específico para la tabla de cotizaciones.
    """
    with dpg.theme() as tema:
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, COLOR_CABECERA_TABLA, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, COLOR_FILA_PAR, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, COLOR_FILA_IMPAR, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, COLOR_BORDE, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, COLOR_BORDE, category=dpg.mvThemeCat_Core)
            
    return tema

def tema_titulo():
    """
    Crea y retorna un tema para títulos con color destacado.
    """
    with dpg.theme() as tema:
        with dpg.theme_component(dpg.mvText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, COLOR_ACENTO_PRIMARIO, category=dpg.mvThemeCat_Core)
            
    return tema

def aplicar_tema_titulo(tag_item):
    """
    Aplica el tema de título a un elemento específico.
    
    Args:
        tag_item: Tag del elemento al que aplicar el tema.
    """
    tema = tema_titulo()
    dpg.bind_item_theme(tag_item, tema)