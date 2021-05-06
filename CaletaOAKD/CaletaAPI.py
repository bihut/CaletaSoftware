import os

import cv2
import depthai as dai
from PyQt5.QtCore import QThread, pyqtSignal

from CaletaOAKD.OAKDCamera import OAKD


class CaletaAPI:

    @staticmethod
    def getNewPipeline():
        return dai.Pipeline()

    @staticmethod
    def getUniqueID():
        import calendar;
        import time;
        ts = calendar.timegm(time.gmtime())
        return ts

    def __init__(self,pipeline,path):
        self.pipeline =  pipeline
        #cmd = 'echo /home/$USER/oakd-videos/'
        self.PATH = path #str(os.system(cmd)) #"/home/bihut/Vídeos/"

    def stopCamera(self):
        self.camera.stopAll()

    def startRecording(self):
        self.camera.startRecording()

    def stopRecording(self):
        self.camera.stopRecording()

    def switchOffCamera(self):
        self.camera.stopCamera()

    def changePath(self,str):
        self.PATH=str
        try:
            if self.camera is not None:
                self.camera.changePath(str)
        except Exception:
            pass

        #self.camera.changePath(str)

    def switchOnCamera(self, streamName,videoContainer):
        self.streamName = streamName;
        self.videoContainer = videoContainer
        self.camera = OAKD(self.streamName,self.videoContainer,self.PATH, self.getUniqueID())
        #self.camera.changePath(self.PATH,self.getUniqueID())
        self.camera.startCamera()


        '''''
        with dai.Device(self.pipeline) as device:
            # Start pipeline
            device.startPipeline()

            # Output queue will be used to get the rgb frames from the output defined above
            q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

            while True:
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                #cv2.imshow("bgr",in_rg)
                # Retrieve 'bgr' (opencv format) frame
                cv2.imshow("bgr", in_rgb.getCvFrame())
                self.thread = VideoThread()
                # connect its signal to the update_image slot
                self.thread.change_pixmap_signal.connect(self.update_image)
                # start the thread
                self.thread.start()

                if cv2.waitKey(1) == ord('q'):
                   break
        '''