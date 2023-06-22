from os.path import exists, join
from os import mkdir
from cv2 import VideoCapture, imwrite, imread, VideoWriter, VideoWriter_fourcc
from cv2 import CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from shutil import rmtree
from tqdm import tqdm
from glob import glob

def RecreateFolder(folderName : str):
    if exists(folderName):
        rmtree(folderName)

    mkdir(folderName)

def ExtractFrames(videoPath : str):
    RecreateFolder("temp")
    RecreateFolder("tempOutput")

    vidCap = VideoCapture(videoPath)

    frameCount = int(vidCap.get(CAP_PROP_FRAME_COUNT))
    height = int(vidCap.get(CAP_PROP_FRAME_HEIGHT))
    fps = float(vidCap.get(CAP_PROP_FPS))

    for i in tqdm(range(0, frameCount), desc="Extracting Frames"):
        success, image = vidCap.read()
        if success:
            imwrite(join("temp", f"frame{i + 1}.png"), image)

    vidCap.release()

    return height, fps

def CreateVideoFromFrames(outputName : str, fps : int):
    totalFiles = len(glob(join("tempOutput", "*")))
    frames = []
    for i in range(0, totalFiles):
        image = imread(join("tempOutput", f"frame{i + 1}_out.png"))
        height, width, layers = image.shape
        size = (width, height)
        frames.append(image)
    
    output = VideoWriter(join("outputs", f"{outputName}.mp4"), VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in tqdm(range(0, len(frames)), desc="Creating Video"):
        output.write(frames[i])

    output.release()