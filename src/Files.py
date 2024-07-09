#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################
#                          Files
#
#This script manages the loading and remova of all items/images 
#into the QTreeWidgets. The selection of the items/images indexs
#in the QTreeWidgets is managed. Additionally the saving of the
#filtered and corrected final image output is managed.

#Author: Nick Burns, January, 20th, 2024
##############################################################

import os
import ctypes
import numpy as np
from skimage import io
from functools import partial

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt

from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import cpu_count 

class Files:

    def __init__(self, win):
        
        self.win = win

        #=========================================
        #             Event Handeling
        #=========================================
        
        #<<<<<<<<<<<<<<Buttons<<<<<<<<<<<<<<< 
        self.win.LoadFolderButton.clicked.connect(self.load_output_directory)
        self.win.SaveTotalButton.clicked.connect(lambda: self.save_total(False))
        self.win.SaveCyclesButton.clicked.connect(self.save_cycles)
        self.win.SaveSinglesButton.clicked.connect(lambda: self.save_total(True))

        #<<<<<<<<<<<<<<Actionss<<<<<<<<<<<<<<<
        self.win.actionTotalImage.triggered.connect(lambda: self.save_total(False))
        self.win.actionCycleImages.triggered.connect(self.save_cycles)
        self.win.actionSingleImages.triggered.connect(lambda: self.save_total(True))
        
        
    #Browse file directory for multiple items/images to populate
    #additive and subtractive image QTreeWidgets.
    #=============================================================
    def browse_files(self):
        
        fileBrowse = QFileDialog()
        #fileBrowse.setViewMode(0)
        fileBrowse.setViewMode(QFileDialog.Detail)
        
        #return io.ImageCollection(fileBrowse.getOpenFileNames(self.win, 'Load Images', '', "Images (*.tif *.tiff)")[0])
        return np.array(fileBrowse.getOpenFileNames(self.win, 'Load Images', '', "Images (*.tif *.tiff)")[0])
    
    #Browse file directory for an item/image to populate multiplicative 
    #and additive correction QTreeWidgets.
    #=============================================================
    def browse_file(self):
        
        fileBrowse = QFileDialog()
        #fileBrowse.setViewMode(0)
        fileBrowse.setViewMode(QFileDialog.Detail)
        
        #return io.ImageCollection(fileBrowse.getOpenFileName(self.win, 'Load Correction', '', "Correction Image (*.tif *.tiff)")[0])
        return fileBrowse.getOpenFileName(self.win, 'Load Correction', '', "Correction Image (*.tif *.tiff)")[0]
        
    #Browse directory for output folder for saved items/images
    #=============================================================
    def browse_directory(self):
        
        fileBrowse = QFileDialog()
        #fileBrowse.setViewMode(0)
        fileBrowse.setViewMode(QFileDialog.Detail)
        
        return fileBrowse.getExistingDirectory(self.win, 'Load Output Directory', '')
    
    #Loads a .tiff image into a numpy array
    #=============================================================
    def load_image(self, name):

        return io.imread(name, None).astype(float)
    
    #Outputs selected output directory into QLineEdit
    #=============================================================
    def load_output_directory(self):
        
        self.win.FolderBox.setText(self.browse_directory())
        
    #Saves a numpy array as a .tiff image
    #=============================================================
    def save_image(self, path, image):
        
        io.imsave(path, image.astype('float32'))

    def load_correction(self):

        if self.win.MulCorrNameTree.topLevelItemCount() != 0:

            mul_img = np.rot90(self.load_image(self.win.trees.multiplicative_parameters['Name']), -self.win.MulCorrRotationalSlider.value())

        else:

            mul_img = 1.0

        return mul_img
    
    def compile_image(self, add_names, sub_names, compile_norms, avg_compile_norm, index):

        compile_img = np.zeros((1, 1))

        if self.win.AddImageNameTree.topLevelItemCount() != 0:
            
            add_img = np.rot90(self.load_image(add_names[index]), -self.win.AddRotationalSlider.value())

            compile_img = add_img + compile_img

        if self.win.SubImageNameTree.topLevelItemCount() != 0:
            
            sub_img = np.rot90(self.load_image(sub_names[index]), -self.win.SubRotationalSlider.value())

            compile_img = -sub_img + compile_img

        return index, compile_img / compile_norms[index] * avg_compile_norm

    def save_total(self, single_check = False):

        if self.win.AddImageNameTree.topLevelItemCount() != 0 or self.win.SubImageNameTree.topLevelItemCount() != 0:

            mul_img = self.load_correction()

            compile_norms = np.ones((1))

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
            for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, add_names, sub_names, compile_norms, avg_compile_norm), range(len(in_indicies[0])))):

                if count == 0:

                    total_img = results[1]

                else:

                    total_img += results[1]
                
                self.win.FileProgressBar.setValue(count + 1)

                if single_check == True:
                    
                    self.save_image(self.win.FolderBox.text() + '/' + self.win.NameBox.text() + '_Item_' + str(results[0]) + '.tiff', results[1] / mul_img)

            pool.close()
            pool.join()

            self.win.FileProgressBar.setValue(0)

            if single_check == False:
                
                self.save_image(self.win.FolderBox.text() + '/' + self.win.NameBox.text() + '.tiff', total_img / mul_img)

    def save_cycles(self):

        if self.win.AddImageNameTree.topLevelItemCount() != 0 or self.win.SubImageNameTree.topLevelItemCount() != 0:

            mul_img = self.load_correction()

            #==================================================================
            compile_norms = np.ones((self.win.CyclesBox.value(), 1))

            if self.win.AddImageNameTree.topLevelItemCount() != 0:

                in_indicies = [np.where(self.win.trees.additive_parameters['Accepted'][i] == True) for i in range(self.win.CyclesBox.value())]

                add_norms = [self.win.trees.additive_parameters['Normalization'][i][in_indicies[i]] for i in range(self.win.CyclesBox.value())]
                add_names = [self.win.trees.additive_parameters['Names'][i][in_indicies[i]] for i in range(self.win.CyclesBox.value())]

                compile_norms = [add_norms[i] + compile_norms[i] for i in range(self.win.CyclesBox.value())]

                avg_compile_norm = [np.average(compile_norms[i]) for i in range(self.win.CyclesBox.value())]

            if self.win.SubImageNameTree.topLevelItemCount() != 0:

                in_indicies = [np.where(self.win.trees.subtractive_parameters['Accepted'][i] == True) for i in range(self.win.CyclesBox.value())]

                sub_norms = [self.win.trees.subtractive_parameters['Normalization'][i][in_indicies[i]] for i in range(self.win.CyclesBox.value())]
                sub_names = [self.win.trees.subtractive_parameters['Names'][i][in_indicies[i]] for i in range(self.win.CyclesBox.value())]

                compile_norms = [sub_norms[i] + compile_norms[i] for i in range(self.win.CyclesBox.value())]

                avg_compile_norm = [np.average(compile_norms[i]) for i in range(self.win.CyclesBox.value())]

            #==================================================================

            self.win.FileProgressBar.setValue(0)
            self.win.FileProgressBar.setMaximum(len(np.hstack(compile_norms)))

            total_count = 0
            for cycle in range(self.win.CyclesBox.value()):

                pool = Pool(cpu_count())
                for count, results in enumerate(pool.imap_unordered(partial(self.compile_image, add_names[cycle], sub_names[cycle], compile_norms[cycle], avg_compile_norm[cycle]), range(len(in_indicies[cycle][0])))):

                    if count == 0:

                        total_img = results

                    else:

                        total_img += results
                    
                    del results

                    total_count += 1

                    self.win.FileProgressBar.setValue(total_count + 1)

                pool.close()
                pool.join()

                self.save_image(self.win.FolderBox.text() + '/' + self.win.NameBox.text() + '_Cycle_' + str(cycle) + '.tiff', total_img / mul_img)

            self.win.FileProgressBar.setValue(0)