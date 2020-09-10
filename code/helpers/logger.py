import daiquiri
import logging
import sys


daiquiri.setup(
    level=logging.INFO,
    outputs=[
        daiquiri.output.Stream(
            sys.stdout,
            daiquiri.formatter.ColorExtrasFormatter(
                keywords=[],
                fmt=(
                    "%(asctime)s %(color)s%(levelname)-8.8s "
                    "%(name)s | %(message)s%(color_stop)s %(extras)s"
                ),
            )
        ),
    ],
    capture_warnings=False,
)

class Logger:
    def __init__(self, name):
        self.log = daiquiri.getLogger(name)
        self.args = ()
        self.kwargs = {}

    def set(self, *args, **kwargs):
        self.kwargs = {**self.kwargs, **kwargs}
        return self

    def info(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.log.info(*args, **kwargs)
        return self

    def warn(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.log.warn(*args, **kwargs)
        return self

    def error(self, *args, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        self.log.error(*args, **kwargs)
        return self
