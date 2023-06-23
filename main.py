from Utilities.UpscaleUtility import Upscale
from Utilities.Utility import RemoveDirectory, SetLogger

from logging import getLogger

def Clear():
    RemoveDirectory("temp")
    RemoveDirectory("tempOutput")

if __name__ == "__main__":
    logger = getLogger()
    SetLogger(logger)

    Upscale(logger)

    Clear()