#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
==============================================================
      Amorphous Toolbox - Image Compiler Tool - Bounds
==============================================================
This script deals with the bounds of additive and subtractive
QTreeWidget items/images, ie. if the mean of image is within
the accepted standard deviation range, or the start and stop
cycle criteria.

Author: Nick Burns, January, 20th, 2024
==============================================================
'''

import numpy as np

class Bounds:

    def __init__(self, win):
        
        self.win = win
        
        #=========================================
        #             Event Handeling
        #=========================================

        #<<<<<<<<<<<<<<Line Edits<<<<<<<<<<<<<<< 
        self.win.addStdMinBox.returnPressed.connect(self.change_bounds)
        self.win.addStdMaxBox.returnPressed.connect(self.change_bounds)
        
        self.win.subStdMinBox.returnPressed.connect(self.change_bounds)
        self.win.subStdMaxBox.returnPressed.connect(self.change_bounds)

        #<<<<<<<<<<<<<<Buttons<<<<<<<<<<<<<<< 
        self.win.addResetButton.triggered.connect(lambda: self.reset_bounds(self.win.addStdMinBox, self.win.addStdMaxBox))
        self.win.subResetButton.triggered.connect(lambda: self.reset_bounds(self.win.subStdMinBox, self.win.subStdMaxBox))
    
    #Sets image bounds to 'False' for the number of images set at the 
    #start and end of a cycle
    #===========================================================
    def start_stop_bounds(self, bounds):

        for cycle in range(len(bounds)):

            for start in range(int(self.win.DropFirstBox.text())):

                if start < len(bounds[cycle]):

                    bounds[cycle][start] = False

            for stop in range(int(self.win.DropLastBox.text())):

                if len(bounds[cycle]) - 1 - stop >= 0:

                    bounds[cycle][len(bounds[cycle]) - 1 - stop] = False

        return bounds
    
    #Merges the bounds of additive and subtractive bounds if both
    #additve and subtractive trees are populated
    #===========================================================
    def merge_bounds(self):    

        if self.win.AddAddSetButton.isChecked() == True and self.win.SubAddSetButton.isChecked() == True:

            self.win.trees.additive_parameters['Accepted']  = [np.logical_and(self.win.trees.additive_parameters['Accepted'][i], self.win.trees.subtractive_parameters['Accepted'][i]) for i in range(len(self.win.trees.additive_parameters['Accepted']))]
            self.win.trees.subtractive_parameters['Accepted'] = [np.logical_and(self.win.trees.additive_parameters['Accepted'][i], self.win.trees.subtractive_parameters['Accepted'][i]) for i in range(len(self.win.trees.additive_parameters['Accepted']))]

        elif self.win.AddAddSetButton.isChecked() == True and self.win.SubAddSetButton.isChecked() == False:

            self.win.trees.additive_parameters['Accepted'] = self.win.bounds.start_stop_bounds(self.win.trees.additive_parameters['Accepted'])
            self.win.trees.additive_parameters['Accepted'] = self.win.bounds.cycle_std_bounds(self.win.trees.additive_parameters['Normalization'], self.win.trees.additive_parameters['Accepted'], self.win.addStdMinBox, self.win.addStdMaxBox)

        elif self.win.AddAddSetButton.isChecked() == False and self.win.SubAddSetButton.isChecked() == True:

            self.win.trees.subtractive_parameters['Accepted'] = self.win.bounds.start_stop_bounds(self.win.trees.subtractive_parameters['Accepted'])
            self.win.trees.subtractive_parameters['Accepted'] = self.win.bounds.cycle_std_bounds(self.win.trees.subtractive_parameters['Normalization'], self.win.trees.subtractive_parameters['Accepted'], self.win.subStdMinBox, self.win.subStdMaxBox)
    
    #Determines if the mean of the image is within the accepted
    #standard deviation range for QTreeItems origanized by
    #cyles, if outside bounds is set to 'False'
    #===========================================================
    def cycle_std_bounds(self, norm_data, bounds, min_box, max_box):

        flat_norm_data = [img for cycle in norm_data for img in cycle]

        for cycle in range(len(bounds)):

            for img in range(len(bounds[cycle])):

                if norm_data[cycle][img] < np.average(np.array(flat_norm_data)) - (np.std(np.array(flat_norm_data)) * float(min_box.text())) or \
                   norm_data[cycle][img] > np.average(np.array(flat_norm_data)) + (np.std(np.array(flat_norm_data)) * float(max_box.text())):

                    bounds[cycle][img] = False

        del flat_norm_data

        return bounds
    
    #Resets the set standard deviations ranges on the selected
    #PixPlot and recalculates the bounds and replots the PixPlot.
    #===========================================================
    def reset_bounds(self, min_box, max_box):

        min_box.setText('4')
        max_box.setText('4')
        self.change_bounds()

    #If the standard deviation bounds are changed for the PixPlots,
    #Determines if cyles are enabled and if both additive and 
    #subtractive QTreeWidgets are populated, in order to properly
    #determine the bounds for all items/images, then updates the
    #PixPlots.
    #===========================================================
    def change_bounds(self):

        if self.win.AddImageNameTree.topLevelItemCount() != 0:

            for i in range(len(self.win.trees.additive_parameters['Accepted'])):

                for j in range(len(self.win.trees.additive_parameters['Accepted'][i])):

                    self.win.trees.additive_parameters['Accepted'][i][j] = True

            self.win.trees.additive_parameters['Accepted'] = self.start_stop_bounds(self.win.trees.additive_parameters['Accepted'])
            self.win.trees.additive_parameters['Accepted'] = self.cycle_std_bounds(self.win.trees.additive_parameters['Normalization'], self.win.trees.additive_parameters['Accepted'], self.win.addStdMinBox, self.win.addStdMaxBox)

        if self.win.SubImageNameTree.topLevelItemCount() != 0:

            for i in range(len(self.win.trees.subtractive_parameters['Accepted'])):

                for j in range(len(self.win.trees.subtractive_parameters['Accepted'][i])):

                    self.win.trees.subtractive_parameters['Accepted'][i][j] = True

            self.win.trees.subtractive_parameters['Accepted'] = self.start_stop_bounds(self.win.trees.subtractive_parameters['Accepted'])
            self.win.trees.subtractive_parameters['Accepted'] = self.cycle_std_bounds(self.win.trees.subtractive_parameters['Normalization'], self.win.trees.subtractive_parameters['Accepted'], self.win.subStdMinBox, self.win.subStdMaxBox)

        if self.win.AddImageNameTree.topLevelItemCount() != 0 or self.win.SubImageNameTree.topLevelItemCount() != 0:
            
            self.merge_bounds()
            self.win.trees.update_trees()
            self.win.selection.reselect_selected()