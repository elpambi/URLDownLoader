import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget, QLineEdit)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoLeech Multisección")
        self.resize(700, 500)

        # --- 1. ESTILO QSS (Look Moderno) ---
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; }
            #Sidebar { background-color: #111; border-right: 1px solid #333; }
            #Contenido { background-color: #1a1a1a; }
            QLabel { color: white; font-family: 'Segoe UI'; }
            QPushButton { 
                background-color: transparent; color: #888; 
                padding: 15px; border: none; text-align: left; font-size: 14px;
            }
            QPushButton:hover { background-color: #222; color: white; }
            QPushButton#Active { color: #5592E3; font-weight: bold; border-left: 3px solid #5592E3; }
            QLineEdit { background: #252525; border: 1px solid #333; color: white; padding: 8px; }
        """)

        # --- 2. LAYOUT PRINCIPAL (Horizontal) ---
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- 3. BARRA LATERAL (Menú) ---
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        self.btn_video = QPushButton(" 🎬 Vídeos (MP4)")
        self.btn_video.setObjectName("Active") # Iniciamos con este activo
        self.btn_musica = QPushButton(" 🎵 Música (MP3)")
        
        sidebar_layout.addWidget(QLabel("VideoLeech"))
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.btn_video)
        sidebar_layout.addWidget(self.btn_musica)
        sidebar_layout.addStretch() # Empuja el menú hacia arriba

        # --- 4. CONTENEDOR DE SECCIONES (QStackedWidget) ---
        self.secciones = QStackedWidget()
        self.secciones.setObjectName("Contenido")
        
        # Creamos las páginas
        self.pagina_video = self.crear_pagina_descarga("VÍDEO MP4", "#5592E3")
        self.pagina_musica = self.crear_pagina_descarga("MÚSICA MP3", "#E35555")
        
        # Las añadimos al mazo de cartas
        self.secciones.addWidget(self.pagina_video)
        self.secciones.addWidget(self.pagina_musica)

        # --- 5. ENSAMBLAR TODO ---
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.secciones)

        # --- 6. EVENTOS (Cambiar entre secciones) ---
        self.btn_video.clicked.connect(lambda: self.cambiar_seccion(0))
        self.btn_musica.clicked.connect(lambda: self.cambiar_seccion(1))

    def crear_pagina_descarga(self, titulo, color):
        """Función ayudante para crear páginas con la misma estructura"""
        pag = QWidget()
        layout = QVBoxLayout(pag)
        layout.setContentsMargins(40, 40, 40, 40)
        
        lbl = QLabel(titulo)
        lbl.setStyleSheet(f"font-size: 20px; color: {color}; font-weight: bold;")
        
        input_url = QLineEdit()
        input_url.setPlaceholderText("Pega el enlace aquí...")
        
        btn_accion = QPushButton(f"Descargar {titulo.split()[0]}")
        btn_accion.setStyleSheet(f"background: {color}; color: white; border-radius: 5px;")
        btn_accion.setFixedWidth(200)

        layout.addWidget(lbl)
        layout.addWidget(input_url)
        layout.addWidget(btn_accion)
        layout.addStretch()
        return pag

    def cambiar_seccion(self, indice):
        # Cambiamos la "carta" visible
        self.secciones.setCurrentIndex(indice)
        
        # Actualizamos qué botón se ve como "activo"
        self.btn_video.setObjectName("Active" if indice == 0 else "")
        self.btn_musica.setObjectName("Active" if indice == 1 else "")
        
        # Forzamos a que el estilo se refresque
        self.btn_video.style().unpolish(self.btn_video)
        self.btn_video.style().polish(self.btn_video)
        self.btn_musica.style().unpolish(self.btn_musica)
        self.btn_musica.style().polish(self.btn_musica)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())