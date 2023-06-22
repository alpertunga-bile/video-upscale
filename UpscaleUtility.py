from glob import glob
from os.path import join
from platform import system
from json import load
from subprocess import run, DEVNULL
from logging import Logger, INFO

from ImageUtility import ExtractFrames, CreateVideoFromFrames

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

    command += f"--ext png "

    if osName == "Windows":
        command += "&& venv\\Scripts\\deactivate.bat"

    run(command, shell=True, stderr=DEVNULL)

def Upscale(logger : Logger):
    videos = glob(join("inputs", "*.mp4")) + glob(join("inputs", "*.avi")) + glob(join("inputs", "*.mkv"))

    if len(videos) == 0:
        logger.log(INFO, "No videos in inputs folder")
        return

    for video in videos:
        logger.log(INFO, f"Upscaling {video} file")
        height, fps = ExtractFrames(video)
        RunUpscaleScript(height)
        CreateVideoFromFrames("output", fps)