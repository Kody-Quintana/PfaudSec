# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'redirect.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.outputbox = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputbox.setFont(font)
        self.outputbox.setReadOnly(True)
        self.outputbox.setObjectName("outputbox")
        self.verticalLayout_5.addWidget(self.outputbox)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.outputbox_2 = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputbox_2.setFont(font)
        self.outputbox_2.setReadOnly(True)
        self.outputbox_2.setObjectName("outputbox_2")
        self.verticalLayout_4.addWidget(self.outputbox_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.grab_sel = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grab_sel.sizePolicy().hasHeightForWidth())
        self.grab_sel.setSizePolicy(sizePolicy)
        self.grab_sel.setObjectName("grab_sel")
        self.verticalLayout.addWidget(self.grab_sel)
        self.output_sel = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_sel.sizePolicy().hasHeightForWidth())
        self.output_sel.setSizePolicy(sizePolicy)
        self.output_sel.setObjectName("output_sel")
        self.verticalLayout.addWidget(self.output_sel)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.grab_display = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grab_display.sizePolicy().hasHeightForWidth())
        self.grab_display.setSizePolicy(sizePolicy)
        self.grab_display.setMaximumSize(QtCore.QSize(16777215, 50))
        self.grab_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.grab_display.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.grab_display.setReadOnly(True)
        self.grab_display.setObjectName("grab_display")
        self.verticalLayout_2.addWidget(self.grab_display)
        self.output_display = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_display.sizePolicy().hasHeightForWidth())
        self.output_display.setSizePolicy(sizePolicy)
        self.output_display.setMaximumSize(QtCore.QSize(16777215, 50))
        self.output_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_display.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.output_display.setReadOnly(True)
        self.output_display.setObjectName("output_display")
        self.verticalLayout_2.addWidget(self.output_display)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.latex_render = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.latex_render.sizePolicy().hasHeightForWidth())
        self.latex_render.setSizePolicy(sizePolicy)
        self.latex_render.setMinimumSize(QtCore.QSize(200, 0))
        self.latex_render.setObjectName("latex_render")
        self.horizontalLayout_2.addWidget(self.latex_render)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_10.addWidget(self.checkBox)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem6)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setMaximum(3)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_10.addWidget(self.spinBox)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem7)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem8 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.job_entry_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.job_entry_1.setObjectName("job_entry_1")
        self.verticalLayout_7.addWidget(self.job_entry_1)
        self.job_entry_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.job_entry_2.setObjectName("job_entry_2")
        self.verticalLayout_7.addWidget(self.job_entry_2)
        self.job_entry_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.job_entry_3.setObjectName("job_entry_3")
        self.verticalLayout_7.addWidget(self.job_entry_3)
        self.job_entry_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.job_entry_4.setObjectName("job_entry_4")
        self.verticalLayout_7.addWidget(self.job_entry_4)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        spacerItem9 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(20, 15, 20, 15)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBox_loose_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_loose_2.setText("")
        self.checkBox_loose_2.setObjectName("checkBox_loose_2")
        self.horizontalLayout_12.addWidget(self.checkBox_loose_2)
        self.lineEdit_loose_name_2 = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_loose_name_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_loose_name_2.setSizePolicy(sizePolicy)
        self.lineEdit_loose_name_2.setObjectName("lineEdit_loose_name_2")
        self.horizontalLayout_12.addWidget(self.lineEdit_loose_name_2)
        self.gridLayout.addLayout(self.horizontalLayout_12, 2, 0, 1, 1)
        self.pushButton_loose_2 = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_loose_2.sizePolicy().hasHeightForWidth())
        self.pushButton_loose_2.setSizePolicy(sizePolicy)
        self.pushButton_loose_2.setObjectName("pushButton_loose_2")
        self.gridLayout.addWidget(self.pushButton_loose_2, 2, 1, 1, 1)
        self.checkBox_loose_1 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_loose_1.setObjectName("checkBox_loose_1")
        self.gridLayout.addWidget(self.checkBox_loose_1, 1, 0, 1, 1)
        self.pushButton_loose_0 = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_loose_0.sizePolicy().hasHeightForWidth())
        self.pushButton_loose_0.setSizePolicy(sizePolicy)
        self.pushButton_loose_0.setChecked(False)
        self.pushButton_loose_0.setObjectName("pushButton_loose_0")
        self.gridLayout.addWidget(self.pushButton_loose_0, 0, 1, 1, 1)
        self.pushButton_loose_1 = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_loose_1.sizePolicy().hasHeightForWidth())
        self.pushButton_loose_1.setSizePolicy(sizePolicy)
        self.pushButton_loose_1.setObjectName("pushButton_loose_1")
        self.gridLayout.addWidget(self.pushButton_loose_1, 1, 1, 1, 1)
        self.checkBox_loose_0 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_loose_0.setObjectName("checkBox_loose_0")
        self.gridLayout.addWidget(self.checkBox_loose_0, 0, 0, 1, 1)
        self.lineEdit_loose_0 = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_loose_0.sizePolicy().hasHeightForWidth())
        self.lineEdit_loose_0.setSizePolicy(sizePolicy)
        self.lineEdit_loose_0.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_loose_0.setObjectName("lineEdit_loose_0")
        self.gridLayout.addWidget(self.lineEdit_loose_0, 0, 2, 1, 1)
        self.lineEdit_loose_1 = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_loose_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_loose_1.setSizePolicy(sizePolicy)
        self.lineEdit_loose_1.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_loose_1.setObjectName("lineEdit_loose_1")
        self.gridLayout.addWidget(self.lineEdit_loose_1, 1, 2, 1, 1)
        self.lineEdit_loose_2 = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_loose_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_loose_2.setSizePolicy(sizePolicy)
        self.lineEdit_loose_2.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_loose_2.setObjectName("lineEdit_loose_2")
        self.gridLayout.addWidget(self.lineEdit_loose_2, 2, 2, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox)
        spacerItem10 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1280, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuConfig = QtWidgets.QMenu(self.menuBar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionSections_config = QtWidgets.QAction(MainWindow)
        self.actionSections_config.setObjectName("actionSections_config")
        self.actionxelatex_config = QtWidgets.QAction(MainWindow)
        self.actionxelatex_config.setObjectName("actionxelatex_config")
        self.actionUser_Procedure = QtWidgets.QAction(MainWindow)
        self.actionUser_Procedure.setObjectName("actionUser_Procedure")
        self.actionAbout_PfaudSec = QtWidgets.QAction(MainWindow)
        self.actionAbout_PfaudSec.setObjectName("actionAbout_PfaudSec")
        self.menuConfig.addAction(self.actionSections_config)
        self.menuConfig.addSeparator()
        self.menuConfig.addAction(self.actionxelatex_config)
        self.menuHelp.addAction(self.actionUser_Procedure)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_PfaudSec)
        self.menuBar.addAction(self.menuConfig.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.grab_sel, self.output_sel)
        MainWindow.setTabOrder(self.output_sel, self.latex_render)
        MainWindow.setTabOrder(self.latex_render, self.outputbox)
        MainWindow.setTabOrder(self.outputbox, self.outputbox_2)
        MainWindow.setTabOrder(self.outputbox_2, self.output_display)
        MainWindow.setTabOrder(self.output_display, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.grab_display)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PfaudSec Data Book tool"))
        self.label.setText(_translate("MainWindow", "PfaudSec: Data Book"))
        self.label_2.setText(_translate("MainWindow", "LaTeX output:"))
        self.label_3.setText(_translate("MainWindow", "PfaudSec output:"))
        self.grab_sel.setText(_translate("MainWindow", "Select document folder"))
        self.output_sel.setText(_translate("MainWindow", "Select output folder"))
        self.latex_render.setText(_translate("MainWindow", "Render PDF"))
        self.checkBox.setText(_translate("MainWindow", "Output to same folder"))
        self.label_4.setText(_translate("MainWindow", "Compression level:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Job Info:"))
        self.job_entry_1.setPlaceholderText(_translate("MainWindow", "Order Number"))
        self.job_entry_2.setPlaceholderText(_translate("MainWindow", "Serial Number"))
        self.job_entry_3.setPlaceholderText(_translate("MainWindow", "Customer"))
        self.job_entry_4.setPlaceholderText(_translate("MainWindow", "Equipment"))
        self.groupBox.setTitle(_translate("MainWindow", "Other Documents:"))
        self.lineEdit_loose_name_2.setPlaceholderText(_translate("MainWindow", "Other"))
        self.pushButton_loose_2.setText(_translate("MainWindow", "Select Folder"))
        self.checkBox_loose_1.setText(_translate("MainWindow", "Brazil Data Book 2"))
        self.pushButton_loose_0.setText(_translate("MainWindow", "Select Folder"))
        self.pushButton_loose_1.setText(_translate("MainWindow", "Select Folder"))
        self.checkBox_loose_0.setText(_translate("MainWindow", "Brazil Data Book"))
        self.menuConfig.setTitle(_translate("MainWindow", "Config"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSections_config.setText(_translate("MainWindow", "Sections config"))
        self.actionxelatex_config.setText(_translate("MainWindow", "XeLaTeX config"))
        self.actionUser_Procedure.setText(_translate("MainWindow", "User Procedure"))
        self.actionAbout_PfaudSec.setText(_translate("MainWindow", "About PfaudSec"))

