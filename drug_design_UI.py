# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drug_design_UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Spectrum_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.Spectrum_view.setGeometry(QtCore.QRect(250, 10, 581, 401))
        self.Spectrum_view.setObjectName("Spectrum_view")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 430, 181, 51))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(730, 440, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 430, 121, 51))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 853, 26))
        self.menubar.setObjectName("menubar")
        self.menuFlow_Control = QtWidgets.QMenu(self.menubar)
        self.menuFlow_Control.setObjectName("menuFlow_Control")
        self.menuSingle_Steps = QtWidgets.QMenu(self.menubar)
        self.menuSingle_Steps.setObjectName("menuSingle_Steps")
        self.menuDebugger = QtWidgets.QMenu(self.menubar)
        self.menuDebugger.setObjectName("menuDebugger")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFlow_Control.menuAction())
        self.menubar.addAction(self.menuSingle_Steps.menuAction())
        self.menubar.addAction(self.menuDebugger.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Optimization Step:"))
        self.pushButton.setText(_translate("MainWindow", "Override"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.menuFlow_Control.setTitle(_translate("MainWindow", "Flow Control"))
        self.menuSingle_Steps.setTitle(_translate("MainWindow", "Single Steps"))
        self.menuDebugger.setTitle(_translate("MainWindow", "Debugger"))

