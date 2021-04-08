from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import depthai as dai
PATH = '/home/bihut/Vídeos/'
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    record_video = pyqtSignal(np.ndarray, cv2.VideoWriter)
    def __init__(self,streamName,videoContainer):
        super().__init__()
        self._run_flag = True
        self._recording = False
        self.streamName = streamName
        self.videoContainer = videoContainer
        self.pipeline = dai.Pipeline()

        #self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #self.out1 = cv2.VideoWriter('/home/bihut/Vídeos/output.mp4', self.fourcc, 30, (self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))

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
                self.change_pixmap_signal.emit(arr2)
                if self._recording:
                    self.record_video.emit(arr2, self.writer)

    def startRecording(self,writer):
        self.writer = writer
        self._recording = True
    def stopRecording(self):
        self._recording=False
        self.writer.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        print("parada desde dentro")
        self._run_flag = False
        #self.out1.release()
        #self.closeWriter()
        self.stopRecording()
class OAKD(QWidget):
    def setStreamName(self,name):
        self.streamName = name

    def setVideoContainer(self,container):
        self.videoContainer = container

    def __init__(self,streamName,videoContainer):
        super().__init__()
        self.streamName = streamName
        self.videoContainer = videoContainer


    def startCamera(self):
        self.thread = VideoThread(self.streamName,self.videoContainer)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.record_video.connect(self.save_video_image)
        # start the thread
        self.thread.start()
        self.thread.exec()

    def stopCamera(self):
        self.thread.stop()

     #def stopAll(self):
     #   self.thread.stop()

    def stopRecording(self):
        self.thread.stopRecording()

    def startRecording(self,id):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(PATH+str(id)+".mp4", fourcc, 30, (
            self.videoContainer.frameGeometry().width(), self.videoContainer.frameGeometry().height()))
        self.thread.startRecording(writer)

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