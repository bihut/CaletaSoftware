import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
caleta = None
pipeline = None
def handleCamera():
    if ui.enableCamera.isChecked():
        ui.enableCamera.setText("Stop Camera")
        caleta.switchOnCamera("video1", ui.videoContent)
    else:
        ui.enableCamera.setText("Start Camera")
        caleta.switchOffCamera()

def handleRecording():
    if ui.startRecording.isChecked():
        ui.startRecording.setText("Stop Recording")
        caleta.startRecording()
    else:
        ui.startRecording.setText("Start Recording")
        caleta.stopRecording()


def uploadVideo():
    #print("clicked") # we will just print clicked when the button is pressed
    caleta.stopCamera()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.enableCamera.clicked.connect(handleCamera)
    ui.startRecording.clicked.connect(handleRecording)
    ui.deleteLastVideo.clicked.connect(uploadVideo)
    window.show()
    pipeline = CaletaAPI.CaletaAPI.getNewPipeline()
    caleta = CaletaAPI.CaletaAPI(pipeline)
    sys.exit(app.exec_())