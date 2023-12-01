from picamera import PiCamera
from itertools import count
import os
from time import sleep
import subprocess

class Camera_Manager_Class:
    _ids = count(0)

    def __init__(self, rotation, imagecount, videocount):
        self.camera = PiCamera()
        self.camera.rotation = rotation
        self.imagecount = imagecount
        self.videocount = videocount
        
    def Take_Picture(self):
        self.imagecount = self.imagecount + 1
        image_file = f'/home/pi/Documents/Octavius/Camera/Images/image{self.imagecount}.jpg'
        self.camera.capture(image_file)
        return image_file
    
    def Take_Video(self, length):
        self.videocount = self.videocount + 1
        video_file = f'/home/pi/Documents/Octavius/Camera/Videos/video{self.videocount}.h264'
        self.camera.start_recording(video_file)
        sleep(length)
        self.camera.stop_recording()
        command = f"MP4Box -add Camera/Videos/video{self.videocount}.h264 Camera/Videos/video{self.videocount}.mp4"
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        os.remove(video_file)
        video_file = f'/home/pi/Documents/Octavius/Camera/Videos/video{self.videocount}.mp4'
        return video_file

def Generate_Camera_Manager():
    for files in os.walk('Camera/Images'):
        filelist = list(files[2])
        imagecount = len(filelist)
    for files in os.walk('Camera/Videos'):
        filelist = list(files[2])
        videocount = len(filelist)
        
    Octavius_Camera_Manager = Camera_Manager_Class(180, imagecount, videocount)
    return Octavius_Camera_Manager
