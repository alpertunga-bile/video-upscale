from shutil import rmtree
from os.path import exists
from os import remove, mkdir
from logging import Logger, INFO, StreamHandler, Formatter
from sys import stdout

def RemoveDirectory(directory : str):
    if exists(directory):
        rmtree(directory)

def RemoveFile(file : str):
    if exists(file):
        remove(file)

def CreateDirectory(directory : str, remove : bool = False):
    isExist = exists(directory)

    if isExist and remove:
        rmtree(directory)

    if isExist is False:
        mkdir(directory)

def SetLogger(logger : Logger):
    logger.setLevel(INFO)

    handler = StreamHandler(stdout)
    handler.setLevel(INFO)
    formatter = Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)