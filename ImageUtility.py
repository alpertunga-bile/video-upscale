from os.path import exists, join
from os import mkdir
from cv2 import VideoCapture, imwrite
from cv2 import CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FPS
from shutil import rmtree
from tqdm import tqdm

def ExtractFrames(videoPath : str):
    if exists("temp"):
        rmtree("temp")

    if exists("tempOutput"):
        rmtree("tempOutput")
    
    mkdir("temp")
    mkdir("tempOutput")

    vidCap = VideoCapture(videoPath)

    frameCount = int(vidCap.get(CAP_PROP_FRAME_COUNT))
    height = int(vidCap.get(CAP_PROP_FRAME_HEIGHT))
    width = int(vidCap.get(CAP_PROP_FRAME_WIDTH))
    fps = float(vidCap.get(CAP_PROP_FPS))

    for i in tqdm(range(0, frameCount), desc="Extracting Frames"):
        success, image = vidCap.read()
        imwrite(join("temp", f"frame{i + 1}.png"), image)

    vidCap.release()

    return height, width, fps