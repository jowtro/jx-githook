import logging

from logging.handlers import RotatingFileHandler


class LoggerX(object):

    def __init__(self, stackTrace=False, path='./git_hook.log', name="Instace_1"):
        """
        If you still need to handle the exception and still want a log just use
        raise keyword
        Args:
            stackTrace (boo: optional): prints stackTrace into log
            path (str: optional): path to log.
        """
        self.stackTrace = stackTrace
        if not hasattr(LoggerX, 'logging_initialized'):
            LoggerX.create_rotating_log(path, name)

    @staticmethod
    def create_rotating_log(path, name):
        """
        Creates a rotating log
        """
        maxMB = 20  # maximum log size MB

        myFormatter = logging.Formatter(
            '%(levelname)s:[%(asctime)s]:%(name)s: %(message)s ')
        LoggerX.logger = logging.getLogger(f'instance_name: {name}')
        LoggerX.logger.setLevel(logging.INFO)

        # add a rotating handler
        LoggerX.handler = RotatingFileHandler(path,
                                              maxBytes=maxMB * 1024 * 1024,
                                              backupCount=5)
        LoggerX.handler.setFormatter(myFormatter)
        LoggerX.logger.addHandler(LoggerX.handler)
        LoggerX.logging_initialized = True

    def __call__(self, func):
        """
        @Decorator
        Decorator that wraps a func and if it raises a exception it will log it
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                LoggerX.logger.error(
                    f'[ERROR]: {ex}', exc_info=self.stackTrace)
        return wrapper
