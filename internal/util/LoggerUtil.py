
import logging

class LoggerUtil:

    def get() -> logging.Logger:
        ...
        return logging.getLogger()