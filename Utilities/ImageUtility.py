from os.path import join
from cv2 import VideoCapture, imwrite, imread, VideoWriter, VideoWriter_fourcc
from cv2 import CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from tqdm import tqdm
from glob import glob
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from Utilities.Utility import CreateDirectory, RemoveFile

def ExtractAudio(videoPath : str):
    videoClip = VideoFileClip(videoPath)
    audioClip = videoClip.audio
    audioClip.write_audiofile("audio.mp3")
    videoClip.close()
    audioClip.close()

def ExtractFrames(videoPath : str):
    CreateDirectory("temp", True)
    CreateDirectory("tempOutput", True)

    RemoveFile("audio.mp3")
    ExtractAudio(videoPath)

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

def SetAudioToVideo(videoPath : str):
    audioClip = AudioFileClip("audio.mp3")
    videoClip = VideoFileClip(videoPath)
    RemoveFile(videoPath)

    newAudioClip = CompositeAudioClip([audioClip])
    videoClip.audio = newAudioClip
    videoClip.write_videofile(videoPath)
    
    videoClip.close()
    audioClip.close()

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

    SetAudioToVideo(join("outputs", f"{outputName}.mp4"))
    RemoveFile("audio.mp3")