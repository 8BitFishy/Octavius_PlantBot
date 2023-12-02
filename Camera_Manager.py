try:
    from picamera import PiCamera
except:
    print("Camera module not installed")

from itertools import count
import os
from time import sleep
import subprocess

class Camera_Manager_Class:

    def __init__(self, rotation, imagecount, videocount, directory):
        try:
            self.camera = PiCamera()
            self.camera.rotation = rotation
        except:
            print("Camera module not installed")
            self.camera = None
            #self.camera.rotation = None

        self.imagecount = imagecount
        self.videocount = videocount
        self.directory = directory
        
    def Take_Picture(self):
        self.imagecount = self.imagecount + 1
        image_file = f'{self.directory}Images/image{self.imagecount}.jpg'
        self.camera.capture(image_file)
        return image_file
    
    def Take_Video(self, length):
        self.videocount = self.videocount + 1
        video_file = f'{self.directory}Videos/video{self.videocount}.h264'
        self.camera.start_recording(video_file)
        sleep(length)
        self.camera.stop_recording()
        command = f"MP4Box -add Videos/video{self.videocount}.h264 Videos/video{self.videocount}.mp4"
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        os.remove(video_file)
        video_file = f'{self.directory}Videos/video{self.videocount}.mp4'
        return video_file

def Generate_Camera_Manager(directory):
    counts = [0, 0]

    for i in range(2):
        if i == 0:
            modifier = "Images"
        else:
            modifier = "Videos"

        if os.path.exists(f"{directory}{modifier}"):
            #print(f"directory exists - {directory}{modifier}")
            for files in os.walk(f"{directory}{modifier}"):
                filelist = list(files[2])
                counts[i] = len(filelist)

        else:
            #print(f"Generating directory - {directory}{modifier}")

            os.mkdir(f"{directory}{modifier}")

    Octavius_Camera_Manager = Camera_Manager_Class(180, counts[0], counts[1], directory)

    return Octavius_Camera_Manager
