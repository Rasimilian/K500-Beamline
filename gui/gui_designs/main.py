# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/gui_designs/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.graphicsView_2 = PlotWidget(self.centralwidget)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout.addWidget(self.graphicsView_2, 0, 1, 1, 1)
        self.graphicsView_4 = PlotWidget(self.centralwidget)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout.addWidget(self.graphicsView_4, 1, 1, 1, 1)
        self.graphicsView_3 = PlotWidget(self.centralwidget)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout.addWidget(self.graphicsView_3, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plainTextEdit_13 = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit_13.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_13.setObjectName("plainTextEdit_13")
        self.gridLayout_3.addWidget(self.plainTextEdit_13, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainTextEdit_11 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_11.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_11.setReadOnly(True)
        self.plainTextEdit_11.setObjectName("plainTextEdit_11")
        self.gridLayout_2.addWidget(self.plainTextEdit_11, 4, 4, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.plainTextEdit, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout_2.addWidget(self.plainTextEdit_2, 3, 2, 1, 1)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_3.setReadOnly(True)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.gridLayout_2.addWidget(self.plainTextEdit_3, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 6, 1, 1, 1)
        self.plainTextEdit_12 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_12.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_12.setReadOnly(True)
        self.plainTextEdit_12.setObjectName("plainTextEdit_12")
        self.gridLayout_2.addWidget(self.plainTextEdit_12, 5, 4, 1, 1)
        self.plainTextEdit_10 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_10.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_10.setReadOnly(True)
        self.plainTextEdit_10.setObjectName("plainTextEdit_10")
        self.gridLayout_2.addWidget(self.plainTextEdit_10, 3, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_6.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_6.setReadOnly(True)
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.gridLayout_2.addWidget(self.plainTextEdit_6, 4, 3, 1, 1)
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_5.setReadOnly(True)
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.gridLayout_2.addWidget(self.plainTextEdit_5, 4, 2, 1, 1)
        self.plainTextEdit_9 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_9.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_9.setReadOnly(True)
        self.plainTextEdit_9.setObjectName("plainTextEdit_9")
        self.gridLayout_2.addWidget(self.plainTextEdit_9, 5, 1, 1, 1)
        self.plainTextEdit_8 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_8.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_8.setReadOnly(True)
        self.plainTextEdit_8.setObjectName("plainTextEdit_8")
        self.gridLayout_2.addWidget(self.plainTextEdit_8, 5, 2, 1, 1)
        self.plainTextEdit_7 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_7.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_7.setReadOnly(True)
        self.plainTextEdit_7.setObjectName("plainTextEdit_7")
        self.gridLayout_2.addWidget(self.plainTextEdit_7, 5, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.plainTextEdit_4.setReadOnly(True)
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.gridLayout_2.addWidget(self.plainTextEdit_4, 4, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setAutoExclusive(True)
        self.pushButton_6.setFlat(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 1, 3, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.setAutoExclusive(True)
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 1, 2, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setChecked(True)
        self.pushButton_7.setAutoExclusive(True)
        self.pushButton_7.setFlat(True)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 1, 4, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.setAutoExclusive(True)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.pushButton_2.setText(_translate("MainWindow", "Save stats"))
        self.pushButton_3.setText(_translate("MainWindow", "Auto-save"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Best beam passing"))
        self.label.setText(_translate("MainWindow", "X"))
        self.label_6.setText(_translate("MainWindow", "I"))
        self.label_5.setText(_translate("MainWindow", "Y"))
        self.pushButton_6.setText(_translate("MainWindow", "DT13"))
        self.pushButton_5.setText(_translate("MainWindow", "DT12"))
        self.pushButton_7.setText(_translate("MainWindow", "1P7"))
        self.pushButton_4.setText(_translate("MainWindow", "DT11"))
from pyqtgraph import PlotWidget