# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(557, 307)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.deleteLastVideo = QtWidgets.QPushButton(self.centralwidget)
        self.deleteLastVideo.setObjectName("deleteLastVideo")
        self.gridLayout.addWidget(self.deleteLastVideo, 0, 2, 1, 1)
        self.startRecording = QtWidgets.QPushButton(self.centralwidget)
        self.startRecording.setObjectName("startRecording")
        self.gridLayout.addWidget(self.startRecording, 0, 1, 1, 1)
        self.enableCamera = QtWidgets.QPushButton(self.centralwidget)
        self.enableCamera.setObjectName("enableCamera")
        self.gridLayout.addWidget(self.enableCamera, 0, 0, 1, 1)
        self.videoFrame = QtWidgets.QFrame(self.centralwidget)
        self.videoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoFrame.setObjectName("videoFrame")
        self.gridLayout.addWidget(self.videoFrame, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 557, 22))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.deleteLastVideo.setText(_translate("MainWindow", "Delete last video"))
        self.startRecording.setText(_translate("MainWindow", "Start Recording"))
        self.enableCamera.setText(_translate("MainWindow", "Enable Camera"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
