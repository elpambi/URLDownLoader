"""Entry launcher that imports the `app` package cleanly and runs the GUI.

Using a package-style import ensures that `app` is available when frozen by PyInstaller.
"""
import sys
from PySide6.QtWidgets import QApplication

try:
    from app.windows.main_window import MainWindow
except Exception:
    # fallback: try relative import if running unpacked
    from src.app.windows.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
