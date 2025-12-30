import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QFrame, QComboBox)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QPixmap, QIcon

# ==========================================
# CONFIGURACIÓN
# ==========================================
COLORS = {
    "bg_main": "#222222",
    "bg_dark": "#121212",
    "bg_panel": "#1c1c1c",
    "accent": "#8B0000",
    "text_main": "#E5E5E5",
    "text_dim": "#777777",
    "input_bg": "#222222"
}

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
# Intentamos varios candidatos: primero el recurso local dentro de `app/resources`,
# si no existe buscamos en `assets/img` en la raíz del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
candidate_logo_paths = [
    BASE_DIR / "resources" / "logo.png",
    PROJECT_ROOT / "assets" / "img" / "logo_with_no_background",
    PROJECT_ROOT / "assets" / "img" / "logo_with_white_background.jpeg",
]

def find_logo_path(candidates):
    for p in candidates:
        if p.exists():
            return str(p)
    # fallback al primero (aunque no exista) para facilitar debugging
    return str(candidates[0])

LOGO_PATH = find_logo_path(candidate_logo_paths)

# ==========================================
# COMPONENTES MODULARES
# ==========================================

class DownloadPage(QWidget):
    def __init__(self, title, placeholder):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Contenedor del Logo
        self.logo_label = QLabel()
        logo_path = LOGO_PATH
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                print(f"Warning: QPixmap no pudo cargar: {logo_path}")
                # Fallback si QPixmap falla
                self.logo_label.setText("V")
                self.logo_label.setFixedSize(140, 140)
                self.logo_label.setStyleSheet(f"background: {COLORS['accent']}; border-radius: 70px; color: white; font-size: 60px; font-weight: bold;")
                self.logo_label.setAlignment(Qt.AlignCenter)
        else:
            print(f"Warning: Logo no existe en: {logo_path}")
            # Fallback si no hay imagen: Círculo con texto
            self.logo_label.setText("V")
            self.logo_label.setFixedSize(140, 140)
            self.logo_label.setStyleSheet(f"background: {COLORS['accent']}; border-radius: 70px; color: white; font-size: 60px; font-weight: bold;")
            self.logo_label.setAlignment(Qt.AlignCenter)

        # Título debajo del logo
        title_label = QLabel(f"VideoLeech")
        title_label.setStyleSheet(f"color: {COLORS['text_main']}; font-size: 14px; margin-top: 10px;")

        # Campo de URL
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText(placeholder)
        self.input_url.setFixedWidth(520)
        self.input_url.setStyleSheet("QLineEdit { background-color: #3a3a3a; color: #ddd; }")

        # Botón de acción
        self.btn_action = QPushButton("⬇  Descargar")
        self.btn_action.setObjectName("BtnDescargar")
        self.btn_action.setFixedWidth(140)
        self.btn_action.setFixedHeight(40)

        # Construcción del layout
        layout.addStretch()
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.input_url, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_action, alignment=Qt.AlignCenter)
        layout.addStretch()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoLeech")
        self.resize(700, 450)
        self.setup_styles()
        self.init_ui()

    def setup_styles(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {COLORS['bg_main']}; }}
            
            #TopBar {{ 
                background-color: {COLORS['bg_dark']}; 
                max-height: 50px; 
            }}
            
            QPushButton#TabBtn {{ 
                background: transparent;
                border: none;
            }}
            QPushButton#TabActive {{ 
                background: transparent;
                border: none;
                border-bottom: 1px solid {COLORS['accent']}
            }}

            #Sidebar {{ 
                background-color: {COLORS['bg_panel']}; 
                border-right: 1px solid #252525;
            }}
            
            QLineEdit {{ 
                background-color: {COLORS['input_bg']}; border: 1px solid #333; 
                color: white; padding: 12px; border-radius: 4px; 
            }}
            
            #BtnDescargar {{ 
                background-color: {COLORS['accent']}; color: white; 
                padding: 12px; border-radius: 4px; font-weight: bold; font-size: 13px;
            }}
            #BtnDescargar:hover {{ background-color: #D30000; }}

            #IconBtn {{ background: transparent; color: white; font-size: 22px; border: none;}}
            
            QComboBox {{ 
                background-color: {COLORS['input_bg']}; color: white; 
                border: 1px solid #333; padding: 8px; border-radius: 4px;
            }}
        """)

    def init_ui(self):
        # Contenedor Raíz
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. BARRA SUPERIOR (NAV)
        # Botón de menú fuera del TopBar (arriba-izquierda). Se mostrará solo en Videos.
        self.btn_menu = QPushButton("≡")
        self.btn_menu.setObjectName("IconBtn")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.clicked.connect(self.toggle_sidebar)

        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        layout_top = QHBoxLayout(top_bar)

        # Pestañas
        tabs_widget = QWidget()
        layout_tabs = QHBoxLayout(tabs_widget)
        self.tab_v = QPushButton("Videos")
        self.tab_v.setObjectName("TabActive")
        self.tab_m = QPushButton("Música")
        self.tab_m.setObjectName("TabBtn")
        layout_tabs.addStretch()
        layout_tabs.addWidget(self.tab_v)
        layout_tabs.addWidget(self.tab_m)
        layout_tabs.addStretch()

        layout_top.addWidget(tabs_widget)

        # NOTA: la TopBar debe ser la barra superior completa.
        # Mostramos `top_bar` primero (barra completa) y luego una fila debajo
        # que contiene el botón hamburguesa alineado a la izquierda.
        menu_row = QWidget()
        menu_row_layout = QHBoxLayout(menu_row)
        menu_row_layout.setContentsMargins(8, 6, 8, 6)
        menu_row_layout.setSpacing(0)
        menu_row_layout.addWidget(self.btn_menu, alignment=Qt.AlignLeft)
        menu_row_layout.addStretch()

        # 2. CUERPO (SIDEBAR + CONTENIDO)
        body = QWidget()
        layout_body = QHBoxLayout(body)
        layout_body.setContentsMargins(0, 0, 0, 0)
        layout_body.setSpacing(0)

        # --- Sidebar ---
        # Left rail con iconos (siempre visibles)
        left_rail = QWidget()
        left_rail.setFixedWidth(48)
        left_layout = QVBoxLayout(left_rail)
        left_layout.setContentsMargins(6, 6, 6, 6)
        left_layout.setSpacing(8)
        left_layout.addStretch()
        self.btn_settings = QPushButton("⚙")
        self.btn_settings.setObjectName("IconBtn")
        self.btn_settings.setFixedSize(36, 36)
        self.btn_help = QPushButton("?")
        self.btn_help.setObjectName("IconBtn")
        self.btn_help.setFixedSize(36, 36)
        left_layout.addWidget(self.btn_settings, alignment=Qt.AlignLeft)
        left_layout.addWidget(self.btn_help, alignment=Qt.AlignLeft)
        left_layout.addSpacing(6)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(0) # Inicia oculta
        self.setup_sidebar_content()

        # --- Contenido ---
        self.content_stack = QStackedWidget()
        self.page_v = DownloadPage("MP4", "Pega el enlace del video aquí...")
        self.page_m = DownloadPage("MP3", "Pega el enlace de la canción aquí...")
        self.content_stack.addWidget(self.page_v)
        self.content_stack.addWidget(self.page_m)

        layout_body.addWidget(left_rail)
        layout_body.addWidget(self.sidebar)
        layout_body.addWidget(self.content_stack)

        # Unir todo: barra superior completa, luego fila del menú, luego el cuerpo
        main_layout.addWidget(top_bar)
        main_layout.addWidget(menu_row)
        main_layout.addWidget(body)

        # Conexiones
        self.tab_v.clicked.connect(lambda: self.switch_page(0))
        self.tab_m.clicked.connect(lambda: self.switch_page(1))

        # Asegurar estado inicial de la UI
        self.switch_page(0)

    def setup_sidebar_content(self):
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl = QLabel("CONFIGURACIÓN")
        lbl.setStyleSheet(f"color: {COLORS['text_dim']}; font-weight: bold; font-size: 11px;")
        
        self.quality_box = QComboBox()
        self.quality_box.addItems(["Máxima Calidad", "1080p", "720p", "480p"])
        
        layout.addWidget(lbl)
        layout.addWidget(self.quality_box)
        layout.addStretch()

    def toggle_sidebar(self):
        current_width = self.sidebar.width()
        new_width = 250 if current_width == 0 else 0
        
        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(350)
        self.anim.setStartValue(current_width)
        self.anim.setEndValue(new_width)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # Mostrar el menú hamburguesa sólo en la pestaña Videos (index 0)
        try:
            self.btn_menu.setVisible(index == 0)
        except AttributeError:
            pass
        self.tab_v.setObjectName("TabActive" if index == 0 else "TabBtn")
        self.tab_m.setObjectName("TabActive" if index == 1 else "TabBtn")
        # Refrescar estilos CSS (reaplicar hoja de estilos para que los
        # selectores por `objectName` se actualicen correctamente)
        self.tab_v.style().unpolish(self.tab_v)
        self.tab_v.style().polish(self.tab_v)
        self.tab_m.style().unpolish(self.tab_m)
        self.tab_m.style().polish(self.tab_m)
        # Forzar reaplicación global por si hace falta
        self.setStyleSheet(self.styleSheet())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())