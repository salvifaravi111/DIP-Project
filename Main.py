import sys
import os
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLabel
from PyQt5.uic import loadUi
import cv2
from ImagePreprocess import Image_Preprocess
import matplotlib.pyplot as plt


from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class ImageShow(QDialog):

    def __init__(self, path):
        super(ImageShow, self).__init__()
        loadUi('ImageShow.ui', self)
        self.init_canvas()

        ## Class Button Properties
        self.OriginalBtn.clicked.connect(self.on_originalbtn_clicked)
        self.GlobalTBtn.clicked.connect(self.on_globaltbtn_clicked)
        self.AdaptiveMBtn.clicked.connect(self.on_adaptivembtn_clicked)
        self.AdaptiveGBtn.clicked.connect(self.on_adaptivegbtn_clicked)
        self.GaussianBtn.clicked.connect(self.on_gaussianbtn_clicked)
        self.MedianBtn.clicked.connect(self.on_medianbtn_clicked)
        self.browseBtn.clicked.connect(self.on_browsebtn_clicked)
        self.modelOneBtn.clicked.connect(self.on_modelonebtn_clicked)
        self.modelTwoBtn.clicked.connect(self.on_modeltwobtn_clicked)


        ###############################################
        ##OPENING IMAGE LOCATIONS
        ###############################################
        self.path = path

        self.image_file = list()
        for file_name in os.listdir(self.path):
            self.image_file.append(self.path +'/'+ file_name)
        ###############################################

        self.ImgProp = Image_Preprocess()
        image_pixel = self.ImgProp.read_image(self.image_file)

        self.show_image(image_pixel)


    @pyqtSlot()
    def on_originalbtn_clicked(self):
        pixels = self.ImgProp.get_original_image()
        self.show_image(pixels)


    @pyqtSlot()
    def on_globaltbtn_clicked(self):
        pixels = self.ImgProp.global_threshold()
        self.show_image(pixels)


    @pyqtSlot()
    def on_adaptivembtn_clicked(self):
        pixels = self.ImgProp.adaptive_mean()
        self.show_image(pixels)

    @pyqtSlot()
    def on_adaptivegbtn_clicked(self):
        pixels = self.ImgProp.adaptive_gaussian()
        self.show_image(pixels)

    @pyqtSlot()
    def on_gaussianbtn_clicked(self):
        pixels = self.ImgProp.gaussian_blur()
        self.show_image(pixels)

    @pyqtSlot()
    def on_medianbtn_clicked(self):
        pixels = self.ImgProp.median_blur()
        self.show_image(pixels)

    @pyqtSlot()
    def on_browsebtn_clicked(self):
        self.file = QFileDialog.getOpenFileName()[0]
        self.InputPath.setText(self.file)

    @pyqtSlot()
    def on_modelonebtn_clicked(self):
        pixels, index = self.ImgProp.model_one(self.file)
        self.show_image2(pixels, index)
        ## Show result

    @pyqtSlot()
    def on_modeltwobtn_clicked(self):
        pixels, index = self.ImgProp.model_two(self.file)
        self.show_image2(pixels, index)
        ## Show result



    def init_canvas(self):
        self.static_canvas = FigureCanvas(Figure(figsize=(12, 8)))
        self.ImageLayout.addWidget(self.static_canvas)

        self._static_ax = [self.static_canvas.figure.add_subplot(221),
                           self.static_canvas.figure.add_subplot(222),
                           self.static_canvas.figure.add_subplot(223),
                           self.static_canvas.figure.add_subplot(224)]

    def show_image(self, image_pixel):

        try:
            self.static_canvas.draw()

            image_file = np.array(image_pixel[0:16])

            plt.imshow(image_file[0])
            for i in range(4):
                self._static_ax[i].cla()
                self._static_ax[i].imshow(image_file[i],'gray')
        except Exception as e:
            print(e)


    def show_image2(self, image_pixel, index):

        try:
            self.static_canvas.draw()

            for i in range(4):
                self._static_ax[i].cla()
                self._static_ax[i].imshow(image_pixel[i],'gray')

            self.resultLbl.setText('Matched with: '+ str(self.image_file[index]))
        except Exception as e:
            print(e)






class ImagePathPicker(QDialog):
    def __init__(self):
        super(ImagePathPicker, self).__init__()
        loadUi('ImagePath.ui', self)
        self.setWindowTitle('Image Folder Picker')

        self.BrowseButton.clicked.connect(self.on_browse_button_clicked)
        self.NextButton.clicked.connect(self.on_next_button_clicked)
        self.BackButton.clicked.connect(self.on_back_button_clicked)



    @pyqtSlot()
    def on_browse_button_clicked(self):
        self.file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.FilePicker.setText(self.file)

    @pyqtSlot()
    def on_next_button_clicked(self):
        if(os.path.isdir(self.file)):
            self.imageShow = ImageShow(path = self.file)
            #self.imageShow.setGeometry(200,200,800,400)
            self.imageShow.setWindowTitle('Fingerprint Checker')
            self.imageShow.show()
            self.hide()


    @pyqtSlot()
    def on_back_button_clicked(self):
        pass




app = QApplication(sys.argv)
widget = ImagePathPicker()
widget.show()
sys.exit(app.exec_())
