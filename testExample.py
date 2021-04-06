import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject, QThread
import sys
import cv2
import depthai as dai


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self,in_rgb,image_label):
        # capture from web cam
        #cap = cv2.VideoCapture(0)
        #while self._run_flag:
        #    ret, cv_img = cap.read()
        #    if ret:
        #        self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        #cap.release()
        arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
        qImg = QtGui.QImage(arr2, 300, 300, QtGui.QImage.Format_RGB888)
        image_label.setPixmap(QtGui.QPixmap.fromImage(qImg))
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class App(QWidget):

    def __init__(self):
        super().__init__()
        #-------------------------
        pipeline = dai.Pipeline()
        cam_rgb = pipeline.createColorCamera()
        cam_rgb.setPreviewSize(300, 300)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        # Create output
        xout_rgb = pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")

        cam_rgb.preview.link(xout_rgb.input)

        #.---------------------------



        self.setWindowTitle("Qt static label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Polecat')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        '''
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                # convert the image to Qt format
                qt_img = self.convert_cv_qt(cv_img)
                # display it
                self.image_label.setPixmap(qt_img)
        '''
        with dai.Device(pipeline) as device:
            print("aaqui")
            # Start pipeline
            device.startPipeline()

            # Output queue will be used to get the rgb frames from the output defined above
            q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            print(q_rgb)
            while True:
                in_rgb = q_rgb.get()  # blocking call, will wait until a new data has arrived
                #qt_img = self.convert_cv_qt(in_rgb.getCvFrame())
                #arr2 = np.require(in_rgb.getCvFrame(), np.uint8, 'C')
                #qImg = QtGui.QImage(arr2, 300, 300, QtGui.QImage.Format_RGB888)
                #cv2.imshow("bgr",in_rg)
                # Retrieve 'bgr' (opencv format) frame
                #cv2.imshow("bgr", in_rgb.getCvFrame())
                #self.image_label.setPixmap(QtGui.QPixmap.fromImage(qImg))
                if cv2.waitKey(1) == ord('q'):
                   break

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
    print("listo pa show")
    a.show()
    sys.exit(app.exec_())