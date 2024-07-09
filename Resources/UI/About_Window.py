# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'About_Window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QSizePolicy, QTextBrowser, QWidget)
import Resources_rc

class Ui_about_dialog(object):
    def setupUi(self, about_dialog):
        if not about_dialog.objectName():
            about_dialog.setObjectName(u"about_dialog")
        about_dialog.resize(580, 350)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(about_dialog.sizePolicy().hasHeightForWidth())
        about_dialog.setSizePolicy(sizePolicy)
        about_dialog.setMinimumSize(QSize(580, 350))
        about_dialog.setMaximumSize(QSize(580, 350))
        palette = QPalette()
        brush = QBrush(QColor(225, 225, 225, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(39, 50, 64, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(225, 225, 225, 128))
        brush2.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        about_dialog.setPalette(palette)
        about_dialog.setStyleSheet(u"background-color:  rgb(39, 50, 64);\n"
"color: rgb(225, 225, 225);")
        self.gridLayout = QGridLayout(about_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(about_dialog)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        self.label.setMaximumSize(QSize(150, 150))
        self.label.setPixmap(QPixmap(u":/Images/Resources/Icons/Full_Amorphous_Toolbox_Logo_Short.png"))
        self.label.setScaledContents(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.textBrowser_2 = QTextBrowser(about_dialog)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setEnabled(True)
        self.textBrowser_2.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser_2.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.textBrowser_2, 0, 1, 1, 1)

        self.line = QFrame(about_dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)

        self.textBrowser = QTextBrowser(about_dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(True)
        self.textBrowser.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 2)


        self.retranslateUi(about_dialog)

        QMetaObject.connectSlotsByName(about_dialog)
    # setupUi

    def retranslateUi(self, about_dialog):
        about_dialog.setWindowTitle(QCoreApplication.translate("about_dialog", u"About Us", None))
        self.label.setText("")
        self.textBrowser_2.setHtml(QCoreApplication.translate("about_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-size:12pt; font-weight:700; color:#deddda;\">Amorphous Toolbox - Image Compiler Tool (v1.0.0)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-size:12pt; color:#deddda;\">\u00a9 </span><span style=\" font-family:'Ubuntu'; font-size"
                        ":11pt; color:#deddda;\">2023-2024</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu'; font-size:11pt; color:#deddda;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.AmorphousToolbox.com\"><span style=\" font-family:'Ubuntu'; font-size:11pt; text-decoration: underline; color:#308cc6;\">http://www.AmorphousToolbox.com</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu'; font-size:11pt; color:#deddda;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"docs-internal-guid-abab8ce0-7fff-f0ea-0a1f-36777192c8c7\"></a><span style=\" font-family:'Arial','sans-"
                        "serif'; font-size:10pt; color:#deddda; background-color:transparent;\">C</span><span style=\" font-family:'Arial','sans-serif'; font-size:10pt; color:#deddda; background-color:transparent;\">reated by: </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; font-weight:700; color:#deddda; background-color:transparent;\">Nicholas Burns</span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; color:#deddda; background-color:transparent;\"> (</span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; text-decoration: underline; color:#308cc6; background-color:transparent;\">burnsn@uoguelph.ca</span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; color:#deddda; background-color:transparent;\">)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
                        "<span style=\" font-family:'Arial','sans-serif'; font-size:11pt; font-weight:700; color:#deddda; background-color:transparent;\">Stefan Kycia </span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; color:#deddda; background-color:transparent;\">(</span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; text-decoration: underline; color:#308cc6; background-color:transparent;\">skycia@uoguelph.ca</span><span style=\" font-family:'Arial','sans-serif'; font-size:11pt; color:#deddda; background-color:transparent;\">)</span></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("about_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-size:11pt; color:#deddda;\">If you found this program useful in correcting your data please cite:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu'; font-size:11pt; color:#deddda;\"><br /></p>\n"
"<p style=\" margin-top:0px; margi"
                        "n-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"docs-internal-guid-0511c0a7-7fff-5768-07c8-3b010aa178db\"></a><span style=\" font-family:'Arial','sans-serif'; font-size:10pt; color:#deddda; background-color:transparent;\">B</span><span style=\" font-family:'Arial','sans-serif'; font-size:10pt; color:#deddda; background-color:transparent;\">urns, N., Rahemtulla, A., Annett, S., Moreno, B., &amp; Kycia, S. (2023). An inclined detector geometry for improved X-ray total scattering measurements. Journal of Applied Crystallography, 56(2), 510-518, </span><a href=\"https://doi.org/10.1107/S1600576723001747\"><span style=\" font-family:'Ubuntu'; font-size:11pt; text-decoration: underline; color:#308cc6;\">https://doi.org/10.1107/S1600576723001747</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Arial','sans-serif'; font-size:10pt; color:#deddda"
                        ";\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-size:11pt; color:#deddda;\">If you have any questions about the program or wish to report any bugs please contact: </span><span style=\" font-family:'Ubuntu'; font-size:11pt; text-decoration: underline; color:#308cc6;\">AmorphousToolbox@gmail.com</span></p></body></html>", None))
    # retranslateUi

