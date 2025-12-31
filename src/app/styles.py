import sys
from pathlib import Path

# ==========================================
# CONFIGURATION CONSTANTS
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
    "input_bg_light": "#807373",
    "input_bg_dark": "#463C3C",
}

if hasattr(sys, '_MEIPASS'):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

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
    "github_icon_light": str(BASE_DIR / "resources" / "github_icon_light.svg"),
    "github_icon_dark": str(BASE_DIR / "resources" / "github_icon_dark.svg"),

}