from Utilities.UpscaleUtility import Upscale
from Utilities.Utility import RemoveDirectory, SetLogger, ClearTerminal, RemoveFile
from Completer import Completer

from logging import getLogger
from json import load, dumps

def Clear():
    from torch.cuda import empty_cache
    from gc import collect

    try:
        empty_cache()
        collect()
    except Exception:
        pass

    RemoveDirectory("temp")
    RemoveDirectory("tempOutput")
    RemoveFile("audio.mp3")

def PrintMainCommands():
    printString = """
    ?           : Open help menu
    cls | clear : Clear the terminal
    exit        : Exit from the application
    print       : Print the upscale settings
    upscale     : Upscale videos in the inputs folder
    set         : Change variables in the upscale settings 
    """

    print(printString)

def PrintSettings():
    with open("settings.json", "r") as file:
        settings = load(file)

    printString = f"""
    targetHeight = {settings['targetHeight']}
    modelName    = {settings['modelName']}
    tileSize     = {settings['tileSize']}
    faceEnhance  = {settings['faceEnhance']}
    fp32         = {settings['fp32']}
    """

    print(printString)

def PrintSetCommands():
    printString = """
    ?                   : Show this menu
    targetHeight (int)  : Set Target Height (1080, 1440, 2160)
    modelName    (str)  : Set Model To Upscale
    tileSize     (int)  : Set Tile Size (Lower values more optimizations but more time). Use 0 for no tiling.
    faceEnhance  (bool) : Activate / Deactivate face enhance with GPFGAN
    fp32         (bool) : Activate / Deactivate fp32 functionality. Use it if you get black outputs.
    clear | cls         : Clear terminal
    exit                : Return to main menu
    """

    print(printString)

def SaveToJson(settings : dict):
    tempJson = dumps(settings, indent=5)

    with open("settings.json", "w") as file:
        file.write(tempJson)

def PrintModelNames():
    printString = """
    ?                  : Show this menu
    clear | cls        : Clear terminal
    exit               : Return to Set menu
    set                : Set model name
    Usable model names :
        RealESRGAN_x4plus
        RealESRGAN_x4plus_anime_6B
        RealESRNet_x4plus
        RealESRGAN_x2plus
        realesr-general-x4v3
    """

    print(printString)

def SetModelName(completer : Completer, settings : dict):
    completer.SetCompleteFunction("modelNames")
    operation = ""

    while True:
        if operation == "?":
            print(f"Current model name : {settings['modelName']}")
            PrintModelNames()
            operation = ""
        elif operation == "clear" or operation == "cls":
            ClearTerminal()
            operation = ""
        elif operation == "exit":
            break
        elif operation == "set":
            print(f"Current model name : {settings['modelName']}")
            settings['modelName'] = input("Model Name : ")
            SaveToJson(settings)
            operation = ""
        else:
            operation = input("ModelName> ")

def SetSettings(completer : Completer):
    completer.SetCompleteFunction("setCommands")
    operation = ""

    with open("settings.json", "r") as file:
        settings = load(file)

    while True:
        if operation == "clear" or operation == "cls":
            ClearTerminal()
            operation = ""
        elif operation == "exit":
            break
        elif operation == "?":
            PrintSetCommands()
            operation = ""
        elif operation == "targetHeight":
            settings["targetHeight"] = int(input("Set Target Size : "))
            SaveToJson(settings)
            operation = ""
        elif operation == "modelName":
            SetModelName(completer, settings)
            operation = ""
        elif operation == "tileSize":
            settings["tileSize"] = int(input("Set Tile Size : "))
            SaveToJson(settings)
            operation = ""
        elif operation == "faceEnhance":
            completer.SetCompleteFunction("trueOrFalse")
            settings["faceEnhance"] = bool(input("Set Face Enhance [true | false] : ").capitalize())
            SaveToJson(settings)
            operation = ""
        elif operation == "fp32":
            completer.SetCompleteFunction("trueOrFalse")
            settings["fp32"] = bool(input("Set Fp32 [true | false] : ").capitalize())
            SaveToJson(settings)
            operation = ""
        else:
            completer.SetCompleteFunction("setCommands")
            operation = input("Set> ")

def SetCompleteFunctions(completer : Completer):
    completer.AddCompleteFunction("mainCompleter", None, vocabs=["print", "cls", "clear", "exit", "?", "upscale", "set"])
    completer.AddCompleteFunction("setCommands", None, vocabs=["?", "targetHeight", "modelName", "tileSize", "faceEnhance", "fp32", "clear", "cls", "exit"])
    completer.AddCompleteFunction("modelNames", None, vocabs=["?", "exit", "set", "clear", "cls", "RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B", "RealESRNet_x4plus", "RealESRGAN_x2plus", "realesr-general-x4v3"])
    completer.AddCompleteFunction("trueOrFalse", None, vocabs=["true", "false", "True", "False"])

if __name__ == "__main__":
    completer = Completer()
    SetCompleteFunctions(completer)
    
    logger = getLogger()
    SetLogger(logger)

    completer.SetCompleteFunction("mainCompleter")
    operation = "clear"

    while True:
        if operation == "clear" or operation == "cls":
            ClearTerminal()
            operation = ""
        elif operation == "?":
            PrintMainCommands()
            operation = ""
        elif operation == "print":
            PrintSettings()
            operation = ""
        elif operation == "set":
            SetSettings(completer)
            operation = ""
        elif operation == "upscale":
            Upscale(logger)
            operation = ""
        elif operation == "exit":
            break
        else:
            completer.SetCompleteFunction("mainCompleter")
            operation = input("Main> ")

    Clear()