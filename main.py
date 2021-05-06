#!/usr/bin/env python
import os

import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTime, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QInputDialog

from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
#caleta = None
#pipeline = None
#s = None
s = None
thread = None



class DisplayImage(QThread):
    displayImg = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self._recording = True

    def run(self):
        while self._recording:
            self.displayImg.emit(True)
            time.sleep(1)
            self.displayImg.emit(False)
            time.sleep(1)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._recording = False

def createDefaultRecordFolder():
    global PATH
    cmd = 'mkdir -p /home/$USER/oakd-videos'
    os.system(cmd)
    cmd = 'echo /home/$USER/oakd-videos/'
    PATH=str(os.popen(cmd).read()).rstrip()

def changeRecordImg(state):
    ui.recordicon.setVisible(state)
    ui.recordstate.setVisible(state)


def handleCamera():
    if ui.enableCamera.isChecked():
        ui.enableCamera.setText("Stop Camera")
        ui.enableCamera.setIcon(QtGui.QIcon('imgs/stop.png'))
        caleta.switchOnCamera("video1", ui.videoContent)
    else:
        ui.enableCamera.setText("Start Camera")
        ui.enableCamera.setIcon(QtGui.QIcon('imgs/play.png'))
        caleta.switchOffCamera()

def startCounting():
    global s
    s = 0
    timer.start(1000)

def stopCounting():
    timer.stop()
    ui.watchcounter.display("00:00:00")

def handleRecording():
    global thread
    if ui.startRecording.isChecked():
        ui.startRecording.setText("Stop Recording")
        ui.startRecording.setIcon(QtGui.QIcon('imgs/record.png'))
        visibleRecordItems(True)
        startCounting()
        ui.currentvideoname.setText(caleta.camera.getCurrentVideoName())
        caleta.startRecording()
        thread = DisplayImage()
        thread.displayImg.connect(changeRecordImg)
        thread.start()
        thread.exec()
    else:
        caleta.stopRecording()
        visibleRecordItems(False)
        ui.startRecording.setText("Start Recording")
        ui.startRecording.setIcon(QtGui.QIcon())
        stopCounting()
        try:
            thread.stop()
        except:
            pass



def visibleRecordItems(state):
    ui.recordicon.setVisible(state)
    ui.recordstate.setVisible(state)
    ui.watchcounter.setVisible(state)
    ui.currentvideoname.setVisible(state)
    ui.videonamelabel.setVisible(state)
    ui.recordicon.setVisible(state)

def LCDEvent():
    global s
    s += 1
    ui.watchcounter.display(time.strftime('%H:%M:%S', time.gmtime(s)))

def changePath():
    text, ok = QInputDialog.getText(window,'Change path', 'Set the new path (e.g. /home/user/videos)')
    if ok:
        caleta.changePath(str(text))

if __name__ == "__main__":
    global PATH
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.enableCamera.clicked.connect(handleCamera)
    ui.startRecording.clicked.connect(handleRecording)
    ui.setpath.triggered.connect(changePath)

    ui.recordicon.setPixmap(QtGui.QPixmap('imgs/recording.png'))
    ui.recordicon.setScaledContents(True)
    _seconds = 0
    ui.enableCamera.setIcon(QtGui.QIcon('imgs/play.png'))
    ui.watchcounter.setNumDigits(8)

    #-----
    createDefaultRecordFolder()
    #-----
    s = 0
    timer = QTimer()
    timer.timeout.connect(LCDEvent)
    ui.watchcounter.display("00:00:00")

    #-----
    visibleRecordItems(False)


    window.show()
    pipeline = CaletaAPI.CaletaAPI.getNewPipeline()
    caleta = CaletaAPI.CaletaAPI(pipeline,PATH)
    sys.exit(app.exec_())


