#!/usr/bin/env python

# Tool to help write new image for E310/312
# Scans connected drives and lists them to user
# Complete Tool Should:
#   * List drives to help user find memory card
#   * Format memory card
#   * Write image to memory card (dd)

import subprocess
import sys
import os

# GUI Imports
from PyQt4 import QtGui, QtCore
import PyQt4.Qwt5 as Qwt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

__version__ = "0.1.0" # Version String

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

## COPY GENERATED PyQT HERE ##
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(529, 216)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.button_select_sd = QtGui.QPushButton(self.centralwidget)
        self.button_select_sd.setObjectName(_fromUtf8("button_select_sd"))
        self.gridLayout.addWidget(self.button_select_sd, 1, 1, 1, 1)
        self.text_input_file = QtGui.QLineEdit(self.centralwidget)
        self.text_input_file.setObjectName(_fromUtf8("text_input_file"))
        self.gridLayout.addWidget(self.text_input_file, 0, 0, 1, 1)
        self.button_input_file = QtGui.QPushButton(self.centralwidget)
        self.button_input_file.setObjectName(_fromUtf8("button_input_file"))
        self.gridLayout.addWidget(self.button_input_file, 0, 1, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.button_write_image = QtGui.QPushButton(self.centralwidget)
        self.button_write_image.setObjectName(_fromUtf8("button_write_image"))
        self.gridLayout_2.addWidget(self.button_write_image, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.progress_write_image = QtGui.QProgressBar(self.centralwidget)
        self.progress_write_image.setProperty("value", 0)
        self.progress_write_image.setObjectName(_fromUtf8("progress_write_image"))
        self.verticalLayout_2.addWidget(self.progress_write_image)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 529, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.button_select_sd.setText(_translate("MainWindow", "Select Drive", None))
        self.text_input_file.setText(_translate("MainWindow", "Image File", None))
        self.button_input_file.setText(_translate("MainWindow", "Browse", None))
        self.lineEdit_2.setText(_translate("MainWindow", "SD Card", None))
        self.button_write_image.setText(_translate("MainWindow", "Write Image", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

## END GENERATED PyQT HERE ##


class Main(QtGui.QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # Push Button Actions
        self.ui.button_input_file.clicked.connect(self.select_image_file)
        self.ui.button_write_image.clicked.connect(self.write_image)
        self.ui.button_select_sd.clicked.connect(self.select_sd_card)

        self.image_file = ""


    def select_image_file(self):
        # Open dialog for user to select file (Get full file name/directory)
        temp_file = QtGui.QFileDialog.getOpenFileName(self, 'Select Image File')
        if not temp_file:
            # If nothing was selected, null string is returned
            self.ui.text_input_file.setText("Image File")
        else:
            self.ui.text_input_file.setText(temp_file)
            self.image_file = temp_file

    def write_image(self):
        # Execute on button press "Write Image" (button_write_image)
        print "Write Image Now!"
        self.get_image_size()

    def image_progress(self):
        pass     

    def get_image_size(self):
        # Get the size of the image file in bytes
        # Use to update write progress
        if not self.image_file:
            pass
        else:
            self.image_size = os.path.getsize(self.image_file)
            print "Image Size: %d bytes" % self.image_size

    def select_sd_card(self):
        # Exectue on button press "Select Drive" (button_select_sd)
        self.get_disk_names()



    def get_disk_names(self):
        # Get output of lsblk
        lsblk = subprocess.Popen(['lsblk'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Strip out lines that are 'disk' types (not partitions)
        blockdevs = [line.strip() for line in lsblk.stdout if 'disk' in line]

        returncode = lsblk.wait()

        if returncode:
            print("Something happened!")

        for devices in blockdevs:
            print devices

if __name__ == '__main__':

    if sys.platform.startswith('linux'):
        # Should show interface now
        app = QtGui.QApplication(sys.argv)
        window = Main()
        window.show()
        sys.exit(app.exec_())
    else:
        print "Only Linux Support now!"
    
