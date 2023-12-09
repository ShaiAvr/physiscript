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

app = App(1600, 900)

while app.running:
    app.start_frame()
    app.update()

app.shutdown()
