# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 605)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 4, 4, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 2, 1, 1)
        self.video_2 = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_2.sizePolicy().hasHeightForWidth())
        self.video_2.setSizePolicy(sizePolicy)
        self.video_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.video_2.setText("")
        self.video_2.setAlignment(QtCore.Qt.AlignCenter)
        self.video_2.setObjectName("video_2")
        self.gridLayout.addWidget(self.video_2, 0, 4, 1, 3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_3.addWidget(self.pushButton_1, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 2, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 1, 4, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_5.addWidget(self.pushButton_3, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_5.addWidget(self.pushButton_4, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 1, 6, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_6.addWidget(self.pushButton_8, 1, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_6.addWidget(self.pushButton_7, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_6.addWidget(self.pushButton_9, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 3, 6, 2, 1)
        self.line_3 = QtWidgets.QFrame(self.centralWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 3, 2, 1)
        self.line_4 = QtWidgets.QFrame(self.centralWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 2, 6, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 5, 3, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.video_1 = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_1.sizePolicy().hasHeightForWidth())
        self.video_1.setSizePolicy(sizePolicy)
        self.video_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.video_1.setText("")
        self.video_1.setAlignment(QtCore.Qt.AlignCenter)
        self.video_1.setObjectName("video_1")
        self.horizontalLayout.addWidget(self.video_1)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.comboBox_1 = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_1.sizePolicy().hasHeightForWidth())
        self.comboBox_1.setSizePolicy(sizePolicy)
        self.comboBox_1.setMaximumSize(QtCore.QSize(16777215, 25))
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.gridLayout.addWidget(self.comboBox_1, 1, 0, 1, 2)
        self.video_3 = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_3.sizePolicy().hasHeightForWidth())
        self.video_3.setSizePolicy(sizePolicy)
        self.video_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.video_3.setText("")
        self.video_3.setAlignment(QtCore.Qt.AlignCenter)
        self.video_3.setObjectName("video_3")
        self.gridLayout.addWidget(self.video_3, 3, 0, 1, 5)
        self.comboBox_3 = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout.addWidget(self.comboBox_3, 4, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 5)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculon"))
        self.pushButton_6.setText(_translate("MainWindow", "Просмотр видео"))
        self.pushButton_5.setText(_translate("MainWindow", "Обозначить границы"))
        self.pushButton_1.setText(_translate("MainWindow", "Обозначить границы"))
        self.pushButton_2.setText(_translate("MainWindow", "Просмотр видео"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Обычный режим"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Распознавание людей"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Распознавание движения"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Распознавание границ"))
        self.pushButton_3.setText(_translate("MainWindow", "Обозначить границы"))
        self.pushButton_4.setText(_translate("MainWindow", "Просмотр видео"))
        self.pushButton_8.setText(_translate("MainWindow", "Настройки"))
        self.pushButton_7.setText(_translate("MainWindow", "Обновить"))
        self.pushButton_9.setText(_translate("MainWindow", "Выход"))
        self.comboBox_1.setItemText(0, _translate("MainWindow", "Обычный режим"))
        self.comboBox_1.setItemText(1, _translate("MainWindow", "Распознавание людей"))
        self.comboBox_1.setItemText(2, _translate("MainWindow", "Распознавание движения"))
        self.comboBox_1.setItemText(3, _translate("MainWindow", "Распознавание границ"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Обычный режим"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Распознавание людей"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Распознавание движения"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "Распознавание границ"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionReset.setShortcut(_translate("MainWindow", "Ctrl+R"))

