import logging

class Logger:

    WARNING = logging.WARNING
    INFO = logging.INFO


    def __init__(self) -> None:
        # Create a custom logger
        self.__logger = logging.getLogger(__name__)
        # Create handlers
        i_handler = logging.FileHandler('info.log')
        w_handler = logging.FileHandler('info.log')
        i_handler.setLevel(logging.WARNING)
        w_handler.setLevel(logging.INFO)
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s \t %(levelname)s \t %(message)s')
        f_format = logging.Formatter('%(asctime)s \t %(levelname)s \t %(message)s')
        i_handler.setFormatter(c_format)
        w_handler.setFormatter(f_format)
        # Add handlers to the logger
        self.__logger.addHandler(i_handler)
        self.__logger.addHandler(w_handler)
        pass
    
    def log(self, message, type):
        if type is self.INFO:
            self.__logger.info(message)
        if type is self.WARNING:
            self.__logger.warning(message)





