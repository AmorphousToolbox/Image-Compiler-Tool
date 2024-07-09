#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##################################################################
#                          Canvas
#
#This script deals with the creation of "Matplotlib" canvases
#for attachment to GUI layouts. Additionally unique plotting 
#functions are defined here such as the plotting of a cube frame.

#Author: Nick Burns, January, 20th, 2024
#################################################################

#Keep this here, need to import PySide6 before
#matplotlib so that the correct backed is loaded. 
import PySide6.QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent = None, width = 1, height = 1, tight = True):
        
        self.face_color = (49. / 255., 63. / 255., 80. / 255.)
        self.axes_color = (0.89, 0.89, 0.89, 1.0)
        
        self.fig = Figure(figsize = (width, height), dpi = 100, facecolor = self.face_color)
        self.axes = self.fig.add_subplot(111)
        self.axes.margins(x = 0, y = 0)
        self.axes.xaxis.label.set_color(self.axes_color)
        self.axes.yaxis.label.set_color(self.axes_color)
        self.axes.tick_params(axis = 'x', colors = self.axes_color)
        self.axes.tick_params(axis = 'y', colors = self.axes_color)
        self.axes.set_facecolor(self.axes_color)
        
        if tight == True:
            
            self.fig.tight_layout()
            
        super(MplCanvas, self).__init__(self.fig)