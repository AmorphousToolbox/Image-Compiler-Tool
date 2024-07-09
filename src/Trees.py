#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
===================================================================
Amorphous Toolbox - Image Compiler Tool - Trees




Author: Nick Burns, January, 20th, 2024
===================================================================
'''

import os
import numpy as np

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtGui import QBrush, QColor

from functools import partial
from multiprocessing.pool import ThreadPool as Pool

class Trees:
    '''
    This class deals with the adding and removing of items to the
    additive, subtractive and multiplicative image QTreeWidgets.
    '''

    def __init__(self, win):
        '''
        Create the storage for the image trees and sets the event handlers 
        for the sliders, buttons and menu actions.
        '''
        
        self.win = win

        #=========================================
        #                  Data
        #=========================================
        
        self.additive_parameters = {'Names': [],
                                    'Accepted': [],
                                    'Normalization': []}
        
        self.subtractive_parameters = {'Names': [],
                                       'Accepted': [],
                                       'Normalization': []}
        
        self.multiplicative_parameters = {'Name': None}

        #=========================================
        #             Event Handeling
        #=========================================
        
        #<<<<<<<<<<<<<<Sliders<<<<<<<<<<<<<<< 
        self.win.AddRotationalSlider.valueChanged.connect(lambda: self.update_rotation(self.win.AddRotationalSlider, self.win.AddRotationalLabel))
        self.win.SubRotationalSlider.valueChanged.connect(lambda: self.update_rotation(self.win.SubRotationalSlider, self.win.SubRotationalLabel))
        self.win.MulCorrRotationalSlider.valueChanged.connect(lambda: self.update_rotation(self.win.MulCorrRotationalSlider, self.win.MulCorrRotationalLabel))
        
        #<<<<<<<<<<<<<<Buttons<<<<<<<<<<<<<<< 
        self.win.AddAddSetButton.clicked.connect(lambda: self.add_set_logic(self.win.AddImageNameTree, self.win.AddPlotView, self.win.AddAddSetButton, self.win.AddRemoveSetButton, self.additive_parameters, self.win.addStdMinBox, self.win.addStdMaxBox))
        self.win.SubAddSetButton.clicked.connect(lambda: self.add_set_logic(self.win.SubImageNameTree, self.win.SubPlotView, self.win.SubAddSetButton, self.win.SubRemoveSetButton, self.subtractive_parameters, self.win.subStdMinBox, self.win.subStdMaxBox))
        self.win.MulAddCorrButton.clicked.connect(self.add_corr)
        
        self.win.AddRemoveSetButton.clicked.connect(lambda: self.remove_set(self.win.AddImageNameTree, self.win.AddPlotView, self.win.AddAddSetButton, self.win.AddRemoveSetButton, self.additive_parameters))
        self.win.SubRemoveSetButton.clicked.connect(lambda: self.remove_set(self.win.SubImageNameTree, self.win.SubPlotView, self.win.SubAddSetButton, self.win.SubRemoveSetButton, self.subtractive_parameters))
        self.win.MulRemoveCorrButton.clicked.connect(self.remove_corr)

        self.win.AddSwapSetButton.clicked.connect(self.swap_set)
        self.win.SubSwapSetButton.clicked.connect(self.swap_set)

        #<<<<<<<<<<<<<<Spinboxs<<<<<<<<<<<<<<<
        self.win.CyclesBox.valueChanged.connect(self.update_cycles)
        self.win.DropFirstBox.valueChanged.connect(self.win.bounds.change_bounds)
        self.win.DropLastBox.valueChanged.connect(self.win.bounds.change_bounds)

        #<<<<<<<<<<<<<<Actions<<<<<<<<<<<<<<<
        self.win.actionAddAdditiveImages.triggered.connect(lambda: self.add_set(self.win.AddImageNameTree, self.win.AddPlotView, self.win.AddAddSetButton, self.win.AddRemoveSetButton, self.additive_parameters, self.win.addStdMinBox, self.win.addStdMaxBox))
        self.win.actionAddSubtractiveImages.triggered.connect(lambda: self.add_set(self.win.SubImageNameTree, self.win.SubPlotView, self.win.SubAddSetButton, self.win.SubRemoveSetButton, self.subtractive_parameters, self.win.subStdMinBox, self.win.subStdMaxBox))
        self.win.actionAddMultiplicativeCorrection.triggered.connect(self.add_corr)

        self.win.actionRemoveAdditiveImages.triggered.connect(lambda: self.remove_set(self.win.AddImageNameTree, self.win.AddPlotView, self.win.AddAddSetButton, self.win.AddRemoveSetButton, self.additive_parameters))
        self.win.actionRemoveSubtractiveImages.triggered.connect(lambda: self.remove_set(self.win.SubImageNameTree, self.win.SubPlotView, self.win.SubAddSetButton, self.win.SubRemoveSetButton, self.subtractive_parameters))
        self.win.actionRemoveMultiplicativeCorrection.triggered.connect(self.remove_corr)

    def add_set_logic(self, tree, plot, add_button, remove_button, image_parameters, min_box, max_box):
        '''
        User is attempting to add a set of images to the additive or subtractive 
        image trees. This logic determines whether or not that operation should 
        procceed. In either case the buttons are set to their appropriate states.
        '''
        
        if tree.topLevelItemCount() == 0:
            
            remove_button.setChecked(False)

            image_parameters['Names'] = self.win.files.browse_files()

            if len(image_parameters['Names']) != 0:

                if len(self.additive_parameters['Names']) != 0 and len(self.subtractive_parameters['Names']) != 0:

                    if len(np.hstack(self.additive_parameters['Names'])) != len(np.hstack(self.subtractive_parameters['Names'])):

                        self.win.messaging.error_message('Incorrect Number of Imports', 'The number of imports must be the same for both additive and subtractive images!')
                        
                        image_parameters['Names'] = []
                        image_parameters['Accepted'] = []
                        image_parameters['Normalization'] = []

                        add_button.setChecked(False)
                        remove_button.setChecked(True)

                    else:

                        self.add_set(tree, plot, image_parameters, min_box, max_box)

                else:

                    self.add_set(tree, plot, image_parameters, min_box, max_box)

            else:

                add_button.setChecked(False)
                remove_button.setChecked(True)

        else:

            add_button.setChecked(True)

    def add_set(self, tree, plot, image_parameters, min_box, max_box):
        '''
        Adds a list of image names to the additive or subtractive and total 
        image trees. The sum of intenisty for each image is calculated and 
        then plotted.
        '''

        self.win.FileProgressBar.setValue(0)
        self.win.FileProgressBar.setMaximum(len(image_parameters['Names']))

        image_parameters['Accepted'] = np.array_split(np.array([True for _ in range(len(image_parameters['Names']))]), int(self.win.CyclesBox.text()), axis = 0)
        image_parameters['Names'] = np.array_split(image_parameters['Names'], int(self.win.CyclesBox.text()), axis = 0)

        if len(image_parameters['Names']) > 0:

            image_parameters['Normalization'] = np.zeros(len(np.hstack(image_parameters['Names'])))

            pool = Pool(os.cpu_count())
                                
            for count, results in enumerate(pool.imap_unordered(partial(self.normalization_factors, np.hstack(image_parameters['Names'])), range(len(np.hstack(image_parameters['Names']))))):
                
                image_parameters['Normalization'][results[0]] = results[1]
                self.win.FileProgressBar.setValue(count + 1)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

            image_parameters['Normalization'] = np.array_split(np.array(image_parameters['Normalization']), int(self.win.CyclesBox.text()), axis = 0)

            image_parameters['Accepted'] = self.win.bounds.start_stop_bounds(image_parameters['Accepted'])
            image_parameters['Accepted'] = self.win.bounds.cycle_std_bounds(image_parameters['Normalization'], image_parameters['Accepted'], min_box, max_box)
            self.win.bounds.merge_bounds()
            
            self.populate_tree(self.win.TotalImageNameTree, np.array_split(np.array(['Image_' + str(i) for i in range(len(np.hstack(image_parameters['Names'])))]), int(self.win.CyclesBox.text())), image_parameters['Accepted'])
            self.populate_tree(tree, image_parameters['Names'], image_parameters['Accepted'])
            
            self.win.plot.update_plot(plot, image_parameters['Normalization'], image_parameters['Accepted'], min_box, max_box)
            
        else:
            
            self.win.add_button.setChecked(False)

            image_parameters['Names'] = []
            image_parameters['Accepted'] = []
            image_parameters['Normalization'] = []

    def add_corr(self):
        '''
        Image is added to the multiplictive correction QTreeWidget,
        disables the add button until the image is removed.
        '''
        
        if self.win.MulCorrNameTree.topLevelItemCount() == 0:
            
            self.multiplicative_parameters['Name'] = self.win.files.browse_file()

            if len(self.multiplicative_parameters['Name']) != 0:
                
                self.win.MulRemoveCorrButton.setChecked(False)

                self.win.MulCorrNameTree.clear()
                self.win.MulCorrNameTree.addTopLevelItem(QTreeWidgetItem([os.path.basename(self.multiplicative_parameters['Name'])], 0))

            else:

                self.win.MulAddCorrButton.setChecked(False)
                self.win.MulRemoveCorrButton.setChecked(True)
            
        else:
            
            self.win.MulAddCorrButton.setChecked(True)
            self.win.MulRemoveCorrButton.setChecked(False)

    def remove_set(self, tree, plot, add_button, remove_button, image_parameters):
        '''
        Items/Images are removed from the additive image QTreeWidget
        disables the remove button until a items/images are added.     
        '''

        remove_button.setChecked(True)
        
        if tree.topLevelItemCount() != 0:

            tree.clear()
            add_button.setChecked(False)

            if self.win.AddImageNameTree.topLevelItemCount() == 0 and self.win.SubImageNameTree.topLevelItemCount() == 0:
                
                self.win.TotalImageNameTree.clear()

            self.win.plot.clear_plot(plot)

            if self.get_tree() != None:

                if self.get_tree().currentIndex().parent().row() == -1:
                    
                    self.win.selection.selected_cycle()

                else:

                    self.win.selection.selected_item()
            
            image_parameters['Names'] = []
            image_parameters['Normalization'] = []
            image_parameters['Accepeted'] = []
            
            self.win.bounds.change_bounds()

    def swap_set(self):
        '''
        Images in the additive and subtractive trees are swapped. Associated
        widget state of sliders and buttons are additionally swapped. The selected
        image is the replotted using the new swaped order of operations.
        '''

        self.additive_parameters, self.subtractive_parameters = self.subtractive_parameters.copy(), self.additive_parameters.copy()

        tmp_min, tmp_max = self.win.addStdMinBox.text(), self.win.addStdMaxBox.text()

        self.win.addStdMinBox.setText(self.win.subStdMinBox.text()), self.win.addStdMaxBox.setText(self.win.subStdMaxBox.text())
        self.win.subStdMinBox.setText(tmp_min), self.win.subStdMaxBox.setText(tmp_max)

        selected_tree = self.get_tree()

        self.win.AddImageNameTree.clear()
        self.win.SubImageNameTree.clear()

        self.win.plot.clear_plot(self.win.AddPlotView)
        self.win.plot.clear_plot(self.win.SubPlotView)

        self.update_trees()

        if selected_tree != None:

            self.win.selection.swap_selected()

        tmp = self.win.AddRotationalSlider.value()

        self.win.AddRotationalSlider.setValue(self.win.SubRotationalSlider.value())
        self.win.SubRotationalSlider.setValue(tmp)

        if self.win.selection.selection_parameters['Type'] == 'Total Images':

            self.win.selection.selected_item()

    def get_tree(self):
        '''
        Returns the QTreeWidget which houses the currently selected image.
        '''

        if self.win.selection.selection_parameters['Type'] == 'Additive Images':

            tree = self.win.AddImageNameTree

        elif self.win.selection.selection_parameters['Type'] == 'Subtractive Images':

            tree = self.win.SubImageNameTree

        elif self.win.selection.selection_parameters['Type'] == 'Total Images':

            tree = self.win.TotalImageNameTree

        elif self.win.selection.selection_parameters['Type'] == 'Multiplicative Correction':

            tree = self.win.MulCorrNameTree

        else:

            tree = None

        return tree

    def remove_corr(self):
        '''
        Item/Image is removed to the multiplictive correction QTreeWidget
        disables the remove button until a item/image is added
        '''

        self.win.MulRemoveCorrButton.setChecked(True)
        
        if self.win.MulCorrNameTree.topLevelItemCount() != 0:

            self.win.MulCorrNameTree.clear()
            self.win.MulAddCorrButton.setChecked(False)

            self.multiplicative_parameters['Name'] = None

    def populate_tree(self, tree, fname, bounds):
        '''
        Loops through all cycles and images imported from the user
        and adds their labels to the appropriate QTreeWidget.
        '''

        tree.clear()
        for cycle in range(len(fname)):

            tree.addTopLevelItem(QTreeWidgetItem(['Cycle_' + str(cycle)], 0))
            tree.expandItem(tree.topLevelItem(cycle))

            for row in range(len(fname[cycle])):

                tree.topLevelItem(cycle).addChild(QTreeWidgetItem([os.path.basename(fname[cycle][row])], 0))

                if bounds[cycle][row] == False:

                    tree.topLevelItem(cycle).child(row).setForeground(0, QBrush(QColor('gold')))

                elif bounds[cycle][row] == True:

                    tree.topLevelItem(cycle).child(row).setForeground(0, QBrush(QColor(225, 225, 225, 255)))

    def change_cycles(self, image_parameters):
        '''
        Data is stored as list of arrays, where the number of lists 
        is equal to the number of desired cycles. When the number of desired 
        cycles is changed the list of arrays is flattened and then re-chunked
        into a list of arrays.
        '''

        image_parameters['Names'] = np.hstack(image_parameters['Names'])
        image_parameters['Normalization'] = np.hstack(image_parameters['Normalization'])
        image_parameters['Accepted'] = np.hstack(image_parameters['Accepted'])

        image_parameters['Accepted'] = np.array_split(np.array([True for _ in range(len(image_parameters['Names']))]), int(self.win.CyclesBox.text()), axis = 0)
        image_parameters['Names'] = np.array_split(image_parameters['Names'], int(self.win.CyclesBox.text()), axis = 0)
        image_parameters['Normalization'] = np.array_split(np.array(image_parameters['Normalization']), int(self.win.CyclesBox.text()), axis = 0)

    def update_cycles(self):
        '''
        When the number of desired cycles is changes this logic
        facilitates the updating of the trees, recalculation
        of the accepted images and repopulates the QTreeWidgets.
        '''

        if len(self.additive_parameters['Names']) != 0:

            self.change_cycles(self.additive_parameters)

        if len(self.subtractive_parameters['Names']) != 0:

            self.change_cycles(self.subtractive_parameters)

        self.update_trees()
        self.win.bounds.change_bounds()

    def update_trees(self):
        '''
        When there is a change to the images stored in the QTreeWidgets,
        this logic facilitates the updating of the trees, and re-plotting
        of the normalization data.
        '''

        if len(self.additive_parameters['Names']) != 0:

            self.populate_tree(self.win.AddImageNameTree, self.additive_parameters['Names'], self.additive_parameters['Accepted'])
            self.populate_tree(self.win.TotalImageNameTree, np.array_split(np.array(['Image_' + str(i) for i in range(len(np.hstack(self.additive_parameters['Names'])))]), int(self.win.CyclesBox.text())), self.additive_parameters['Accepted'])
            self.win.plot.update_plot(self.win.AddPlotView, self.additive_parameters['Normalization'], self.additive_parameters['Accepted'], self.win.addStdMinBox, self.win.addStdMaxBox)

        if len(self.subtractive_parameters['Names']) != 0:
            
            self.populate_tree(self.win.SubImageNameTree, self.subtractive_parameters['Names'], self.subtractive_parameters['Accepted'])
            self.populate_tree(self.win.TotalImageNameTree, np.array_split(np.array(['Image_' + str(i) for i in range(len(np.hstack(self.subtractive_parameters['Names'])))]), int(self.win.CyclesBox.text())), self.subtractive_parameters['Accepted'])
            self.win.plot.update_plot(self.win.SubPlotView, self.subtractive_parameters['Normalization'], self.subtractive_parameters['Accepted'], self.win.subStdMinBox, self.win.subStdMaxBox)

    def update_rotation(self, slider, rotation_label):
        '''
        Rotational value of the imges in the additive and subtractive
        QTreeWidget is changed update the plotted image.
        '''

        rotation_label.setText(str(slider.value() * 90) + '°')

        if self.win.selection.selection_parameters['Type'] == 'Additive Images':

            self.win.selection.selected_item()

        elif self.win.selection.selection_parameters['Type'] == 'Subtractive Images':

            self.win.selection.selected_item()

        elif self.win.selection.selection_parameters['Type'] == 'Total Images':

            self.win.selection.selected_item()

        elif self.win.selection.selection_parameters['Type'] == 'Multiplicative Correction':

            self.win.selection.selected_item()
        
        if self.win.linesegButton.isChecked() == True:
            
            self.win.linesegButton.setChecked(False)
            
            if self.win.pixmapTabs.count() > 1:
                
                self.win.traceplot.clear_trace()

    def normalization_factors(self, paths, index):
        '''
        From a collection of image paths, load a specific image from 
        the given "index", then calculate the sum of intensity for that
        image.
        '''

        img = self.win.files.load_image(paths[index])

        return (index, np.sum(img[int(np.shape(img)[0] * 0.01) : np.shape(img)[0] - int(np.shape(img)[0] * 0.01), \
                                  int(np.shape(img)[1] * 0.01) : np.shape(img)[1] - int(np.shape(img)[1] * 0.01)]))