try:
    from picamera import PiCamera
except:
    print("Camera module not installed")

from itertools import count
import os
from time import sleep
import subprocess

class Camera_Manager:

    def __init__(self, rotation, imagecount, videocount, directory):
        self.rotation = rotation
        try:
            self.Initialise_Camera()
        except:
            print("Camera module not installed")
            self.camera = None
            #self.camera.rotation = None

        self.imagecount = imagecount
        self.videocount = videocount
        self.directory = directory


    def Initialise_Camera(self):
        self.camera = PiCamera()
        self.camera.rotation = self.rotation


    def Check_Camera(self):
        if self.camera is None:
            try:
                self.Initialise_Camera()
                if self.camera is None:
                    return False
            except:
                return False
        else:
            return True

        
    def Take_Picture(self):
        if self.Check_Camera():
            self.imagecount = self.imagecount + 1
            image_file = f'{self.directory}Images/image{self.imagecount}.jpg'
            self.camera.capture(image_file)
            return image_file
        else:
            return None

    
    def Take_Video(self, length):
        if self.Check_Camera():
            print(f"Recording {length} second video")
            self.videocount = self.videocount + 1
            video_file = f'{self.directory}Videos/video{self.videocount}.h264'
            print(f"{video_file}")
            self.camera.start_recording(video_file)
            sleep(length)
            self.camera.stop_recording()
            command = f"MP4Box -add {self.directory}Videos/video{self.videocount}.h264 {self.directory}Videos/video{self.videocount}.mp4"
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            print(output)
            #os.remove(video_file)
            video_file = f'{self.directory}Videos/video{self.videocount}.mp4'
            print(f"New video file = {video_file}")
            return video_file, output
        else:
            return None, None


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

    Octavius_Camera_Manager = Camera_Manager(180, counts[0], counts[1], directory)

    return Octavius_Camera_Manager
