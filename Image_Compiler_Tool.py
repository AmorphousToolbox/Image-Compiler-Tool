#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
===================================================================
Amorphous Toolbox - Image Compiler Tool

This GUI is designed to compile large sets of X-ray total scattering 
images.

Author: Nick Burns, January, 20th, 2024
===================================================================
'''

import src

import sys
import ctypes

from Resources.UI.Main_Window import Ui_MainWindow

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtCore import QCoreApplication, Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices

version = '1.0.0'

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        #=========================================
        #                Imports
        #=========================================

        #<<<<<<<<<<<<UI<<<<<<<<<<<<<<
        self.setupUi(self)
        
        #<<<<<<<<<<<<Utility Scripts<<<<<<<<<<<<<<
        self.canvas = src.Canvas
        self.image = src.Image(self)
        self.plot = src.Plot(self)
        self.trace = src.Trace(self)
        self.bounds = src.Bounds(self)
        self.selection = src.Selection(self)
        self.trees = src.Trees(self)
        self.files = src.Files(self)
        self.messaging = src.Messaging(self)

        #=========================================
        #       Widget/Main Window Settings
        #=========================================

        self.version = version
    
        self.statusBar.addPermanentWidget(QLabel('v' + str(version) + '                                 \
                                                                                            \
                                                                                            \
                                                           Created By: N. Burns and S. Kycia'))
        
        self.menuBar.setStyleSheet("""
                                    QMenu::item:selected
                                    {
                                        background: rgb(38, 109, 154);
                                        color: white;
                                    }

                                    QMenu::item:hover
                                    {
                                        background: rgb(38, 109, 154);
                                        color: white;
                                    }
                                    QMenubar::item:hover
                                    {
                                        background: rgb(38, 109, 154);
                                        color: white;
                                    }
                                    QMenubar::item:selected
                                    {
                                        background: rgb(38, 109, 154);
                                        color: white;
                                    } 
                                    """)
        
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        #=========================================
        #             Event Handeling
        #=========================================

        self.actionAbout.triggered.connect(self.messaging.open_about_window)
        self.actionDocumentation.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.AmorphousToolbox.com", QUrl.TolerantMode)))
        self.actionExit.triggered.connect(self.close)
    
if __name__ == '__main__':

    defaultfont = QFont('Ubuntu', 11)
    myappid = 'AmorphopusToolbox.Image_Compiler_Tool.' + str(version)

    if sys.platform == 'win32':
        
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(defaultfont)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())