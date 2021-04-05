import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from mainUI import Ui_MainWindow

def handleCamera():
    print("clicked") # we will just print clicked when the button is pressed

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
    ui.uploadVideo.clicked.connect(uploadVideo)
    window.show()
    sys.exit(app.exec_())