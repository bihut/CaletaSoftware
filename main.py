#!/usr/bin/env python
import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTime, QTimer

from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
#caleta = None
#pipeline = None
#s = None
s = None
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
    if ui.startRecording.isChecked():
        startCounting()

        ui.startRecording.setText("Stop Recording")
        ui.startRecording.setIcon(QtGui.QIcon('imgs/record.png'))
        caleta.startRecording()

    else:
        stopCounting()
        ui.startRecording.setText("Start Recording")
        ui.startRecording.setIcon(QtGui.QIcon())
        caleta.stopRecording()

def LCDEvent():
    global s
    s += 1
    ui.watchcounter.display(time.strftime('%H:%M:%S', time.gmtime(s)))
    #ui.watchcounter.display(s)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.enableCamera.clicked.connect(handleCamera)
    ui.startRecording.clicked.connect(handleRecording)
    _seconds = 0
    ui.enableCamera.setIcon(QtGui.QIcon('imgs/play.png'))
    ui.watchcounter.setNumDigits(8)

    #-----
    s = 0
    timer = QTimer()
    timer.timeout.connect(LCDEvent)
    ui.watchcounter.display("00:00:00")
    #-----


    window.show()
    pipeline = CaletaAPI.CaletaAPI.getNewPipeline()
    caleta = CaletaAPI.CaletaAPI(pipeline)
    sys.exit(app.exec_())