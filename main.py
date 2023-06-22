from UpscaleUtility import Upscale

from logging import Logger, getLogger, INFO, StreamHandler, Formatter
from sys import stdout

def SetLogger(logger : Logger):
    logger.setLevel(INFO)

    handler = StreamHandler(stdout)
    handler.setLevel(INFO)
    formatter = Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler) 

if __name__ == "__main__":
    logger = getLogger()
    SetLogger(logger)

    Upscale(logger)