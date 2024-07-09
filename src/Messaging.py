#!/usr/bin/env python3
##############################################################
#                          Messaging
#
#This script deals with any screen pop-ups that are to be 
#delivered to the user.
#
#Author: Nicholas Burns, January, 28th, 2024
##############################################################

from Resources.UI.About_Window import Ui_about_dialog

from PySide6.QtWidgets import QMessageBox, QDialog

class Messaging:

    def __init__(self, win):
        """
        Generate the pop-up object that will be delivered to the user.
        Style of the pop-up is also selected.

        :win: Import the main window, provides acess to all other
              connected scripts.
        :return: None
        """ 
        
        self.win = win

    def error_message(self, title, message):
        """
        Displays a pop-up box on the screen with a
        large red X that the user must exit to continue.

        :title: Words printed on the header of the pop-up.
        :message: Words printed in the body of the pop-up.
        :return: None
        """ 
        
        self.win.error_dialog = QMessageBox()
        self.win.error_dialog.setStyleSheet("background-color: rgb(49, 63, 80);color:white;")
        self.win.error_dialog.setWindowTitle(title)
        self.win.error_dialog.setText(message)
        self.win.error_dialog.setIcon(QMessageBox.Critical)
        self.win.error_dialog.show()

    def accept_message(self, title, message, data_type, index):

        self.win.error_dialog = QMessageBox()
        self.win.error_dialog.setStyleSheet("background-color: rgb(49, 63, 80);color:white;")
        self.win.error_dialog.setWindowTitle(title)
        self.win.error_dialog.setText(message)
        self.win.error_dialog.setStandardButtons(QMessageBox.Cancel|QMessageBox.Apply)

        self.win.error_dialog.setIcon(QMessageBox.Question)
        self.win.error_dialog.setDefaultButton(QMessageBox.Apply)

        self.win.error_dialog_choice = None

        if data_type == 'parameter':
            
            self.win.error_dialog.buttonClicked.connect(lambda button_choice: self.win.preconditioning.distribute_parameter(button_choice, index))

        elif data_type == 'bound':
            
            self.win.error_dialog.buttonClicked.connect(lambda button_choice: self.win.preconditioning.distribute_boundary(button_choice, index))

        self.win.error_dialog.show()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #                        About Us Window
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    class About_Popup(QDialog, Ui_about_dialog):

        def __init__(self, parent):

            super().__init__(parent)

            self.setupUi(self)
            self.show()

    def open_about_window(self):

        about_window = self.About_Popup(self.win)
        about_window.rejected.connect(lambda: self.close_about_window(about_window))

        self.win.setDisabled(True)
        about_window.setDisabled(False)

        about_window.show()

    def close_about_window(self, about_window):

        self.win.setDisabled(False)
        about_window.close()
        self.win.setFocus()