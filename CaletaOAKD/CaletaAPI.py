import cv2
import depthai as dai
from PyQt5.QtCore import QThread, pyqtSignal

from CaletaOAKD.OAKDCamera import OAKD


class CaletaAPI:

    @staticmethod
    def getNewPipeline():
        return dai.Pipeline()


    def __init__(self,pipeline):
        self.pipeline =  pipeline
        #self.initCamera()
    '''
    def initCamera(self,frame):
        # Define a source - color camera
        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(300, 300)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)


        # Create output
        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")

        #cam_rgb.preview.link(xout_rgb.input)

    '''

    def stopCamera(self):
        self.camera.stopAll()

    def startRecording(self):
        self.camera.startRecording(self.streamName,self.videoContainer)


    def switchOffCamera(self):
        self.camera.stopCamera()

    def switchOnCamera(self, streamName,videoContainer):
        self.streamName = streamName;
        self.videoContainer = videoContainer
        self.camera = OAKD(self.streamName,self.videoContainer)
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