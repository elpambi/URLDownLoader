import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QUrl, Signal
from PySide6.QtGui import QPixmap, QIcon, QFont, QDesktopServices
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from app.styles import COLORS, PATHS


GIT_URL = "https://github.com/elpambi/URLDownLoader"
APP_URL = "https://your-app-site.example"


class ClickableLabel(QLabel):
    clicked = Signal()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("About")
        self.setWindowFlag(Qt.Window)
        self.setMinimumSize(360, 420)

        self.title = QLabel("About to Develop")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.avatar = QLabel()
        self.avatar.setObjectName("avatar")
        self.avatar.setFixedSize(96, 96)
        self.avatar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.avatar.setAlignment(Qt.AlignCenter)
        self._make_fallback_avatar()

        self.developer_label = QLabel("Developer: <a href='https://github.com/elpambi'>raspy_dev</a>")
        self.developer_label.setOpenExternalLinks(True)
        self.developer_label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.info_label = QLabel("If you have a doubt or question, visit:")
        self.info_label.setWordWrap(True)

        logos_row = QHBoxLayout()
        logos_row.setSpacing(16)

        self.logo_git = ClickableLabel()
        self.logo_git.setObjectName("logo_git")
        self.logo_git.setFixedSize(120, 80)
        self.logo_git.setAlignment(Qt.AlignCenter)
        self.logo_git.setCursor(Qt.PointingHandCursor)
        self.logo_git.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GIT_URL)))

        self.logo_app = ClickableLabel()
        self.logo_app.setObjectName("logo_app")
        self.logo_app.setFixedSize(120, 80)
        self.logo_app.setAlignment(Qt.AlignCenter)
        self.logo_app.setCursor(Qt.PointingHandCursor)
        self.logo_app.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(APP_URL)))

        logos_row.addWidget(self.logo_git)
        logos_row.addWidget(self.logo_app)

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(12)
        main.addWidget(self.title)

        avatar_row = QHBoxLayout()
        avatar_row.addWidget(self.avatar)
        avatar_row.addSpacing(12)
        avatar_row.addStretch()
        main.addLayout(avatar_row)

        main.addWidget(self.developer_label)
        main.addWidget(self.info_label)
        main.addLayout(logos_row)
        main.addStretch()

        theme = None
        if hasattr(parent, 'theme'):
            theme = getattr(parent, 'theme')
        elif parent is None:
            theme = 'dark'

        self.apply_theme(theme)

    def _make_fallback_avatar(self):
        self.avatar.setText("R")
        self.avatar.setStyleSheet(
            f"background: {COLORS['main_color']}; color: white; border-radius: 48px;"
            " font-size: 36px; font-weight: bold; padding-top:6px;"
        )

    def apply_theme(self, theme: str):
        if theme == 'light':
            bg = COLORS['bg_main_light']
            text = COLORS['texts_&_icons_light']
            bars = COLORS['bg_bars_light']
        else:
            bg = COLORS['bg_main_dark']
            text = COLORS['texts_&_icons_dark']
            bars = COLORS['bg_bars_dark']

        qss = f"""
            QWidget {{ background-color: {bg}; color: {text}; }}
            QLabel {{ color: {text}; }}
            QLabel#avatar {{ border: none; }}
        """
        self.setStyleSheet(qss)

        git_icon_path = PATHS.get('github_icon_light') if theme == 'light' else PATHS.get('github_icon_dark')
        if git_icon_path and os.path.exists(git_icon_path):
            pix = QPixmap(git_icon_path)
            if not pix.isNull():
                self.logo_git.setPixmap(pix.scaled(100, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_git.setStyleSheet("")
            else:
                self.logo_git.setPixmap(QPixmap())
                self.logo_git.setText("GITHUB")
                self.logo_git.setStyleSheet(f"color: {text};")
        else:
            self.logo_git.setPixmap(QPixmap())
            self.logo_git.setText("GITHUB")
            self.logo_git.setStyleSheet(f"color: {text};")

        app_logo = PATHS.get('logo')
        if app_logo and os.path.exists(app_logo):
            pix2 = QPixmap(app_logo)
            if not pix2.isNull():
                self.logo_app.setPixmap(pix2.scaled(100, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_app.setStyleSheet("")
            else:
                self.logo_app.setPixmap(QPixmap())
                self.logo_app.setText("APP")
                self.logo_app.setStyleSheet(f"color: {text};")
        else:
            self.logo_app.setPixmap(QPixmap())
            self.logo_app.setText("APP")
            self.logo_app.setStyleSheet(f"color: {text};")
