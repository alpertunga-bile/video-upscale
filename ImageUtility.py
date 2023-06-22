from os.path import exists, join
from os import mkdir
import cv2
from shutil import rmtree
from tqdm import tqdm

def ExtractImages(videoPath : str):
    if exists("temp"):
        rmtree("temp")
    
    mkdir("temp")

    vidCap = cv2.VideoCapture(videoPath)

    frameCount = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))
    height = int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH))

    for i in tqdm(range(0, frameCount), desc="Extracting Frames"):
        success, image = vidCap.read()
        cv2.imwrite(join("temp", f"frame{i + 1}.png"), image)

    return height, width