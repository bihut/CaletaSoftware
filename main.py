import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from CaletaOAKD import CaletaAPI
from mainUI import Ui_MainWindow
caleta = None
def handleCamera():
    print("clicked") # we will just print clicked when the button is pressed
    caleta.switchOnCamera(ui.videoFrame)
def handleRecording():
    print("clicked2") # we will just print clicked when the button is pressed

def uploadVideo():
    print("clicked") # we will just print clicked when the button is pressed


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.enableCamera.clicked.connect(handleCamera)
    ui.startRecording.clicked.connect(handleRecording)
    window.show()

    caleta = CaletaAPI.CaletaAPI()
    caleta.initCamera(ui.videoFrame)
    caleta.switchOnCamera(ui.videoFrame)

    sys.exit(app.exec_())