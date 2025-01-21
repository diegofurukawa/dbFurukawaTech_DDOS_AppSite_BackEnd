import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler

class DynamicFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename_pattern, *args, **kwargs):
        self.filename_pattern = filename_pattern
        filename = self._get_current_filename()
        super().__init__(filename, *args, **kwargs)

    def _get_current_filename(self):
        return datetime.datetime.now().strftime(self.filename_pattern)

    def _open(self):
        current_filename = self._get_current_filename()
        if current_filename != self.baseFilename:
            self.baseFilename = current_filename
        return open(self.baseFilename, self.mode, encoding=self.encoding)

class ContextLogger(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        extra.update(self.extra)
        kwargs['extra'] = extra
        return f'[{self.extra.get("class_name", "")}] {msg}', kwargs

    def getChild(self, suffix):
        child_logger = self.logger.getChild(suffix)
        return ContextLogger(child_logger, self.extra)

class LogCreator:
    _instance = None

    @classmethod
    def get_instance(cls, log_directory="logs", log_prefix="log_processor_", 
                     log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = cls(log_directory, log_prefix, log_level)
        return cls._instance

    def __init__(self, log_directory="logs", log_prefix="log_processor_", 
                 log_level=logging.INFO):
        if LogCreator._instance is not None:
            raise Exception("This class is a singleton. Use get_instance() instead.")
        self.log_directory = log_directory
        self.log_prefix = log_prefix
        self.log_level = log_level
        self.logger = self.setup_logging()

    def get_log_file_pattern(self):
        return os.path.join(self.log_directory, f"{self.log_prefix}%Y%m%d.log")

    def setup_logging(self):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        logger = logging.getLogger(self.log_prefix.rstrip('_'))
        logger.setLevel(self.log_level)

        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = DynamicFileHandler(
            self.get_log_file_pattern(),
            when="midnight",
            interval=1,
            backupCount=0
        )
        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info(f"Logs configurados e salvos em {file_handler.baseFilename}")
        return logger

def create_logger(name, log_directory="logs", log_prefix="log_processor_", 
                  log_level=logging.INFO):
    log_creator = LogCreator.get_instance(log_directory, log_prefix, log_level)
    logger = log_creator.logger.getChild(name)
    return ContextLogger(logger, {"class_name": name})