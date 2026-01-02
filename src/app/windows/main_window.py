import sys
from pathlib import Path
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QFrame, QComboBox, QFileDialog)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QSettings, QThread
from PySide6.QtGui import QPixmap, QIcon
from .about_window import AboutWindow
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from app.styles import COLORS, PATHS
from app.main import download_video, download_audio, default_download_dir
from app.core.downloader import DownloadWorker

home = Path.home()
downloads_path = Path(default_download_dir())

if not downloads_path.exists():
    downloads_path = home

# ==========================================
# MODULARS COMPONENTS
# ==========================================

class DownloadPage(QWidget):
    def __init__(self, title, placeholder, is_video=True):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.is_video = is_video

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
        
        self.btn_action = QPushButton("Download")
        self.btn_action.setObjectName("btn_download")
        icon_download = QIcon(PATHS["download_icon"])
        self.btn_action.setIcon(icon_download)
        self.btn_action.setIconSize(QSize(20, 20))
        self.btn_action.setFixedWidth(150)
        self.btn_action.setFixedHeight(40)
        self.btn_action.clicked.connect(self.handle_download)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)


        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.input_line)
        layout.addSpacing(30)
        layout.addWidget(self.btn_action, alignment=Qt.AlignCenter)
        layout.addStretch()
        
    def handle_download(self):
        url = self.input_line.text()
        parent = self.parent()
        download_dir = getattr(parent, 'dir_input', None)
        if download_dir:
            download_dir = parent.dir_input.text()
        if not download_dir:
            download_dir = str(default_download_dir())
        try:
            mw = self.window()
            if hasattr(mw, 'start_download'):
                mw.start_download(url=url, is_video=self.is_video, quality=getattr(parent, 'quality_box', None) and parent.quality_box.currentText() or None, download_dir=download_dir)
            else:
                self.btn_action.setText("Downloading...")
                self.status_label.setText("")
                QApplication.processEvents()
                success = False
                if self.is_video:
                    success = download_video(url, quality=None, download_dir=download_dir)
                else:
                    success = download_audio(url, download_dir=download_dir)
                if success:
                    carpeta = download_dir if download_dir else str(default_download_dir())
                    self.status_label.setText(f"Downloaded in {carpeta}")
                else:
                    self.status_label.setText("Error during download")
                self.btn_action.setText("Download")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            self.btn_action.setText("Download")


        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoLeech")
        self.setWindowIcon(QIcon(PATHS["logo_application"]))
        self.resize(700, 450)
        self.init_ui()
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
                background-color: {COLORS['input_bg_dark']};
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
            input_bg = COLORS['input_bg_light']
            toggle_icon = PATHS.get('dark_mode_icon', PATHS.get('light_mode_icon'))
        else:
            bg_main = COLORS['bg_main_dark']
            bg_bars = COLORS['bg_bars_dark']
            text = COLORS['texts_&_icons_dark']
            input_bg = COLORS['input_bg_dark']
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
            background-color: {COLORS['input_bg_light'] if theme == 'light' else COLORS['input_bg_dark']}; 
            }}

            QLineEdit::placeholder {{ color: {COLORS['placeholder_text']}; }}

            /* Asegurar que el texto dentro del sidebar sea legible en ambos temas */
            #Sidebar, #Sidebar * {{ color: {text}; }}
            #Sidebar QComboBox {{ background-color: {bg_bars}; color: {text}; }}
            #Sidebar QComboBox QAbstractItemView {{ background-color: {bg_bars}; color: {text}; selection-background-color: {COLORS['accent']}; }}
            
            
            #Sidebar {{ background-color: {bg_bars}; }}
            
            QPushButton#IconBtn:hover {{ background-color: {COLORS['accent']}; }}
            
            Qlabel#SidebarTitle-Config {{
                font-weight: bold;
                font-size: 11px;
                color: {COLORS['texts_&_icons_dark'] if theme == 'dark' else COLORS['texts_&_icons_light']};
            }}
        """
        self.setStyleSheet(qss)

        try:
            self.btn_dark_or_light_mode.setIcon(QIcon(toggle_icon))
        except Exception:
            pass

        try:
            if theme == 'light':
                self.btn_menu.setIcon(QIcon(PATHS.get('icon_menu_light', PATHS.get('icon_menu_dark'))))
                self.btn_about.setIcon(QIcon(PATHS.get('about_icon_light', PATHS.get('about_icon_dark'))))
            else:
                self.btn_menu.setIcon(QIcon(PATHS.get('icon_menu_dark', PATHS.get('icon_menu_light'))))
                self.btn_about.setIcon(QIcon(PATHS.get('about_icon_dark', PATHS.get('about_icon_light'))))
        except Exception:
            pass

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
        self.btn_about.clicked.connect(self.open_about)

        left_layout.addWidget(self.btn_dark_or_light_mode, alignment=Qt.AlignLeft)
        left_layout.addWidget(self.btn_about, alignment=Qt.AlignLeft)
        left_layout.addSpacing(0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(0)
        self.setup_sidebar_content()
        
        self.content_stack = QStackedWidget()
        self.page_video = DownloadPage("MP4", "Paste the url of the video here...", is_video=True)
        self.page_music = DownloadPage("MP3", "Paste the url of the song here...", is_video=False)
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
        
        lbl = QLabel("Configuration")
        lbl.setObjectName("SidebarTitle-Config")
        
        self.quality_box = QComboBox()
        self.quality_box.addItems(["Maximum Quality", "1080p", "720p", "480p"])
        


        layout.addWidget(lbl)
        layout.addWidget(self.quality_box)
        layout.addSpacing(20)
        layout.addStretch()
    
    def select_download_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona carpeta de descarga", self.dir_input.text())
        if folder:
            self.dir_input.setText(folder)

    def start_download(self, url: str, is_video: bool = True, quality: str | None = None, download_dir: str | None = None):
        """Crear QThread y DownloadWorker para ejecutar la descarga en background."""
        if not url:
            widget = self.content_stack.currentWidget()
            widget.status_label.setText("Please provide a URL")
            return

        widget = self.content_stack.currentWidget()
        try:
            widget.btn_action.setText("Downloading...")
        except Exception:
            pass

        if not download_dir:
            download_dir = str(default_download_dir())

        thread = QThread()
        worker = DownloadWorker(url=url, is_video=is_video, quality=quality, download_dir=download_dir)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.progress.connect(lambda msg: widget.status_label.setText(msg))

        def _on_finished_ui(success: bool):
            try:
                widget.btn_action.setText("Download")
            except Exception:
                pass
            if success:
                widget.status_label.setText("Download completed")
            else:
                widget.status_label.setText("Download failed")

        worker.finished.connect(_on_finished_ui)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        self._dl_thread = thread
        self._dl_worker = worker

        thread.start()
    
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

        try:
            if index != 0 and self.sidebar.width() > 0:
                self.sidebar_anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
                self.sidebar_anim.setDuration(250)
                self.sidebar_anim.setStartValue(self.sidebar.width())
                self.sidebar_anim.setEndValue(0)
                self.sidebar_anim.setEasingCurve(QEasingCurve.InOutQuart)
                self.sidebar_anim.start()
        except Exception:
            try:
                self.sidebar.setFixedWidth(0)
            except Exception:
                pass

    def open_about(self):
        if not hasattr(self, "about_window") or self.about_window is None:
            self.about_window = AboutWindow(parent=self)
            self.about_window.setAttribute(Qt.WA_DeleteOnClose, False)
        try:
            if hasattr(self.about_window, 'apply_theme'):
                self.about_window.apply_theme(getattr(self, "theme", "dark"))
        except Exception:
            pass
        self.about_window.setWindowModality(Qt.ApplicationModal)
        self.about_window.show()
        self.about_window.raise_()
        self.about_window.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())