import logging
import time


class LogUtil:

    WARNING = logging.WARNING
    INFO = logging.INFO
    __format = '%(asctime)s :: %(levelname)s : %(message)s'
    __out = ''

    def __init__(self, output='a.log') -> None:
        with open('readme.txt', 'w') as f:
            f.write('')
         
        self.__out = output
        pass

    def convertToXSV(line, delim):
        retval = str(line[0])
        for i in range(1, len(line)):
            retval += delim + str(line[i])
        return retval + "\n"

    def log(self, message, type):
        if type is self.INFO:
            logging.basicConfig(filename=self.__out, level=type,
                                filemode='a', format=self.__format)
            logging.info(message)
        if type is self.WARNING:
            logging.basicConfig(filename=self.__out, level=type,
                                filemode='a', format=self.__format)
            logging.warning(message)


    def print(self, message, type):
        t = time.strftime("%H:%M:%S", time.localtime())
        prefix = "WARNING(%s)::" if type is self.WARNING else "INFO(%s)::"
        print(prefix % t, message)
