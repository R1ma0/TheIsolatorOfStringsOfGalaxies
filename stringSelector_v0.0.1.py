# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from Widgets.skeletonizationWindow import Ui_SkeletonitationWindow
from Modules.ImageUtilities import IUtils
from Modules.ImageBinarizationMethods import ImageBinarization, binaryMethods
import imutils

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.move(5, 5)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.imageViewLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.imageViewLabel.setFont(font)
        self.imageViewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageViewLabel.setObjectName("imageViewLabel")
        self.gridLayout.addWidget(self.imageViewLabel, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_Image = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.actionOpen_Image.setShortcut("Ctrl+O")
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionSave_Image.setShortcut("Ctrl+S")
        self.actionSkeletonization = QtWidgets.QAction(MainWindow)
        self.actionSkeletonization.setObjectName("actionSkeletonization")
        self.actionResizeImage = QtWidgets.QAction(MainWindow)
        self.actionResizeImage.setObjectName("actionResizeImage")
        self.menuFile.addAction(self.actionOpen_Image)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuTools.addAction(self.actionSkeletonization)
        self.menuTools.addAction(self.actionResizeImage)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        # Triggers
        self.actionResizeImage.triggered.connect(self.resizeImage)
        self.actionOpen_Image.triggered.connect(self.loadImage)
        self.actionSave_Image.triggered.connect(self.saveImage)
        self.actionSkeletonization.triggered.connect(self.openSkeletonizationWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setupVariables()
        
    def setupVariables(self):
        self.filename = None # Stores the name of the uploaded file
        self.loadedImage = None # Stores the original uploaded image
        self.selectedBinarizationMethod = None
        self.selectedThresholdValue = None
        self.editableImage = None
        self.gaussianBlockSizeValue = None
        self.gaussianCValue = None

        self.binarizationMethodsList = [""] + binaryMethods
        self.binarizationMethods = ImageBinarization()
        self.imageUtils = IUtils()

    def openSkeletonizationWindow(self):
        self.baseSkeletonizationWindow = QtWidgets.QMainWindow()
        self.skeletonizationWindow = Ui_SkeletonitationWindow()
        self.skeletonizationWindow.setupUi(self.baseSkeletonizationWindow)
        self.skeletonizationWindow.binarizationMethodChangedSignal.connect(self.setBinarizationMethod)
        self.skeletonizationWindow.thresholdValueChangedSignal.connect(self.setThresholdValue)
        self.skeletonizationWindow.binaryThresholdValueSpinBoxSignal.connect(self.setThresholdValue)
        self.skeletonizationWindow.gaussianCSpinBoxSignal.connect(self.setGaussianCValue)
        self.skeletonizationWindow.gaussianCValueSliderSignal.connect(self.setGaussianCValue)
        self.skeletonizationWindow.gaussianBlockSizeSpinBoxSignal.connect(self.setGaussianBlockSizeValue)
        self.skeletonizationWindow.gaussianBlockSizeValueSliderSignal.connect(self.setGaussianBlockSizeValue)
        self.baseSkeletonizationWindow.show()

    def setGaussianCValue(self, value):
        self.gaussianCValue = value
        self.applyBinarizationMethodToImage()

    def setGaussianBlockSizeValue(self, value):
        if value % 2 == 1:
            self.gaussianBlockSizeValue = value
        self.applyBinarizationMethodToImage()

    def setThresholdValue(self, value):
        self.selectedThresholdValue = value
        self.applyBinarizationMethodToImage()

    def setBinarizationMethod(self, method):
        self.selectedBinarizationMethod = method

    def applyBinarizationMethodToImage(self):
        if self.loadedImage is None:
            return

        if self.selectedBinarizationMethod == 1:
            self.editableImage = self.binarizationMethods.convertUsingThresholdBinarization(
                self.loadedImage, self.selectedThresholdValue
            )
        elif self.selectedBinarizationMethod == 2:
            self.editableImage = self.binarizationMethods.convertUsingBrightnessBinarization(
                self.loadedImage
            )
        elif self.selectedBinarizationMethod == 3:
            self.editableImage = self.binarizationMethods.convertUsingAdaptiveGaussianBinarization(
                self.loadedImage, self.gaussianBlockSizeValue, self.gaussianCValue
            )
        else:
            pass

        if self.editableImage is not None:
            self.viewImage(self.editableImage)

    def resizeImage(self):
        if self.editableImage is None:
            return
        
        imageScalingVariant = [str(x) for x in range(5, 100, 5)]
        element, isSelected = QtWidgets.QInputDialog.getItem(
            MainWindow, "Resize", "Variants:", imageScalingVariant
        )

        if isSelected:
            self.editableImage = self.imageUtils.resizeImage(self.editableImage, int(element.replace('%', '')))
            self.viewImage(self.editableImage)

    def loadImage(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(filter="Image (*.png *.jpg)")[0]
        self.loadedImage = self.imageUtils.readImageFrom(self.filename)
        self.editableImage = None
        self.viewImage(self.loadedImage)

    def saveImage(self):
        options = QtWidgets.QFileDialog.Options()
        saveToFilename, check = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", "", "All Files (*)", options=options)
        if check:
            self.imageUtils.writeImageTo(saveToFilename, self.editableImage)

    def viewImage(self, image):
        image = imutils.resize(image, 800)
        image = self.imageUtils.BGR2RGB(image)
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0], QtGui.QImage.Format_RGB888)
        self.imageViewLabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "String Selector v0.1.3"))
        self.imageViewLabel.setText(_translate("MainWindow", "Image View Label"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionSkeletonization.setText(_translate("MainWindow", "Skeletonization"))
        self.actionResizeImage.setText(_translate("MainWindow", "Resize Image"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
