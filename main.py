import sys

from PyQt5 import QtWidgets, QtGui

from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
caleta = None
pipeline = None

def handleCamera():
    if ui.enableCamera.isChecked():
        ui.enableCamera.setText("Stop Camera")
        ui.enableCamera.setIcon(QtGui.QIcon('imgs/stop.png'))
        caleta.switchOnCamera("video1", ui.videoContent)
    else:
        ui.enableCamera.setText("Start Camera")
        ui.enableCamera.setIcon(QtGui.QIcon('imgs/play.png'))
        caleta.switchOffCamera()


def handleRecording():
    if ui.startRecording.isChecked():
        ui.startRecording.setText("Stop Recording")
        ui.startRecording.setIcon(QtGui.QIcon('imgs/record.png'))
        caleta.startRecording()
    else:
        ui.startRecording.setText("Start Recording")
        ui.startRecording.setIcon(QtGui.QIcon())

        caleta.stopRecording()


def uploadVideo():
    caleta.stopCamera()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.enableCamera.clicked.connect(handleCamera)
    ui.startRecording.clicked.connect(handleRecording)

    ui.enableCamera.setIcon(QtGui.QIcon('imgs/play.png'))


    window.show()
    pipeline = CaletaAPI.CaletaAPI.getNewPipeline()
    caleta = CaletaAPI.CaletaAPI(pipeline)
    sys.exit(app.exec_())