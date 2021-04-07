import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
caleta = None
pipeline = None
recording = False
def handleCamera():

    #caleta.switchOnCamera("video1", ui.videoContent)

    caleta.switchOnCamera("video1",ui.videoContent)


def handleRecording():
    print("dejando de grabar")  # we will just print clicked when the button is pressed
    caleta.switchOffCamera()

    '''
    global recording
    if recording==False:
        caleta.startRecording()
        recording = True
    else:
        caleta.startRecording()
        recording = False
    '''
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