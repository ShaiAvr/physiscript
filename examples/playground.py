import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    level="TRACE",
    format=(
        "<green>{time:DD.MM.YYYY HH:mm:ss.SSS}</> | "
        "<level>{level: <10}</> {level.icon} | "
        "<cyan>{name}</>:<cyan>{function}</>:<cyan>{line}</> - "
        "<level>{message}</>"
    ),
)

import imgui

from physiscript import App

app = App(1600, 900, clear_color=(0.08, 0.16, 0.18), fps=60, exit_on_escape=False)
ui = app.ui()

option = 0

while app.running:
    app.start_frame()
    imgui.show_demo_window()
    app.update()

app.shutdown()
