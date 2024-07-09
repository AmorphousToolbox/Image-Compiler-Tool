#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
===================================================================
Amorphous Toolbox - Image Compiler Tool - Selection




Author: Nick Burns, January, 20th, 2024
===================================================================
'''

import numpy as np

from PySide6.QtCore import Qt

class Selection:
    '''
    This class deals with the selection of images within the
    additive, subtractive and multiplicative QTreeWidgets by
    the user.
    '''

    def __init__(self, win):
        '''
        Creates storage for a selected item and its indicies. 
        Sets the event handlers for items selected in the QTreeWidgets.
        '''
        
        self.win = win

        #=========================================
        #                  Data
        #=========================================
        
        self.selection_parameters = {'Image': None,
                                     'Cycle_Index': None,
                                     'Item_Index': None,
                                     'Total_Index': None,
                                     'Type': None}
        
        #=========================================
        #             Event Handeling
        #=========================================

        #<<<<<<<<<<<<<<Trees<<<<<<<<<<<<<<< 
        self.win.AddImageNameTree.clicked.connect(lambda: self.selected_item_logic(self.win.AddImageNameTree))
        self.win.SubImageNameTree.clicked.connect(lambda: self.selected_item_logic(self.win.SubImageNameTree))
        self.win.TotalImageNameTree.clicked.connect(lambda: self.selected_item_logic(self.win.TotalImageNameTree))
        self.win.MulCorrNameTree.clicked.connect(lambda: self.selected_item_logic(self.win.MulCorrNameTree))
        
    #Determines the hierarchy of the selected index (Parent or Child?)
    #based on selection clears PixMap and reset selected buttons,
    #if proper index is selected begins plotting item/image to
    #PixMap and updating PixPlots.
    #=============================================================
    def selected_item_logic(self, tree):

        if tree.currentIndex().parent().row() == -1:

            self.selection_parameters['Cycle_Index'] = tree.currentIndex().row()
            self.selection_parameters['Item_Index'] = None
            self.selection_parameters['Total_Index'] = None

        else:
        
            self.selection_parameters['Cycle_Index'] = tree.currentIndex().parent().row()
            self.selection_parameters['Item_Index'] = tree.currentIndex().row()
            self.selection_parameters['Total_Index'] = tree.topLevelItem(0).childCount() * tree.currentIndex().parent().row() + tree.currentIndex().row()

        self.selection_parameters['Type'] = tree.currentIndex().model().headerData(0, Qt.Horizontal, 0)

        self.win.edgeButton.setChecked(False)
        
        if self.win.linesegButton.isChecked() == True:
            
            self.win.linesegButton.setChecked(False)

        if tree.currentIndex().parent().row() == -1:

            if self.selection_parameters['Type'] != 'Multiplicative Correction':
            
                self.selected_cycle()

            else:

                self.selected_item()

        else:

            self.selected_item()
            
        self.clear_selection(tree)
        
    #Selected item index is updated, plotting selected item/image
    #to the PixPlot, index is plotted on PixPlots, if total image
    #QTreeWidget index is selected the total image is calculated
    #and plotted in the Pixmap. Other trees selection is cleared
    #=============================================================
    def selected_item(self):
        
        if self.selection_parameters['Type'] == 'Additive Images':

            self.selection_parameters['Image'] = np.rot90(self.win.files.load_image(\
                                                          self.win.trees.additive_parameters['Names'][self.selection_parameters['Cycle_Index']][self.selection_parameters['Item_Index']]), \
                                                         -self.win.AddRotationalSlider.value())
            
        elif self.selection_parameters['Type'] == 'Subtractive Images':
            
            self.selection_parameters['Image'] = np.rot90(self.win.files.load_image(\
                                                          self.win.trees.subtractive_parameters['Names'][self.selection_parameters['Cycle_Index']][self.selection_parameters['Item_Index']]), \
                                                         -self.win.SubRotationalSlider.value())
        
        elif self.selection_parameters['Type'] == 'Total Images':

            additive_image, subtractive_image = np.array([[0]]), np.array([[0]])

            if self.win.AddImageNameTree.topLevelItemCount() != 0:
                
                additive_image = np.rot90(self.win.files.load_image(\
                                          self.win.trees.additive_parameters['Names'][self.selection_parameters['Cycle_Index']][self.selection_parameters['Item_Index']]), \
                                         -self.win.AddRotationalSlider.value())
                
            if self.win.SubImageNameTree.topLevelItemCount() != 0:
            
                subtractive_image = np.rot90(self.win.files.load_image(\
                                             self.win.trees.subtractive_parameters['Names'][self.selection_parameters['Cycle_Index']][self.selection_parameters['Item_Index']]), \
                                            -self.win.SubRotationalSlider.value())
                
            self.selection_parameters['Image'] = additive_image - subtractive_image

            if self.win.MulCorrNameTree.topLevelItemCount() != 0:
                
                self.selection_parameters['Image'] /= np.rot90(self.win.files.load_image(self.win.trees.multiplicative_parameters['Name']), -self.win.MulCorrRotationalSlider.value())

        elif self.selection_parameters['Type'] == 'Multiplicative Correction':

            self.selection_parameters['Image'] = np.rot90(self.win.files.load_image(\
                                                          self.win.trees.multiplicative_parameters['Name']), \
                                                         -self.win.MulCorrRotationalSlider.value())

        self.win.image.clear_image()
        self.win.image.update_image(self.selection_parameters['Image'])

        if self.win.AddImageNameTree.topLevelItemCount() != 0:

            self.win.plot.clear_plot(self.win.AddPlotView)
            self.win.plot.update_plot(self.win.AddPlotView, self.win.trees.additive_parameters['Normalization'], self.win.trees.additive_parameters['Accepted'], self.win.addStdMinBox, self.win.addStdMaxBox)

        if self.win.SubImageNameTree.topLevelItemCount() != 0:

            self.win.plot.clear_plot(self.win.SubPlotView)
            self.win.plot.update_plot(self.win.SubPlotView, self.win.trees.subtractive_parameters['Normalization'], self.win.trees.subtractive_parameters['Accepted'], self.win.subStdMinBox, self.win.subStdMaxBox)

    def selected_cycle(self):

        self.win.image.clear_image()

        if self.win.AddImageNameTree.topLevelItemCount() != 0:

            self.win.plot.clear_plot(self.win.AddPlotView)
            self.win.plot.update_plot(self.win.AddPlotView, self.win.trees.additive_parameters['Normalization'], self.win.trees.additive_parameters['Accepted'], self.win.addStdMinBox, self.win.addStdMaxBox)

        if self.win.SubImageNameTree.topLevelItemCount() != 0:

            self.win.plot.clear_plot(self.win.SubPlotView)
            self.win.plot.update_plot(self.win.SubPlotView, self.win.trees.subtractive_parameters['Normalization'], self.win.trees.subtractive_parameters['Accepted'], self.win.subStdMinBox, self.win.subStdMaxBox)

    def swap_selected(self):
        
        if self.selection_parameters['Type'] == 'Additive Images':
            
            self.selection_parameters['Type'] = 'Subtractive Images'

            if self.selection_parameters['Item_Index'] != None:
                
                self.win.SubImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)

        elif self.selection_parameters['Type'] == 'Subtractive Images':

            self.selection_parameters['Type'] = 'Additive Images'

            if self.selection_parameters['Item_Index'] != None:
                
                self.win.AddImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)

        elif self.selection_parameters['Type'] == 'Total Images':

            if self.selection_parameters['Item_Index'] != None:

                self.win.TotalImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)

    def reselect_selected(self):

        if self.selection_parameters['Type'] == 'Additive Images':

            if self.selection_parameters['Item_Index'] != None:
                
                self.win.AddImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)

        elif self.selection_parameters['Type'] == 'Subtractive Images':

            if self.selection_parameters['Item_Index'] != None:
                
                self.win.SubImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)

        elif self.selection_parameters['Type'] == 'Total Images':

            if self.selection_parameters['Item_Index'] != None:

                self.win.TotalImageNameTree.topLevelItem(self.selection_parameters['Cycle_Index']).child(self.selection_parameters['Item_Index']).setSelected(True)


    #Clears selection in all QTreeWidgets except for selected 
    #QTreeWidget.
    #=============================================================
    def clear_selection(self, tree):

        if tree.currentIndex().model().headerData(0, Qt.Horizontal, 0) == 'Additive Images':

            self.win.SubImageNameTree.selectionModel().clear()
            self.win.TotalImageNameTree.selectionModel().clear()
            self.win.MulCorrNameTree.selectionModel().clear()

            self.selection_parameters['Type'] = 'Additive Images'

        elif tree.currentIndex().model().headerData(0, Qt.Horizontal, 0) == 'Subtractive Images':

            self.win.AddImageNameTree.selectionModel().clear()
            self.win.TotalImageNameTree.selectionModel().clear()
            self.win.MulCorrNameTree.selectionModel().clear()

            self.selection_parameters['Type'] = 'Subtractive Images'

        elif tree.currentIndex().model().headerData(0, Qt.Horizontal, 0) == 'Total Images':

            self.win.AddImageNameTree.selectionModel().clear()
            self.win.SubImageNameTree.selectionModel().clear()
            self.win.MulCorrNameTree.selectionModel().clear()

            self.selection_parameters['Type'] = 'Total Images'
            
        elif tree.currentIndex().model().headerData(0, Qt.Horizontal, 0) == 'Multiplicative Correction':
            
            self.win.AddImageNameTree.selectionModel().clear()
            self.win.SubImageNameTree.selectionModel().clear()
            self.win.TotalImageNameTree.selectionModel().clear()

            self.selection_parameters['Type'] = 'Multiplicative Correction'           