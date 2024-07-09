#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################
#                          Plots
#
#This script deals with the creation of PixMap, PixPlots and
#TracePlots. Custom toolbars are designed for each plot. Manipulation
#of each plot is implemented here. Additionally the calculation
#of the traces for TracePlot are perfomed here.

#Author: Nick Burns, January, 20th, 2024
##############################################################

import sys
import numpy as np
import cv2 as cv
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QLineEdit, QGridLayout
from PySide6.QtCore import QSize, QRect, QEventLoop, QTimer
from PySide6.QtGui import QIcon, QAction

from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count 

from matplotlib.backends.backend_qt5agg import  NavigationToolbar2QT as NavigationToolbar

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                        ImagePlot
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Image:

    def __init__(self, win):
        
        self.win = win
        
        #Generate the PixMap canvas, plot interactive toolbars above
        #and below. Top toolbar contains visual and saving actions,
        #bottom contains manipulative actions.
        #=============================================================
        self.win.image_view = self.win.canvas.MplCanvas(self, tight = False)
        self.win.image_view.axes.set_position([0.0, 0.0, 1, 1])
        self.win.image_toolbar = NavigationToolbar(self.win.image_view, self.win)
        self.win.image_toolbar_View = NavigationToolbar(self.win.image_view, self.win)
        
        toolbar_actions = self.win.image_toolbar.actions()
        toolbar_actions[0].setIcon(QIcon(':/Images/Resources/Icons/Home.png'))
        toolbar_actions[4].setIcon(QIcon(':/Images/Resources/Icons/Move.png'))
        toolbar_actions[5].setIcon(QIcon(':/Images/Resources/Icons/Zoom.png'))
        toolbar_actions[9].setIcon(QIcon(':/Images/Resources/Icons/Save.png'))

        for x in self.win.image_toolbar.actions(): self.win.image_toolbar.removeAction(x)

        self.win.image_toolbar.addAction(toolbar_actions[0])
        self.win.image_toolbar.addAction(toolbar_actions[4])
        self.win.image_toolbar.addAction(toolbar_actions[5])
        self.win.image_toolbar.addAction(toolbar_actions[9])
        self.win.image_toolbar.addAction(toolbar_actions[3])
        self.win.image_toolbar.addAction(toolbar_actions[10])
        self.win.image_toolbar.setIconSize(QSize(21, 21))
        
        for x in self.win.image_toolbar_View.actions(): self.win.image_toolbar_View.removeAction(x)
            
        self.win.leftSpacer = QLabel(self.win)
        self.win.leftSpacer.setFixedSize(121, 21)
        self.win.stdminBox, self.win.stdmaxBox = QLineEdit(self.win), QLineEdit(self.win)
        self.win.stdminBox.setText('1'), self.win.stdmaxBox.setText('1')
        self.win.stdminBox.setFixedSize(59, 23), self.win.stdmaxBox.setFixedSize(59, 23)
        self.win.stdminBox.setAlignment(Qt.AlignHCenter), self.win.stdmaxBox.setAlignment(Qt.AlignHCenter) 
        
        self.win.stdBox = QAction(QIcon(':/Images/Resources/Icons/Standard_Deviation.png'), 'Reset View', self.win)
        self.win.edgeButton = QAction(QIcon(':/Images/Resources/Icons/Edge.png'), 'Edge Detection', self.win)
        self.win.linesegButton = QAction(QIcon(':/Images/Resources/Icons/Line.png'), 'Plot Line Segment', self.win)
        self.win.resetButton = QAction(QIcon(':/Images/Resources/Icons/Reset.png'), 'Reset View', self.win)
        
        self.win.stdBox.setEnabled(False), self.win.edgeButton.setCheckable(True), self.win.linesegButton.setCheckable(True)
        
        self.win.image_toolbar_View.addAction(self.win.edgeButton)
        self.win.image_toolbar_View.addAction(self.win.linesegButton)
        self.win.image_toolbar_View.addAction(toolbar_actions[8])
        self.win.image_toolbar_View.addWidget(self.win.leftSpacer)
        self.win.image_toolbar_View.addAction(self.win.stdBox)
        self.win.image_toolbar_View.addWidget(self.win.stdminBox)
        self.win.image_toolbar_View.addWidget(self.win.stdmaxBox)
        self.win.image_toolbar_View.addAction(self.win.resetButton)
        self.win.image_toolbar_View.setIconSize(QSize(21, 21))
        
        layout = QVBoxLayout()
        layout.addWidget(self.win.image_toolbar)
        layout.addWidget(self.win.image_view)
        layout.addWidget(self.win.image_toolbar_View)
        layout.setAlignment(self.win.image_toolbar, Qt.AlignLeft)
        layout.setAlignment(self.win.image_toolbar_View, Qt.AlignHCenter)
        self.win.imagematplotFrame.setLayout(layout)
        self.win.image_view.axes.set(xticks = [], yticks = [])
        
        self.win.stdminBox.returnPressed.connect(self.color_bounds)
        self.win.stdmaxBox.returnPressed.connect(self.color_bounds)
        self.win.edgeButton.triggered.connect(self.edge_detection)
        self.win.resetButton.triggered.connect(self.reset_image)
        
    #Update the PixMap with the latest item/image, adjusts the color
    #scale based on the standard deviations set in QLineEdit.
    #=============================================================
    def update_image(self, img):
        
        self.win.pixmap_image = np.copy(img)

        img_std = np.std(self.win.pixmap_image)
        img_avg = np.average(self.win.pixmap_image)

        self.win.image_view.axes.cla()
        self.win.image_view.axes.imshow(self.win.pixmap_image, origin = 'lower', cmap = 'cividis', vmin = img_avg - img_std * \
                                   float(self.win.stdminBox.text()), vmax = img_avg + img_std * float(self.win.stdmaxBox.text()))
        
        self.win.image_view.axes.set(xticks = [], yticks = [])
        self.win.image_view.draw()
        self.win.show()
    
    #Clears the Pixmap to a blank canvas and resets the standard
    #deviation within QLineEdit.
    #=============================================================
    def clear_image(self):
        
        self.win.stdminBox.setText('1')
        self.win.stdmaxBox.setText('1')
        
        self.win.image_view.axes.clear()
        self.win.image_view.axes.set(xticks = [], yticks = [])
        self.win.image_view.draw()
        self.win.show()

    #Resets the PixMap to the initially selected item/image before
    #application of manipulative actions, additionally resets the
    #standard deviations within QLineEdit.
    #=============================================================
    def reset_image(self):
        
        if bool(self.win.image_view.axes.get_images()) == True:
            
            self.win.stdminBox.setText('1')
            self.win.stdmaxBox.setText('1')

            self.win.edgeButton.setChecked(False)
            self.update_image(self.win.selection.selection_parameters['Image'])
        
    #Changes the colorbounds of the plotted PixMap when the standard
    #deviations set in the QLineEdit are updated.
    #=============================================================  
    def color_bounds(self):
        
        if bool(self.win.image_view.axes.get_images()) == True:
            
            if self.win.edgeButton.isChecked() == False:

                self.update_image(self.win.selection.selection_parameters['Image'])

            else:

                self.edge_detection()
        else:
            
            self.win.stdminBox.setText('1')
            self.win.stdmaxBox.setText('1')
            
    #Calculates and plots the 'Massif' extraction of the plotted
    #PixMap image. Highlights edge features in the image.
    #=============================================================  
    def edge_detection(self):

        if bool(self.win.image_view.axes.get_images()) == True:

            if self.win.edgeButton.isChecked() == True:

                self.update_image(self.win.selection.selection_parameters['Image'] - cv.blur(self.win.selection.selection_parameters['Image'], \
                                 (int(self.win.selection.selection_parameters['Image'].shape[0] * 0.02), int(self.win.selection.selection_parameters['Image'].shape[1] * 0.02)), None, (-1, -1), cv.BORDER_DEFAULT))

            elif self.win.edgeButton.isChecked() == False:

                self.reset_image()


        else:

            if self.win.edgeButton.isChecked() == True: 
                
                self.win.edgeButton.setChecked(False)

            elif self.win.edgeButton.isChecked() == False: 
                
                self.win.edgeButton.setChecked(True)
                
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                         PixPlots
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Plot:
    
    def __init__(self, win):
        
        self.win = win
        
        #=============================================================
        #                      Additive PixPlot
        #=============================================================
        
        #Generate the additive PixPlot canvas, plots an interactive 
        #toolbar above contains visual and saving actions. Additive 
        #PixPlot shows the mean data of all loaded images to the 
        #additive image QTreeWidget.
        #=============================================================
        self.win.AddPlotView = self.win.canvas.MplCanvas(self, width = 4, height = 1)
        self.win.AddPlotView.axes.set_position([0.05, 0.225, 0.915, 0.7775])
        self.win.AddPlotToolbar = NavigationToolbar(self.win.AddPlotView, self.win)
        
        toolbar_actions = self.win.AddPlotToolbar.actions()
        toolbar_actions[0].setIcon(QIcon(':/Images/Resources/Icons/Home.png'))
        toolbar_actions[4].setIcon(QIcon(':/Images/Resources/Icons/Move.png'))
        toolbar_actions[5].setIcon(QIcon(':/Images/Resources/Icons/Zoom.png'))
        toolbar_actions[9].setIcon(QIcon(':/Images/Resources/Icons/Save.png'))

        self.win.AddLeftSpacer, self.win.AddRightSpacer = QLabel(self.win), QLabel(self.win)
        self.win.AddLeftSpacer.setFixedSize(5, 21), self.win.AddRightSpacer.setFixedSize(130, 21)
        self.win.addStdMinBox, self.win.addStdMaxBox = QLineEdit(self.win), QLineEdit(self.win)
        self.win.addStdMinBox.setText('4'), self.win.addStdMaxBox.setText('4')
        self.win.addStdMinBox.setFixedSize(59, 23), self.win.addStdMaxBox.setFixedSize(59, 23)
        self.win.addStdMinBox.setAlignment(Qt.AlignHCenter), self.win.addStdMaxBox.setAlignment(Qt.AlignHCenter)
        
        self.win.addStdButton = QAction(QIcon(':/Images/Resources/Icons/Standard_Deviation.png'), 'Reset View', self.win)
        self.win.addResetButton = QAction(QIcon(':/Images/Resources/Icons/Reset.png'), 'Reset', self.win)
        
        self.win.addStdButton.setEnabled(False)
        for x in self.win.AddPlotToolbar.actions(): self.win.AddPlotToolbar.removeAction(x)
        
        self.win.AddPlotToolbar.addWidget(self.win.AddLeftSpacer)
        self.win.AddPlotToolbar.addAction(toolbar_actions[0])
        self.win.AddPlotToolbar.addAction(toolbar_actions[4])
        self.win.AddPlotToolbar.addAction(toolbar_actions[5])
        self.win.AddPlotToolbar.addAction(toolbar_actions[9])
        self.win.AddPlotToolbar.addAction(toolbar_actions[3])
        self.win.AddPlotToolbar.addWidget(self.win.AddRightSpacer)
        self.win.AddPlotToolbar.addAction(self.win.addStdButton)
        self.win.AddPlotToolbar.addWidget(self.win.addStdMinBox)
        self.win.AddPlotToolbar.addWidget(self.win.addStdMaxBox)
        self.win.AddPlotToolbar.addAction(self.win.addResetButton)
        self.win.AddPlotToolbar.setIconSize(QSize(21, 21))
        
        layout = QVBoxLayout()
        layout.addWidget(self.win.AddPlotToolbar)
        layout.addWidget(self.win.AddPlotView)
        layout.setAlignment(self.win.AddPlotToolbar, Qt.AlignLeft)
        self.win.AddNormMatplotFrame.setLayout(layout)  
        self.win.AddPlotView.axes.set(xticks = [0, 1, 2, 3, 4, 5, 6], yticks = [], yticklabels = [])
        self.win.AddPlotView.axes.set_xticklabels([0, 1, 2, 3, 4, 5, 6], fontsize = 8)
        self.win.AddPlotView.axes.set_ylabel('Additive Intensity', fontsize = 8)
        self.win.AddPlotView.axes.set_xlabel('Number of Images', fontsize = 8)
        
        #=============================================================
        #                Generate Subtractive PixPlot
        #=============================================================
        
        #Generate the subtractive PixPlot canvas, plots an interactive 
        #toolbar above contains visual and saving actions. Subtractive
        #PixPlot shows the mean data of all loaded images to the 
        #subtractive image QTreeWidget.
        #=============================================================
        self.win.SubPlotView = self.win.canvas.MplCanvas(self, width = 4, height = 2)
        self.win.SubPlotView.axes.set_position([0.05, 0.225, 0.915, 0.7775])
        self.win.SubPlotToolbar = NavigationToolbar(self.win.SubPlotView, self.win)
        
        toolbar_actions = self.win.SubPlotToolbar.actions()
        toolbar_actions[0].setIcon(QIcon(':/Images/Resources/Icons/Home.png'))
        toolbar_actions[4].setIcon(QIcon(':/Images/Resources/Icons/Move.png'))
        toolbar_actions[5].setIcon(QIcon(':/Images/Resources/Icons/Zoom.png'))
        toolbar_actions[9].setIcon(QIcon(':/Images/Resources/Icons/Save.png'))
        
        self.win.SubLeftSpacer, self.win.SubRightSpacer = QLabel(self.win), QLabel(self.win)
        self.win.SubLeftSpacer.setFixedSize(5, 21), self.win.SubRightSpacer.setFixedSize(130, 21)
        self.win.subStdMinBox, self.win.subStdMaxBox = QLineEdit(self.win), QLineEdit(self.win)
        self.win.subStdMinBox.setText('4'), self.win.subStdMaxBox.setText('4')
        self.win.subStdMinBox.setFixedSize(59, 23), self.win.subStdMaxBox.setFixedSize(59, 23)
        self.win.subStdMinBox.setAlignment(Qt.AlignHCenter), self.win.subStdMaxBox.setAlignment(Qt.AlignHCenter) 
        
        self.win.subStdButton = QAction(QIcon(':/Images/Resources/Icons/Standard_Deviation.png'), 'Reset View', self.win)
        self.win.subResetButton = QAction(QIcon(':/Images/Resources/Icons/Reset.png'), 'Reset', self.win)
        
        self.win.subStdButton.setEnabled(False)
        for x in self.win.SubPlotToolbar.actions(): self.win.SubPlotToolbar.removeAction(x)
            
        self.win.SubPlotToolbar.addWidget(self.win.SubLeftSpacer)
        self.win.SubPlotToolbar.addAction(toolbar_actions[0])
        self.win.SubPlotToolbar.addAction(toolbar_actions[4])
        self.win.SubPlotToolbar.addAction(toolbar_actions[5])
        self.win.SubPlotToolbar.addAction(toolbar_actions[9])
        self.win.SubPlotToolbar.addAction(toolbar_actions[3])
        self.win.SubPlotToolbar.addWidget(self.win.SubRightSpacer)
        self.win.SubPlotToolbar.addAction(self.win.subStdButton)
        self.win.SubPlotToolbar.addWidget(self.win.subStdMinBox)
        self.win.SubPlotToolbar.addWidget(self.win.subStdMaxBox)
        self.win.SubPlotToolbar.addAction(self.win.subResetButton)
        self.win.SubPlotToolbar.setIconSize(QSize(21, 21))

        layout = QVBoxLayout()
        layout.addWidget(self.win.SubPlotToolbar)
        layout.addWidget(self.win.SubPlotView)
        layout.setAlignment(self.win.SubPlotToolbar, Qt.AlignLeft)
        self.win.SubNormMatplotFrame.setLayout(layout)
        self.win.SubPlotView.axes.set(xticks = [0, 1, 2, 3, 4, 5, 6], yticks = [], yticklabels = [])
        self.win.SubPlotView.axes.set_xticklabels([0, 1, 2, 3, 4, 5, 6], fontsize = 8)
        self.win.SubPlotView.axes.set_ylabel('Subtractive Intensity', fontsize = 8)
        self.win.SubPlotView.axes.set_xlabel('Number of Images', fontsize = 8)
        
    #Updates the PixPlot to the latest mean data.
    #=============================================================
    def update_plot(self, canvas, norm, bounds, std_min_box, std_max_box):

        bounds = np.hstack(bounds)
        norm = np.hstack(norm)
        
        in_indicies = np.where(bounds == True)
        out_indicies = np.where(bounds == False)
        
        ylabel_text = canvas.axes.get_ylabel()
        label_format = '{:,.0f}'

        canvas.axes.cla()
        canvas.axes.scatter(in_indicies, norm[in_indicies], marker = 'o', c = 'mediumblue')
        canvas.axes.scatter(out_indicies, norm[out_indicies], marker = 'o', c = 'gold')
        
        if self.win.selection.selection_parameters['Total_Index'] != None:

            if self.win.selection.selection_parameters['Total_Index'] != None:
            
                canvas.axes.scatter(self.win.selection.selection_parameters['Total_Index'], norm[self.win.selection.selection_parameters['Total_Index']], marker = 'o', c = 'deepskyblue', edgecolors = 'black')
                
        plot_std = np.std(norm)
        plot_avg = np.average(norm)

        if plot_avg - plot_std * float(std_min_box.text()) * 1.25 != plot_avg + plot_std * float(std_min_box.text()) * 1.25:
            
            canvas.axes.plot(np.full_like(norm, plot_avg + plot_std * float(std_max_box.text())), '-', color = 'black')
            canvas.axes.plot(np.full_like(norm, plot_avg - plot_std * float(std_min_box.text())), '-', color = 'black')
            canvas.axes.set_ylim([plot_avg - plot_std * float(std_min_box.text()) * 1.25, plot_avg + plot_std * float(std_max_box.text()) * 1.25])
        
        canvas.axes.set(yticks = [], yticklabels = [])
        canvas.axes.set_xticks(canvas.axes.get_xticks().tolist()[1:-1])
        canvas.axes.set_xticklabels([label_format.format(x) for x in canvas.axes.get_xticks().tolist()], fontsize = 8)
        canvas.axes.set_ylabel(ylabel_text, fontsize = 8)
        canvas.axes.set_xlabel('Number of Images', fontsize = 8)
        canvas.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        canvas.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        canvas.draw()

            
    #Clears the PixPlot to a blank canvas.
    #=============================================================
    def clear_plot(self, canvas):
        
        ylabel_text = canvas.axes.get_ylabel()
        
        canvas.axes.clear()
        canvas.axes.set(xticks = [0, 1, 2, 3, 4, 5, 6], yticks = [], yticklabels = [])
        canvas.axes.set_xticklabels([0, 1, 2, 3, 4, 5, 6], fontsize = 8)
        canvas.axes.set_ylabel(ylabel_text, fontsize = 8)
        canvas.axes.set_xlabel('Number of Images', fontsize = 8)
        canvas.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        canvas.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        canvas.draw()
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                         TracePlots
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Trace:
    
    def __init__(self, win):
        
        self.win = win
        
        #Generate the TracePlot canvas, plots an interactive 
        #toolbar above and below. Toolbar above contains visual and saving 
        #actions. Toolbar below contains trace stacking options for the 
        #selected trace. TracePlot shows the trace of the the selected
        #two points on the PixMap.
        #=============================================================
        self.win.pixmapTabs.removeTab(1)
        
        self.win.traceView = self.win.canvas.MplCanvas(self, tight = False)
        self.win.traceView.axes.set_position([0.04, 0.04, 0.935, 0.99])
        self.win.traceToolbar = NavigationToolbar(self.win.traceView, self.win)
        self.win.traceToolbar_View = NavigationToolbar(self.win.traceView, self.win)
        self.win.traceToolbar.hide()
        self.win.traceToolbar_View.hide()

        toolbar_actions = self.win.traceToolbar.actions()
        toolbar_actions[0].setIcon(QIcon(':/Images/Resources/Icons/Home.png'))
        toolbar_actions[4].setIcon(QIcon(':/Images/Resources/Icons/Move.png'))
        toolbar_actions[5].setIcon(QIcon(':/Images/Resources/Icons/Zoom.png'))
        toolbar_actions[9].setIcon(QIcon(':/Images/Resources/Icons/Save.png'))

        for x in self.win.traceToolbar.actions(): self.win.traceToolbar.removeAction(x)

        self.win.traceToolbar.addAction(toolbar_actions[0])
        self.win.traceToolbar.addAction(toolbar_actions[4])
        self.win.traceToolbar.addAction(toolbar_actions[5])
        self.win.traceToolbar.addAction(toolbar_actions[9])
        self.win.traceToolbar.addAction(toolbar_actions[3])
        self.win.traceToolbar.addAction(toolbar_actions[10])
        self.win.traceToolbar.setIconSize(QSize(21, 21))

        toolbar_view_actions = self.win.traceToolbar_View.actions()
        for x in self.win.traceToolbar_View.actions(): self.win.traceToolbar_View.removeAction(x)

        self.win.compileButton = QAction(QIcon(':/Images/Resources/Icons/Compile.png'), 'Compile Selected Image Set Traces', self.win)
        self.win.stackButton = QAction(QIcon(':/Images/Resources/Icons/Stack.png'), 'Stack Selected Image Set Traces', self.win)
        self.win.selectedButton = QAction(QIcon(':/Images/Resources/Icons/Single.png'), 'Selected Image Trace', self.win)
        self.win.trashButton = QAction(QIcon(':/Images/Resources/Icons/Trash.png'), 'Remove Trace', self.win)

        self.win.compileButton.setCheckable(True), self.win.stackButton.setCheckable(True), self.win.selectedButton.setCheckable(True)
        self.win.selectedButton.setChecked(True)

        self.win.traceSpacer = QLabel(self.win)
        self.win.traceSpacer.setFixedSize(220, 21)

        self.win.traceToolbar_View.addAction(self.win.compileButton)
        self.win.traceToolbar_View.addAction(self.win.stackButton)
        self.win.traceToolbar_View.addAction(self.win.selectedButton)
        self.win.traceToolbar_View.addAction(toolbar_view_actions[3])
        self.win.traceToolbar_View.addWidget(self.win.traceSpacer)
        self.win.traceToolbar_View.addAction(toolbar_view_actions[8])
        self.win.traceToolbar_View.addAction(self.win.trashButton)
        self.win.traceToolbar_View.setIconSize(QSize(21, 21))
        
        self.win.traceWidget = QFrame(self.win)
        self.win.traceWidget.setFrameShape(QFrame.NoFrame)
        self.win.traceWidget.setMinimumWidth(401), self.win.traceWidget.setMinimumHeight(473)
        self.win.traceWidget.setMaximumWidth(401), self.win.traceWidget.setMaximumHeight(473)
        self.win.traceWidget.setFrameRect(QRect(0, 0, 401, 473))
        self.win.traceWidget.hide()
        
        self.win.traceFrame = QFrame(self.win)
        self.win.traceFrame.setFrameShape(QFrame.StyledPanel)
        self.win.traceFrame.setMinimumWidth(401), self.win.traceFrame.setMinimumHeight(471)
        self.win.traceFrame.setMaximumWidth(401), self.win.traceFrame.setMaximumHeight(471)
        self.win.traceFrame.setFrameRect(QRect(0, 0, 401, 471))
        self.win.traceFrame.hide()

        self.traceWidgetLayout = QGridLayout()
        self.traceWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.traceWidgetLayout.setSpacing(0)
        self.traceWidgetLayout.addWidget(self.win.traceFrame)
        
        self.traceFrameLayout = QVBoxLayout()
        self.traceFrameLayout.addWidget(self.win.traceToolbar)
        self.traceFrameLayout.addWidget(self.win.traceView)
        self.traceFrameLayout.addWidget(self.win.traceToolbar_View)
        self.traceFrameLayout.setAlignment(self.win.traceToolbar, Qt.AlignLeft)
        self.traceFrameLayout.setAlignment(self.win.traceToolbar_View, Qt.AlignHCenter)
        
        self.win.trashButton.triggered.connect(self.clear_trace)
        self.win.selectedButton.triggered.connect(self.selected_plot_logic)
        self.win.stackButton.triggered.connect(self.stack_plot_logic)
        self.win.compileButton.triggered.connect(self.compile_plot_logic)
        self.win.linesegButton.toggled.connect(self.draw_line_segment)
        self.win.image_view.mpl_connect("button_press_event", self.pick_point)
        
    #Enabling the line segment button enables the action of
    #selecting points on the Pixmap. If a trace has already been
    #selected disabling the line segment button clears the trace.
    #=============================================================
    def draw_line_segment(self):
        
        if self.win.linesegButton.isChecked() == True:
            
            if bool(self.win.image_view.axes.get_images()) == True:
                
                self.win.anchor_count = 0
                
            else:
                
                self.win.linesegButton.setChecked(False)
        
        elif self.win.linesegButton.isChecked() == False:
            
            if self.win.pixmapTabs.count() > 1:
                
                self.clear_trace()
        
    #Selecting points on the Pixmap, the first selected point is 
    #plotted. The second selected point is plotted and a trace is 
    #created from the first point to the second. Once the trace is 
    #created another tab is added to the QTabWidget. Selecting a 
    #Third point clears the trace and is considered to be the first
    #point repeating the cycle.
    #=============================================================
    def pick_point(self, event):
        
        if bool(self.win.image_view.axes.get_images()) == True:
            
            if self.win.linesegButton.isChecked() == True:
                
                if event.xdata != None and event.ydata != None:
                    
                    if self.win.anchor_count == 0:

                        self.win.anchor_x, self.win.anchor_y = [], []
                        self.win.anchor_x.append(int(np.round(event.xdata))), self.win.anchor_y.append(int(np.round(event.ydata)))
                        self.win.anchor_1 = self.win.image_view.axes.scatter(self.win.anchor_x[0], \
                                            self.win.anchor_y[0], c = 'deepskyblue', edgecolors = 'black')
                        self.win.image_view.draw()
                        self.win.show()
                        
                        self.win.anchor_count += 1
                        
                    elif self.win.anchor_count == 1:
                        
                        if self.win.anchor_x[0] != int(np.round(event.xdata)) and self.win.anchor_y[0] != int(np.round(event.ydata)):
                        
                            self.win.anchor_x.append(int(np.round(event.xdata))), self.win.anchor_y.append(int(np.round(event.ydata)))
                            self.win.anchor_2 = self.win.image_view.axes.scatter(self.win.anchor_x[1], self.win.anchor_y[1], c = 'deepskyblue', edgecolors = 'black')
                            
                            self.calc_trace()
                            self.win.lineseg = self.win.image_view.axes.plot(self.win.line_x, self.win.line_y, c = 'deepskyblue')[0]
                            self.win.image_view.draw()
                            
                            self.win.pixmapTabs.insertTab(1, self.win.traceWidget, 'Trace')
                            self.win.traceWidget.setLayout(self.traceWidgetLayout)
                            self.win.traceFrame.setLayout(self.traceFrameLayout)
                            self.win.traceWidget.show()
                            self.win.traceFrame.show()
                            self.win.traceToolbar.show()
                            self.win.traceToolbar_View.show()
                            self.clear_traceplot()

                            self.win.traceView.axes.plot(self.win.selection.selection_parameters['Image'][self.win.line_y, self.win.line_x])
                            self.win.traceView.axes.set(xticks = [], xticklabels = [], yticks = [], yticklabels = [])
                            self.win.traceView.axes.set_ylim([self.win.traceView.axes.get_ylim()[0] - self.win.traceView.axes.get_ylim()[1] * 0.025, \
                                                              self.win.traceView.axes.get_ylim()[1] * 1.05])
                            self.win.traceView.axes.set_ylabel('Intensity', fontsize = 8)
                            self.win.traceView.axes.set_xlabel('Number of Selected Points', fontsize = 8)
                            self.win.traceView.axes.format_coord = lambda x, y: 'x={:g}, y={:g}'.format(x, y)
                            self.win.traceView.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
                            self.win.traceView.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
                            self.win.traceView.draw()
                            
                            loop = QEventLoop()
                            QTimer.singleShot(500, loop.quit)
                            loop.exec_()

                            self.win.pixmapTabs.setCurrentIndex(1)

                            self.win.anchor_count += 1
                        
                    else:
                        
                        self.win.pixmapTabs.removeTab(1)
                        self.win.anchor_1.remove(), self.win.anchor_2.remove(), self.win.lineseg.remove()
                        
                        del self.win.anchor_1, self.win.anchor_2, self.win.lineseg
                        
                        self.win.image_view.draw()
                        self.win.show()
                        
                        self.win.anchor_x, self.win.anchor_y = [], []
                        self.win.anchor_x.append(int(np.round(event.xdata))), self.win.anchor_y.append(int(np.round(event.ydata)))
                        self.win.anchor_1 = self.win.image_view.axes.scatter(self.win.anchor_x[0], \
                                        self.win.anchor_y[0], c = 'deepskyblue', edgecolors = 'black')
                        self.win.image_view.draw()
                        self.win.show()
                        
                        self.win.anchor_count = 1
            
    #Calculate the equation of a line between the two selected points
    #calculate the line for number of y pixels, round the coordinates
    #to nearest integer values and filter the indicies to contain only
    #the unique coordinates. Select the unique values along the trace.
    #=============================================================
    def calc_trace(self):
        
        m = (self.win.anchor_y[1] - self.win.anchor_y[0]) / (self.win.anchor_x[1] - self.win.anchor_x[0])
        b = self.win.anchor_y[0] - m * self.win.anchor_x[0]

        self.win.line_size = np.max(np.shape(self.win.selection.selection_parameters['Image']))
        self.win.line_x = np.linspace(self.win.anchor_x[0], self.win.anchor_x[1], self.win.line_size)
        self.win.line_y = np.round(self.win.line_x * m + b).astype(int)
        self.win.line_x = np.round(self.win.line_x).astype(int)

        line_index = np.sort(np.unique(self.win.line_y * np.shape(self.win.selection.selection_parameters['Image'])[0] + self.win.line_x, return_index = True)[1])
        self.win.line_x = self.win.line_x[line_index]
        self.win.line_y = self.win.line_y[line_index]
            
    #Clear the TracePlot to a blank canvas
    #=============================================================
    def clear_traceplot(self):
        
        self.win.traceView.axes.clear()
        self.win.traceView.axes.set(xticks = [], yticks = [])
        self.win.traceView.draw()
        self.win.show()
                 
    #Clears a selected trace by removing the added 'Trace' tab in the
    #QTabWidget, and clearing the plotted trace from the PixMap
    #=============================================================
    def clear_trace(self):
        
        self.win.pixmapTabs.removeTab(1)
        
        self.win.selectedButton.setChecked(True)
        self.win.compileButton.setChecked(False)
        self.win.stackButton.setChecked(False)
        
        self.win.anchor_1.remove(), self.win.anchor_2.remove(), self.win.lineseg.remove()
        del self.win.anchor_1, self.win.anchor_2, self.win.lineseg
        
        self.win.image_view.draw()
        self.win.show()
        
        self.win.anchor_count = 0
        
    #Determine if the selected trace is already plotted on the TracePlot
    #if True the selected trace button is disabled, if False begins
    #plotting the selected trace in the TracePlot.
    #=============================================================
    def selected_plot_logic(self):
        
        if self.win.selectedButton.isChecked() == True:
            
            self.win.compileButton.setChecked(False)
            self.win.stackButton.setChecked(False)
            
            self.clear_traceplot()
            
            self.selected_plot()
            
        elif self.win.selectedButton.isChecked() == False:
            
            self.win.selectedButton.setChecked(True)
            
    #Plots the selected trace in the TracePlot
    #=============================================================
    def selected_plot(self):
        
        self.win.traceView.axes.plot(self.win.selection.selection_parameters['Image'][self.win.line_y, self.win.line_x])
        self.win.traceView.axes.set(xticks = [], xticklabels = [], yticks = [], yticklabels = [])
        self.win.traceView.axes.set_ylim([self.win.traceView.axes.get_ylim()[0] - self.win.traceView.axes.get_ylim()[1] * 0.025, self.win.traceView.axes.get_ylim()[1] * 1.05])
        self.win.traceView.axes.set_ylabel('Intensity', fontsize = 8)
        self.win.traceView.axes.set_xlabel('Number of Selected Points', fontsize = 8)
        self.win.traceView.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.draw()
    
    #Determine if one of the image QTreeWidgets is selected, if True
    #begin plotting the stack trace on the TracePlot, if False,
    #disable the stack trace option.
    #=============================================================
    def stack_plot_logic(self):
         
        if self.win.selection.selection_parameters['Type'] == 'Additive Images' or \
           self.win.selection.selection_parameters['Type'] == 'Subtractive Images' or \
           self.win.selection.selection_parameters['Type'] == 'Total Images':
            
            if self.win.stackButton.isChecked() == True:

                self.win.selectedButton.setChecked(False)
                self.win.compileButton.setChecked(False)
                self.clear_traceplot()
                self.stack_plot()

            elif self.win.stackButton.isChecked() == False:

                self.win.stackButton.setChecked(True)
                
        else:
            
            self.win.stackButton.setChecked(False)
            self.win.compileButton.setChecked(False)

    
    def compile_image(self, paths, norms, avg_norm, slider, index):

        return index, np.rot90(self.win.files.load_image(paths[index]), -slider.value()) / norms[index] * avg_norm

    def stack_plot(self):
        
        if self.win.selection.selection_parameters['Type'] == 'Additive Images':

            if self.win.AddImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.additive_parameters['Accepted']) == True)

                add_norms = np.hstack(self.win.trees.additive_parameters['Normalization'])[in_indicies]
                add_names = np.hstack(self.win.trees.additive_parameters['Names'])[in_indicies]

                avg_norm = np.average(add_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, add_names, add_norms, avg_norm, self.win.AddRotationalSlider), range(len(in_indicies[0])))):

                self.win.traceView.axes.plot(results[1][self.win.line_y, self.win.line_x]) 

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

        elif self.win.selection.selection_parameters['Type'] == 'Subtractive Images':

            if self.win.SubImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.subtractive_parameters['Accepted']) == True)

                sub_norms = np.hstack(self.win.trees.subtractive_parameters['Normalization'])[in_indicies]
                sub_names = np.hstack(self.win.trees.subtractive_parameters['Names'])[in_indicies]

                avg_norm = np.average(sub_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, sub_names, sub_norms, avg_norm, self.win.SubRotationalSlider), range(len(in_indicies[0])))):

                self.win.traceView.axes.plot(results[1][self.win.line_y, self.win.line_x]) 

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

        elif self.win.selection.selection_parameters['Type'] == 'Total Images':

            mul_img = self.win.files.load_correction()

            compile_norms, add_names, sub_names = np.ones((1)), np.ones((1)), np.ones((1))

            if self.win.AddImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.additive_parameters['Accepted']) == True)

                add_norms = np.hstack(self.win.trees.additive_parameters['Normalization'])[in_indicies]
                add_names = np.hstack(self.win.trees.additive_parameters['Names'])[in_indicies]

                compile_norms = add_norms + compile_norms

                avg_compile_norm = np.average(compile_norms)

            if self.win.SubImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.subtractive_parameters['Accepted']) == True)

                sub_norms = np.hstack(self.win.trees.subtractive_parameters['Normalization'])[in_indicies]
                sub_names = np.hstack(self.win.trees.subtractive_parameters['Names'])[in_indicies]

                compile_norms = -sub_norms + compile_norms

                avg_compile_norm = np.average(compile_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.win.files.compile_image, add_names, sub_names, compile_norms, avg_compile_norm), range(len(in_indicies[0])))):

                self.win.traceView.axes.plot((results[1] / mul_img)[self.win.line_y, self.win.line_x])

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

        self.win.traceView.axes.set(xticks = [], xticklabels = [], yticks = [], yticklabels = [])
        self.win.traceView.axes.set_ylim([self.win.traceView.axes.get_ylim()[0] - self.win.traceView.axes.get_ylim()[1] * 0.025, self.win.traceView.axes.get_ylim()[1] * 1.05])
        self.win.traceView.axes.set_ylabel('Intensity', fontsize = 8)
        self.win.traceView.axes.set_xlabel('Number of Selected Points', fontsize = 8)
        self.win.traceView.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.draw()
        
    #Determine if one of the image QTreeWidgets is selected, if True
    #begin plotting the compile trace on the TracePlot, if False,
    #disable the compile trace option.
    #=============================================================
    def compile_plot_logic(self):
        
        if self.win.selection.selection_parameters['Type'] == 'Additive Images' or \
           self.win.selection.selection_parameters['Type'] == 'Subtractive Images' or \
           self.win.selection.selection_parameters['Type'] == 'Total Images':
            
            if self.win.compileButton.isChecked() == True:

                self.win.selectedButton.setChecked(False)
                self.win.stackButton.setChecked(False)
                self.clear_traceplot()
                self.compile_plot()

            elif self.win.compileButton.isChecked() == False:

                self.win.compileButton.setChecked(True)
                
        else:
            
            self.win.stackButton.setChecked(False)
            self.win.compileButton.setChecked(False)
         
    #Generate a compile of traces from the selected image QTreeWidget
    #and plot the compilation on the TracePlot.
    #=============================================================
    def compile_plot(self):
        
        if self.win.selection.selection_parameters['Type'] == 'Additive Images':

            if self.win.AddImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.additive_parameters['Accepted']) == True)

                add_norms = np.hstack(self.win.trees.additive_parameters['Normalization'])[in_indicies]
                add_names = np.hstack(self.win.trees.additive_parameters['Names'])[in_indicies]

                avg_norm = np.average(add_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, add_names, add_norms, avg_norm, self.win.AddRotationalSlider), range(len(in_indicies[0])))):

                if count == 0:

                    total_img = results[1]

                else:

                    total_img += results[1]

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

        elif self.win.selection.selection_parameters['Type'] == 'Subtractive Images':

            if self.win.SubImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.subtractive_parameters['Accepted']) == True)

                sub_norms = np.hstack(self.win.trees.subtractive_parameters['Normalization'])[in_indicies]
                sub_names = np.hstack(self.win.trees.subtractive_parameters['Names'])[in_indicies]

                avg_norm = np.average(sub_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, sub_names, sub_norms, avg_norm, self.win.SubRotationalSlider), range(len(in_indicies[0])))):

                if count == 0:

                    total_img = results[1]

                else:

                    total_img += results[1]

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

        elif self.win.selection.selection_parameters['Type'] == 'Total Images':

            mul_img = self.win.files.load_correction()

            compile_norms, add_names, sub_names = np.ones((1)), np.ones((1)), np.ones((1))

            if self.win.AddImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.additive_parameters['Accepted']) == True)

                add_norms = np.hstack(self.win.trees.additive_parameters['Normalization'])[in_indicies]
                add_names = np.hstack(self.win.trees.additive_parameters['Names'])[in_indicies]

                compile_norms = add_norms + compile_norms

                avg_compile_norm = np.average(compile_norms)

            if self.win.SubImageNameTree.topLevelItemCount() != 0:

                in_indicies = np.where(np.hstack(self.win.trees.subtractive_parameters['Accepted']) == True)

                sub_norms = np.hstack(self.win.trees.subtractive_parameters['Normalization'])[in_indicies]
                sub_names = np.hstack(self.win.trees.subtractive_parameters['Names'])[in_indicies]

                compile_norms = -sub_norms + compile_norms

                avg_compile_norm = np.average(compile_norms)

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(in_indicies[0]))

            pool = Pool(cpu_count())
            for count, results in enumerate(pool.imap_unordered(partial(self.win.files.compile_image, add_names, sub_names, compile_norms, avg_compile_norm), range(len(in_indicies[0])))):

                if count == 0:

                    total_img = results[1]

                else:

                    total_img += results[1]

                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

            total_img /= mul_img
        
        self.win.traceView.axes.plot(total_img[self.win.line_y, self.win.line_x])
        self.win.traceView.axes.set(xticks = [], xticklabels = [], yticks = [], yticklabels = [])
        self.win.traceView.axes.set_ylim([self.win.traceView.axes.get_ylim()[0] - self.win.traceView.axes.get_ylim()[1] * 0.025, self.win.traceView.axes.get_ylim()[1] * 1.05])
        self.win.traceView.axes.set_ylabel('Intensity', fontsize = 8)
        self.win.traceView.axes.set_xlabel('Number of Selected Points', fontsize = 8)
        self.win.traceView.axes.xaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.axes.yaxis.label.set_color((0.89, 0.89, 0.89, 1.0))
        self.win.traceView.draw()