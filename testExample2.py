from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import depthai as dai

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    pipeline=None
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.pipeline = dai.Pipeline()
        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(300, 300)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

        xout_rgb = self.pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)

    def run(self):
        with dai.Device(self.pipeline) as device:
            # Start pipeline
            device.startPipeline()
            # Output queue will be used to get the rgb frames from the output defined above
            q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            while self._run_flag:
                print("true")
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                #qImg = QtGui.QImage(arr2, 300, 300, QtGui.QImage.Format_RGB888)
                self.change_pixmap_signal.emit(arr2)
                #cv2.imshow("bgr", in_rgb.getCvFrame())
                #if cv2.waitKey(1) == ord('q'):
                #   break


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        print("gha parado")
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        #-------------------------
        #pipeline = dai.Pipeline()
        #cam_rgb = pipeline.createColorCamera()
        #cam_rgb.setPreviewSize(300, 300)
        #cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        #cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        #cam_rgb.setInterleaved(False)
        #cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        # Create output


        #cam_rgb.preview.link(xout_rgb.input)

        #.---------------------------
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

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        print("dentro np.ndarray")
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())