from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import depthai as dai

class VideoThread(QThread):
    #change_pixmap_signal = pyqtSignal(np.ndarray)
    record_video = pyqtSignal(np.ndarray, cv2.VideoWriter)
    def __init__(self,streamName,videoContainer):
        super().__init__()
        self._run_flag = True
        self.streamName = streamName
        self.videoContainer = videoContainer
        self.pipeline = dai.Pipeline()

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out1 = cv2.VideoWriter('/home/bihut/Vídeos/output.mp4', self.fourcc, 30, (
        self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))

        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height())
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName(self.streamName)
        cam_rgb.preview.link(xout_rgb.input)

    def run(self):

        with dai.Device(self.pipeline) as device:
            device.startPipeline()
            q_rgb = device.getOutputQueue(name=self.streamName, maxSize=4, blocking=False)
            while self._run_flag:
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                #self.change_pixmap_signal.emit(arr2)
                self.record_video.emit(arr2, self.out1)


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        print("parada desde dentro")
        self._run_flag = False
        self.out1.release()


'''
class VideoRecord(QThread):
    #change_pixmap_signal = pyqtSignal(np.ndarray)
    record_video = pyqtSignal(np.ndarray)
    def __init__(self,streamName,videoContainer):
        super().__init__()
        self._run_flag = True
        self.streamName = streamName
        self.videoContainer = videoContainer
        self.pipeline = dai.Pipeline()

        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height())
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName(self.streamName)
        cam_rgb.preview.link(xout_rgb.input)


    def run(self):
        with dai.Device(self.pipeline) as device:
            print(device)
            device.startPipeline()
            q_rgb = device.getOutputQueue(name=self.streamName, maxSize=4, blocking=False)
            while self._run_flag:
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                 #self.change_pixmap_signal.emit(arr2)
                self.record_video.emit(arr2)



    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


'''

'''
class Thread2(QThread):

    def __init__(self, pipeline,streamName):
        super().__init__()
        self.active = True
        self.pipeline = pipeline
        self.streamName = streamName

    def run(self):
        if self.active:
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out1 = cv2.VideoWriter('/home/bihut/Vídeos/output.avi', self.fourcc, 30, (640, 480))
            #self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            #self.cap1.set(3, 480)
            #self.cap1.set(4, 640)
            #self.cap1.set(5, 30)
            xout_rgb = self.pipeline.createXLinkOut()
            xout_rgb.setStreamName(self.streamName)
            while self.active:
                #ret1, image1 = self.cap1.read()
                #if ret1:
                with dai.Device(self.pipeline) as device:
                    device.startPipeline()
                    q_rgb = device.getOutputQueue(name=self.streamName, maxSize=4, blocking=False)
                    while self._run_flag:
                        in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                        arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                        #self.change_pixmap_signal.emit(arr2)
                        self.out1.write(arr2)
                        #self.msleep(10)

    def stop(self):
        self.out1.release()
'''
class OAKD(QWidget):
    def setStreamName(self,name):
        self.streamName = name

    def setVideoContainer(self,container):
        self.videoContainer = container

    def __init__(self,streamName,videoContainer):
        super().__init__()
        self.streamName = streamName
        self.videoContainer = videoContainer
        '''
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        '''
        # create the video capture thread

    def startCamera(self):
        self.thread = VideoThread(self.streamName,self.videoContainer)
        # connect its signal to the update_image slot
        #self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.record_video.connect(self.save_video_image)
        # start the thread
        self.thread.start()
        self.thread.exec()

    def stopCamera(self):
        print("camara parada")
        self.thread.stop()
        #event.accept()

    def stopAll(self):
        self.thread.stop()

    def startRecording(self,pipeline,streamName):
        '''
        self.thread2 = VideoRecord(self.streamName,self.videoContainer)
        # connect its signal to the update_image slot
        #self.thread2.change_pixmap_signal.connect(self.update_image)
        self.thread2.record_video.connect(self.save_video_image)
        # start the thread
        self.thread2.start()
        self.thread2.exec()
        '''
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.videoContainer.setPixmap(qt_img)

    @pyqtSlot(np.ndarray,cv2.VideoWriter)
    def save_video_image(self, cv_img, out):
        """Updates the image_label with a new opencv image"""
        #print("saving video")
        qt_img = self.convert_cv_qt(cv_img)
        out.write(cv_img)
        #self.videoContainer.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        p = convert_to_Qt_format.scaled(self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height(), Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    a = App()
#    a.show()
#    sys.exit(app.exec_())