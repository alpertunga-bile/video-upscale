from glob import glob
from os.path import join
from platform import system
from json import load
from subprocess import run

from ImageUtility import ExtractFrames

def RunUpscaleScript(originalHeight : int):
    osName = system()

    with open("settings.json", "r") as settingsFile:
        settingsDict = load(settingsFile)

    command = ""

    if osName == "Windows":
        command += "venv\\Scripts\\activate.bat && "
        command += "venv\\Scripts\\python.exe "
    elif osName == "Linux":
        command += "source venv/bin/activate && "
        command += "python3 "

    command += f"{join('Real-ESRGAN', 'inference_realesrgan.py')} -n {settingsDict['modelName']} "
    command += f"-i temp/ -o tempOutput/ "
    command += f"--outscale {settingsDict['targetHeight'] / originalHeight} "
    command += f"--tile {settingsDict['tileSize']} "

    if settingsDict['faceEnhance']:
        command += "--face_enhance "
    elif settingsDict['fp32']:
        command += "--fp32 "

    command += f"--ext {settingsDict['ext']} "

    if osName == "Windows":
        command += "&& venv\\Scripts\\deactivate.bat"

    run(command, shell=True)

def Upscale():
    videos = glob(join("inputs", "*.mp4"))

    for video in videos:
        height, width, fps = ExtractFrames(video)
        RunUpscaleScript(height)
        