import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QFrame, QComboBox)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QSettings
from PySide6.QtGui import QPixmap, QIcon


# ==========================================
# CONFIGURACIÓN
# ==========================================
COLORS = {
    "bg_main_dark": "#222222",
    "bg_bars_dark": "#1c1c1c",
    "main_color": "#8B0000",
    "secundary_color": "#463C3C",
    "accent": "#F03030",
    "texts_&_icons_dark": "#ffffff",
    "bg_main_light": "#E3E3E3",
    "bg_bars_light": "#F6F6F6",
    "texts_&_icons_light": "#000000",
    "placeholder_text": "#9E9A9A",
    "input_background_light": "#807373",
    "input_background_dark": "#463C3C",
}

if hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

PATHS = {
    "logo": str(BASE_DIR / "resources" / "logo.png"),
    "icon_menu_dark": str(BASE_DIR / "resources" / "menu_icon_dark.svg"),
    "icon_menu_light": str(BASE_DIR / "resources" / "menu_icon_light.svg"),
    "icon_close": str(BASE_DIR / "resources" / "menu_close_icon.svg"),
    "about_icon_dark": str(BASE_DIR / "resources" / "about_icon_dark.svg"),
    "about_icon_light": str(BASE_DIR / "resources" / "about_icon_light.svg"),
    "download_icon": str(BASE_DIR / "resources" / "download_icon.svg"),
    "dark_mode_icon": str(BASE_DIR / "resources" / "dark_mode_icon.svg"),
    "light_mode_icon": str(BASE_DIR / "resources" / "light_mode_icon.svg"),
    "logo_application": str(BASE_DIR / "resources" / "logo_application.svg"),
}

# ==========================================
# COMPONENTES MODULARES
# ==========================================

class DownloadPage(QWidget):
    def __init__(self, title, placeholder):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel()
        logo_path = PATHS["logo"]
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                print(f"Warning: QPixmap no pudo cargar: {logo_path}")
                self.logo_label.setText("V")
                self.logo_label.setFixedSize(140, 140)
                self.logo_label.setStyleSheet(f"background: {COLORS['accent']}; border-radius: 70px; color: white; font-size: 60px; font-weight: bold;")
                self.logo_label.setAlignment(Qt.AlignCenter)
        else:
            print(f"Warning: Logo no existe en: {logo_path}")
            self.logo_label.setText("V")
            self.logo_label.setFixedSize(140, 140)
            self.logo_label.setStyleSheet(f"background: {COLORS['accent']}; border-radius: 70px; color: white; font-size: 60px; font-weight: bold;")
            self.logo_label.setAlignment(Qt.AlignCenter)
        
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText(placeholder)
        self.input_line.setFixedWidth(450)
        self.input_line.setStyleSheet(f"""background-color: {COLORS['secundary_color']}; color: {COLORS['placeholder_text']};""")
        
        self.btn_action = QPushButton("Download")
        self.btn_action.setObjectName("btn_download")
        icon_download = QIcon(PATHS["download_icon"])
        self.btn_action.setIcon(icon_download)
        self.btn_action.setIconSize(QSize(20, 20))
        self.btn_action.setFixedWidth(150)
        self.btn_action.setFixedHeight(40)
        
        
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.input_line)
        layout.addSpacing(30)
        layout.addWidget(self.btn_action, alignment=Qt.AlignCenter)
        layout.addStretch()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoLeech")
        self.setWindowIcon(QIcon(PATHS["logo_application"]))
        self.resize(800, 600)
        # Construir UI primero, luego aplicar tema guardado (porque apply_theme
        # modifica iconos de botones que se crean en init_ui)
        self.init_ui()
        # Persistencia del tema
        self.settings = QSettings("VideoLeech", "VideoLeech")
        saved = self.settings.value("theme", "dark")
        self.apply_theme(saved)
        
    def setup_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_main_dark']};
            }}
            QPushButton#btn_download {{
                background-color: {COLORS['main_color']};
                color: {COLORS['texts_&_icons_dark']};
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }}
            QPushButton{{
                background-color: transparent;
                color: {COLORS['texts_&_icons_dark']};
                border: none;
                font-size: 20px;
            }}
            QPushButton#TabBtn:hover {{
                background-color: transparent;
                color: {COLORS['texts_&_icons_dark']};
                border: none;
                border-bottom: 1px solid {COLORS['accent']};
            }}
            #TopBar {{
                background-color: {COLORS['bg_bars_dark']};
                }}
            QPushButton#btn_download:hover {{
                background-color: {COLORS['accent']};
            }}
            QPushButton#TabActive {{
                border-bottom: 1px solid {COLORS['accent']};
            }}
            QLineEdit {{
                padding: 8px;
                color: {COLORS['texts_&_icons_dark']};
                border-radius: 5px;
                background-color: {COLORS['input_background_dark']};
            }}
            #Sidebar {{
                background-color: {COLORS['bg_bars_dark']};
            }}
            QPushButton#IconBtn:hover {{
                background-color: {COLORS['accent']};
            }}
        """)

    def apply_theme(self, theme: str):
        """Aplicar tema 'dark' o 'light' y guardar la preferencia."""
        self.theme = theme
        if theme == "light":
            bg_main = COLORS['bg_main_light']
            bg_bars = COLORS['bg_bars_light']
            text = COLORS['texts_&_icons_light']
            input_bg = COLORS['input_background_light']
            toggle_icon = PATHS.get('dark_mode_icon', PATHS.get('light_mode_icon'))
        else:
            bg_main = COLORS['bg_main_dark']
            bg_bars = COLORS['bg_bars_dark']
            text = COLORS['texts_&_icons_dark']
            input_bg = COLORS['secundary_color']
            toggle_icon = PATHS.get('light_mode_icon', PATHS.get('dark_mode_icon'))

        qss = f"""
            QMainWindow {{ background-color: {bg_main}; }}
            
            QPushButton{{ 
            background-color: transparent; 
            color: {text}; border: none; 
            font-size: 20px; 
            }}
            
            QPushButton#btn_download {{
                background-color: {COLORS['main_color']};
                color: {COLORS['texts_&_icons_dark']};
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }}
            
            QPushButton#btn_download:hover {{
                background-color: {COLORS['accent']};
            }}
            
            QPushButton#TabBtn:hover {{ 
            background-color: transparent; 
            color: {text}; 
            border: none; 
            border-bottom: 1px solid {COLORS['accent']}; 
            }}
            
            #TopBar {{ background-color: {bg_bars}; }}
            
            QPushButton#btn_download:hover {{ background-color: {COLORS['accent']}; }}
            
            QPushButton#TabActive {{ border-bottom: 1px solid {COLORS['accent']}; }}
            
            QLineEdit {{ 
            padding: 8px; 
            color: {text}; 
            border-radius: 5px; 
            background-color: {input_bg}; 
            }}
            
            #Sidebar {{ background-color: {bg_bars}; }}
            
            QPushButton#IconBtn:hover {{ background-color: {COLORS['accent']}; }}
        """
        self.setStyleSheet(qss)

        # Actualizar icono del toggle si ya existe
        try:
            self.btn_dark_or_light_mode.setIcon(QIcon(toggle_icon))
        except Exception:
            pass

        # Actualizar otros iconos según el tema
        try:
            if theme == 'light':
                self.btn_menu.setIcon(QIcon(PATHS.get('icon_menu_light', PATHS.get('icon_menu_dark'))))
                self.btn_about.setIcon(QIcon(PATHS.get('about_icon_light', PATHS.get('about_icon_dark'))))
            else:
                self.btn_menu.setIcon(QIcon(PATHS.get('icon_menu_dark', PATHS.get('icon_menu_light'))))
                self.btn_about.setIcon(QIcon(PATHS.get('about_icon_dark', PATHS.get('about_icon_light'))))
        except Exception:
            pass

        # Guardar preferencia
        try:
            self.settings.setValue('theme', theme)
        except Exception:
            pass

    def toggle_theme(self):
        new = 'light' if getattr(self, 'theme', 'dark') == 'dark' else 'dark'
        self.apply_theme(new)
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.btn_menu = QPushButton()
        self.btn_menu.setObjectName("IconBtn")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.setIcon(QIcon(PATHS["icon_menu_dark"]))
        self.btn_menu.setIconSize(QSize(24, 24))
        self.btn_menu.setFixedSize(40, 40)
        
        self.btn_menu.clicked.connect(self.toggle_sidebar)

        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        layout_top = QHBoxLayout(top_bar)
        
        tabs_widget = QWidget()
        layout_tabs = QHBoxLayout(tabs_widget)
        self.tabs_video = QPushButton("Video")
        self.tabs_video.setObjectName("TabBtn")
        
        self.tabs_music = QPushButton("Music")
        self.tabs_music.setObjectName("TabBtn")
        
        layout_tabs.addStretch()
        layout_tabs.addWidget(self.tabs_video)
        layout_tabs.addSpacing(20)
        layout_tabs.addWidget(self.tabs_music)
        layout_tabs.addStretch()
        
        layout_top.addWidget(tabs_widget)
        
        menu_row = QWidget()
        menu_row_layout = QHBoxLayout(menu_row)
        menu_row_layout.setContentsMargins(0, 0, 0, 0)
        menu_row_layout.setSpacing(0)
        menu_row_layout.addWidget(self.btn_menu, alignment=Qt.AlignLeft)
        menu_row_layout.addStretch()
        
        body = QWidget()
        layout_body = QHBoxLayout(body)
        layout_body.setContentsMargins(0, 0, 0, 0)
        layout_body.setSpacing(0)
        
        left_rail = QWidget()
        left_rail.setFixedWidth(48)
        left_layout = QVBoxLayout(left_rail)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.addStretch()
        
        self.btn_dark_or_light_mode = QPushButton()
        self.btn_dark_or_light_mode.setObjectName("IconBtn")
        self.btn_dark_or_light_mode.setIcon(QIcon(PATHS["light_mode_icon"]))
        self.btn_dark_or_light_mode.setIconSize(QSize(24, 24))
        self.btn_dark_or_light_mode.setFixedSize(36, 36)
        self.btn_dark_or_light_mode.clicked.connect(self.toggle_theme)
        
        
        self.btn_about = QPushButton()
        self.btn_about.setObjectName("IconBtn")
        self.btn_about.setIcon(QIcon(PATHS["about_icon_light"]))
        self.btn_about.setIconSize(QSize(24, 24))
        self.btn_about.setFixedSize(36, 36)
        

        left_layout.addWidget(self.btn_dark_or_light_mode, alignment=Qt.AlignLeft)
        left_layout.addWidget(self.btn_about, alignment=Qt.AlignLeft)
        left_layout.addSpacing(0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(0)
        self.setup_sidebar_content()
        
        self.content_stack = QStackedWidget()
        self.page_video = DownloadPage("MP4", "Pega el enlace del video aquí...")
        self.page_music = DownloadPage("MP3", "Pega el enlace de la canción aquí...")
        self.content_stack.addWidget(self.page_video)
        self.content_stack.addWidget(self.page_music)

        layout_body.addWidget(left_rail)
        layout_body.addWidget(self.sidebar)
        layout_body.addWidget(self.content_stack)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(menu_row)
        main_layout.addWidget(body)

        self.tabs_video.clicked.connect(lambda: self.switch_page(0))
        self.tabs_music.clicked.connect(lambda: self.switch_page(1))

        # Asegurar estado inicial de la UI
        self.switch_page(0)
        
    def toggle_sidebar(self):
        current_width = self.sidebar.width()
        new_width = 250 if current_width == 0 else 0
        
        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(350)
        self.anim.setStartValue(current_width)
        self.anim.setEndValue(new_width)
        self.anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.anim.start()
    
    def setup_sidebar_content(self):
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl = QLabel("CONFIGURACIÓN")
        lbl.setStyleSheet(f"color: {COLORS['texts_&_icons_dark']}; font-weight: bold; font-size: 11px;")
        
        self.quality_box = QComboBox()
        self.quality_box.addItems(["Máxima Calidad", "1080p", "720p", "480p"])
        
        layout.addWidget(lbl)
        layout.addWidget(self.quality_box)
        layout.addStretch()
    
    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        try:
            self.btn_menu.setVisible(index == 0)
        except AttributeError:
            pass
        self.tabs_video.setObjectName("TabActive" if index == 0 else "TabBtn")
        self.tabs_music.setObjectName("TabActive" if index == 1 else "TabBtn")
        self.tabs_video.style().unpolish(self.tabs_video)
        self.tabs_video.style().polish(self.tabs_video)
        self.tabs_music.style().unpolish(self.tabs_music)
        self.tabs_music.style().polish(self.tabs_music)
        self.setStyleSheet(self.styleSheet())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())