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

from physiscript import App

app = App(1600, 900, limit_fps=True, target_fps=30)
dt = 0

while app.running:
    app.start_frame()
    if dt > 0:
        app.title = f"{1 / dt:.3f} FPS {'(Idling)' if app.is_idling else ''}"
    dt = app.update()

app.shutdown()
