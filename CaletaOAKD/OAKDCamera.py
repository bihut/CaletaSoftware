from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import depthai as dai


RESOLUTION_WIDTH = 1920
RESOLUTION_HEIGHT = 1080
FPS = 60
FPS_MONO = 30
RESOLUTION_WIDTH_MONO = 1280
RESOLUTION_HEIGHT_MONO = 720

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def setRecording(self,val):
        self._recording = val
    def __init__(self, streamName, videoContainer):
        super().__init__()
        self._run_flag = True
        self._recording = False
        self.streamName = streamName
        self.videoContainer = videoContainer
        self.pipeline = dai.Pipeline()
        # 3840*2160
        # self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # self.out1 = cv2.VideoWriter('/home/bihut/Vídeos/output.mp4', self.fourcc, 30, (self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))

        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(RESOLUTION_WIDTH,RESOLUTION_HEIGHT)
        #cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        #cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        #cam_rgb.setInterleaved(False)
        #xout_rgb = self.pipeline.createXLinkOut()
        #xout_rgb.setStreamName(self.streamName)
        #cam_rgb.preview.link(xout_rgb.input)


        #
        #colorCam = self.pipeline.createColorCamera()

        monoCam = self.pipeline.createMonoCamera()
        monoCam.setCamId(1)

        monoCam2 = self.pipeline.createMonoCamera()
        monoCam2.setCamId(2)

        ve1 = self.pipeline.createVideoEncoder()
        ve1.setDefaultProfilePreset(1280, 720, 30, dai.VideoEncoderProperties.Profile.H264_MAIN)
        monoCam.out.link(ve1.input)

        ve2 = self.pipeline.createVideoEncoder()
        ve2.setDefaultProfilePreset(1920, 1080, 30, dai.VideoEncoderProperties.Profile.H265_MAIN)
        cam_rgb.video.link(ve2.input)


        ve3 = self.pipeline.createVideoEncoder()
        ve3.setDefaultProfilePreset(1280, 720, 30, dai.VideoEncoderProperties.Profile.H264_MAIN)
        monoCam2.out.link(ve3.input)

        # Create outputs
        ve1Out = self.pipeline.createXLinkOut()
        ve1Out.setStreamName('ve1Out')
        ve1.bitstream.link(ve1Out.input)

        ve2Out = self.pipeline.createXLinkOut()
        ve2Out.setStreamName("ve2Out")
        #---
        cam_rgb.setVideoSize(RESOLUTION_WIDTH,RESOLUTION_HEIGHT)
        #cam_rgb.setPreviewSize(300, 300)
        videoEncoder = self.pipeline.createVideoEncoder()
        videoEncoder.setDefaultProfilePreset(cam_rgb.getVideoSize(), FPS,
                                             dai.VideoEncoderProperties.Profile.MJPEG)
        cam_rgb.video.link(videoEncoder.input)
        videoEncoder.bitstream.link(ve2Out.input)

        #---
        #ve2.bitstream.link(ve2Out.input)

        #cam_rgb.setInterleaved(True)
        #cam_rgb.preview.link(ve2Out.input)

        ve3Out = self.pipeline.createXLinkOut()
        ve3Out.setStreamName('ve3Out')
        ve3.bitstream.link(ve3Out.input)




    def run(self):
        with dai.Device(self.pipeline) as self.device:
            device = self.device
            device.startPipeline()
            data = device.getOutputQueue('ve2Out')
            while self._run_flag:
                #for previewFrame in previewFrames:
                    #cv2.imshow('preview',
                    #           previewFrame.getData().reshape(previewFrame.getWidth(), previewFrame.getHeight(), 3))
                try:
                    videoFrames = data.tryGetAll()
                    for videoFrame in videoFrames:
                        # Decode JPEG
                        #print("dentro")
                        frame0 = cv2.imdecode(videoFrame.getData(), cv2.IMREAD_UNCHANGED)
                        frame = cv2.resize(frame0, (
                          self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
                        arr2 = np.require(frame, np.uint8, 'C')
                        self.change_pixmap_signal.emit(arr2)
                        # Display
                        #cv2.imshow('video', frame)
                    #frame = cv2.resize(previewFrames.getCvFrame(), (
                    #   self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
                    #arr2 = np.require(frame, np.uint8, 'C')
                    #self.change_pixmap_signal.emit(arr2)
                except:
                    pass
                #print(self._run_flag)
            #in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                #print(in_rgb.getCvFrame().shape)
                #frame = cv2.resize(in_rgb.getCvFrame(), (
                #    self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
                #arr2 = np.require(frame, np.uint8, 'C')
                #self.change_pixmap_signal.emit(arr2)
                #in_rgb.getData().tofile(file_color_h265)

                '''
                #print("tiene")
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                frame = cv2.resize(in_rgb.getCvFrame(), (
                self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
                arr2 = np.require(frame, np.uint8, 'C')
                self.change_pixmap_signal.emit(arr2)
                if self._recording:
                    file_color_h265 = open(self.videoname + '-center.h265', 'wb')
                    while in_rgb.has():
                        in_rgb.get().getData().tofile(file_color_h265)
                '''
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False


    def getPipeline(self):
        return self.pipeline

    def getDevice(self):
        return self.device

class VideoThread(QThread):
    #change_pixmap_signal = pyqtSignal(np.ndarray)
    #record_video = pyqtSignal(np.ndarray, cv2.VideoWriter)

    def __init__(self,streamName,videoContainer,PATH,pipeline,device):
        super().__init__()
        self._recording = True
        self.streamName = streamName
        self.videoContainer = videoContainer
        self.device = device
        self.pipeline = pipeline#dai.Pipeline()
        self.videoname = PATH
        #3840*2160
        #self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #self.out1 = cv2.VideoWriter('/home/bihut/Vídeos/output.mp4', self.fourcc, 30, (self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
        '''
        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(RESOLUTION_WIDTH,RESOLUTION_HEIGHT)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName(self.streamName)
        cam_rgb.preview.link(xout_rgb.input)

        ve1 = self.pipeline.createVideoEncoder()
        ve1.setDefaultProfilePreset(RESOLUTION_WIDTH, RESOLUTION_HEIGHT, FPS, dai.VideoEncoderProperties.Profile.H265_MAIN)
        ve1.bitstream.link(xout_rgb.input)
        cam_rgb.video.link(ve1.input)

        #right and left cameras
        camRight = self.pipeline.createMonoCamera()
        camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

        xoutRight = self.pipeline.createXLinkOut()
        xoutRight.setStreamName("right")
        camRight.out.link(xoutRight.input)

        ve2 = self.pipeline.createVideoEncoder()
        ve2.setDefaultProfilePreset(RESOLUTION_WIDTH_MONO, RESOLUTION_HEIGHT_MONO, FPS_MONO, dai.VideoEncoderProperties.Profile.H264_MAIN)
        camRight.out.link(ve2.input)

        ve2Out = self.pipeline.createXLinkOut()
        ve2Out.setStreamName('right')
        ve2.bitstream.link(ve2Out.input)


        camLeft = self.pipeline.createMonoCamera()
        camLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        camLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

        ve3 = self.pipeline.createVideoEncoder()
        ve3.setDefaultProfilePreset(RESOLUTION_WIDTH_MONO, RESOLUTION_HEIGHT_MONO, FPS_MONO, dai.VideoEncoderProperties.Profile.H264_MAIN)
        camLeft.out.link(ve3.input)

        ve3Out = self.pipeline.createXLinkOut()
        ve3Out.setStreamName('left')
        ve3.bitstream.link(ve3Out.input)

        '''
        #-----
        '''
        colorCam = self.pipeline.createColorCamera()

        monoCam = self.pipeline.createMonoCamera()
        monoCam.setCamId(1)

        monoCam2 = self.pipeline.createMonoCamera()
        monoCam2.setCamId(2)

        ve1 = self.pipeline.createVideoEncoder()
        ve1.setDefaultProfilePreset(1280, 720, 30, dai.VideoEncoderProperties.Profile.H264_MAIN)
        monoCam.out.link(ve1.input)

        ve2 = self.pipeline.createVideoEncoder()
        ve2.setDefaultProfilePreset(1920, 1080, 30, dai.VideoEncoderProperties.Profile.H265_MAIN)
        colorCam.video.link(ve2.input)

        ve3 = self.pipeline.createVideoEncoder()
        ve3.setDefaultProfilePreset(1280, 720, 30, dai.VideoEncoderProperties.Profile.H264_MAIN)
        monoCam2.out.link(ve3.input)

        # Create outputs
        ve1Out = self.pipeline.createXLinkOut()
        ve1Out.setStreamName('ve1Out')
        ve1.bitstream.link(ve1Out.input)

        ve2Out = self.pipeline.createXLinkOut()
        ve2Out.setStreamName("ve2Out")
        ve2.bitstream.link(ve2Out.input)

        ve3Out = self.pipeline.createXLinkOut()
        ve3Out.setStreamName('ve3Out')
        ve3.bitstream.link(ve3Out.input)
        '''

    def run(self):
        device = self.device# dai.Device(self.pipeline)
        #device.startPipeline()
        outQ1 = device.getOutputQueue(name='ve1Out')
        outQ2 = device.getOutputQueue(name="ve2Out")
        outQ3 = device.getOutputQueue(name='ve3Out')
        file_mono1_h264 = open(self.videoname + '-right.h264', 'wb')
        file_mono2_h264 = open(self.videoname + '-left.h264', 'wb')
        file_color_h265 = open(self.videoname + '-center.h265', 'wb')
        while self._recording:
            try:
                while outQ1.has():
                    outQ1.get().getData().tofile(file_mono1_h264)
                while outQ2.has():
                    outQ2.get().getData().tofile(file_color_h265)
                while outQ3.has():
                    outQ3.get().getData().tofile(file_mono2_h264)
            except KeyboardInterrupt:
                 # Keyboard interrupt (Ctrl + C) detected
                 print("error")

        '''
        with dai.Device(self.pipeline) as device, open(self.videoname+'-right.h264', 'wb') as file_mono1_h264, open(self.videoname+'-center.h265', 'wb') as file_color_h265, open(self.videoname+'-left.h264', 'wb') as file_mono2_h264:
            device.startPipeline()
            q_rgb = device.getOutputQueue(name=self.streamName, maxSize=4, blocking=False)
            qLeft = device.getOutputQueue("left", maxSize=4, blocking=False)
            qRight = device.getOutputQueue("right", maxSize=4, blocking=False)

            #outQ3 = device.getOutputQueue(name='left')
            while self._run_flag:
                while q_rgb.has():
                    in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                    frame = cv2.resize(in_rgb.getCvFrame(), (self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
                    arr2 = np.require(frame, np.uint8, 'C')
                    self.change_pixmap_signal.emit(arr2)
                if self._recording:
                    #arr3 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                    #self.record_video.emit(arr3, self.writer)
                    while qLeft.has():
                        qLeft.get().getData().tofile(file_mono2_h264)
                    while qRight.has():
                        qRight.get().getData().tofile(file_mono1_h264)
                    while q_rgb.has():
                            q_rgb.get().getData().tofile(file_color_h265)
                    #arr3 = np.require(in_monoleft.getCvFrame(), np.uint8, 'C')
                    #self.record_video.emit(arr3, self.writer_left)
                    #arr3 = np.require(in_monoright.getCvFrame(), np.uint8, 'C')
                    #self.record_video.emit(arr3, self.writer_right)
            '''


    #def startRecording(self,writer,writer_left,writer_right):
    def startRecording(self):
        #self.writer = writer
        self._recording = True
        #self.writer_left = writer_left
        #self.writer_right = writer_right

    def stopRecording(self):
        self._recording=False
        cmd = "ffmpeg -framerate 30 -i {} -c copy {}"
        print(cmd.format(self.videoname + '-right.h264', self.videoname + "-right.mp4"))
        print(cmd.format(self.videoname + '-left.h264', self.videoname + "-left.mp4"))
        print(cmd.format(self.videoname + '-center.h265', self.videoname + "-center.mp4"))


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
       # self._run_flag = False
        if self._recording:
            self.stopRecording()
        self.wait()

class OAKD(QWidget):
    def setStreamName(self,name):
        self.streamName = name

    def setVideoContainer(self,container):
        self.videoContainer = container

    def __init__(self,streamName,videoContainer):
        super().__init__()
        self.streamName = streamName
        self.videoContainer = videoContainer

        self.PATH = '/home/bihut/Vídeos/'
        self.videoname = ""

    def startCamera(self):
        #self.thread = VideoThread(self.streamName,self.videoContainer,self.PATH)
        self.threadCamera = CameraThread(self.streamName, self.videoContainer)
        # connect its signal to the update_image slot
        self.threadCamera.change_pixmap_signal.connect(self.update_image)
        #self.thread.record_video.connect(self.save_video_image)
        # start the thread
        self.threadCamera.start()
        self.threadCamera.exec()

    def stopCamera(self):
        #corregir la parada y reinicio de visualización
        try:
            self.thread.stop()
        except:
            pass
        self.threadCamera.stop()



    def stopRecording(self):
        self.thread.stopRecording()
        #cmd = "ffmpeg -framerate 30 -i {} -c copy {}"
        #print(cmd.format(self.videoname + '-right.h264', self.videoname + "-right.mp4"))
        #print(cmd.format(self.videoname + '-left.h264', self.videoname + "-left.mp4"))
        #print(cmd.format(self.videoname + '-center.h265', self.videoname + "-center.mp4"))

        #self.videoname = ""

    def getCurrentVideoName(self):
        return self.videoname

    def changePath(self,path,id):
        self.PATH = path
        self.videoname= self.PATH + str(id)
        #print("path cambiado a %s",self.PATH)

    def startRecording(self):
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #self.videoname = self.PATH + str(id)
        '''
        writer = cv2.VideoWriter(self.videoname+"-center.avi", fourcc, FPS_MONO, (
                RESOLUTION_WIDTH_MONO, RESOLUTION_HEIGHT_MONO))
        writer_left = cv2.VideoWriter(self.videoname+"-left.avi", fourcc, FPS_MONO, (
            RESOLUTION_WIDTH_MONO, RESOLUTION_HEIGHT_MONO))
        writer_right = cv2.VideoWriter(self.videoname+"-right.avi", fourcc, FPS_MONO, (
            RESOLUTION_WIDTH_MONO, RESOLUTION_HEIGHT_MONO))
        '''
        self.thread = VideoThread(self.streamName,self.videoContainer,self.videoname,self.threadCamera.pipeline,self.threadCamera.device)
        # connect its signal to the update_image slot
        #self.threadCamera.change_pixmap_signal.connect(self.update_image)
        # self.thread.record_video.connect(self.save_video_image)
        # start the thread
        self.thread.start()
        self.thread.exec()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.videoContainer.setPixmap(qt_img)

    @pyqtSlot(np.ndarray,cv2.VideoWriter)
    def save_video_image(self, cv_img, out):
        """Updates the image_label with a new opencv image"""
        out.write(cv_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    a = App()
#    a.show()
#    sys.exit(app.exec_())