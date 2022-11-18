# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from Widgets.binarizationWindow import Ui_SkeletonitationWindow
from Modules.ImageUtilities import IUtils
from Modules.ImageBinarizationMethods import ImageBinarization, binaryMethods
from Modules.ImageSkeletonizationMethods import OPCASkeletonization, ZSSkeletonization
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
        self.menuSkeletonization = QtWidgets.QMenu(self.menuTools)
        self.menuSkeletonization.setObjectName("menuSkeletonization")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_Image = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image.setObjectName("actionOpen_Image")
        self.actionOpen_Image.setShortcut("Ctrl+O")
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionSave_Image.setShortcut("Ctrl+S")
        self.actionBinarization = QtWidgets.QAction(MainWindow)
        self.actionBinarization.setObjectName("actionBinarization")
        self.actionBinarization.setEnabled(False)
        self.actionResizeImage = QtWidgets.QAction(MainWindow)
        self.actionResizeImage.setObjectName("actionResizeImage")
        self.actionOPCAMethod = QtWidgets.QAction(MainWindow)
        self.actionOPCAMethod.setObjectName("actionOPCAMethod")
        self.actionZSMethod = QtWidgets.QAction(MainWindow)
        self.actionZSMethod.setObjectName("actionZSMethod")
        self.menuFile.addAction(self.actionOpen_Image)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuTools.addAction(self.actionBinarization)
        self.menuTools.addAction(self.actionResizeImage)
        self.menuTools.addAction(self.menuSkeletonization.menuAction())
        self.menuSkeletonization.addAction(self.actionOPCAMethod)
        self.menuSkeletonization.addAction(self.actionZSMethod)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        # Triggers
        self.actionResizeImage.triggered.connect(self.resizeImage)
        self.actionOpen_Image.triggered.connect(self.loadImage)
        self.actionSave_Image.triggered.connect(self.saveImage)
        self.actionBinarization.triggered.connect(self.openBinarizationWindow)
        self.actionOPCAMethod.triggered.connect(self.performOPCASkeletonization)
        self.actionZSMethod.triggered.connect(self.performZSSkeletonization)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setupVariables()
        
    def setupVariables(self):
        self.filename = None # Stores the name of the uploaded file
        self.imageToChange = None
        self.loadedImage = None
        self.selectedBinarizationMethod = None
        self.selectedThresholdValue = None
        self.gaussianBlockSizeValue = None
        self.gaussianCValue = None

        self.binarizationMethodsList = [""] + binaryMethods
        self.binarizationMethods = ImageBinarization()
        self.opcaSkeletonization = OPCASkeletonization()
        self.zsSkeletonization = ZSSkeletonization()
        self.imageUtils = IUtils()

    def openBinarizationWindow(self):
        self.baseBinarizationWindow = QtWidgets.QMainWindow()
        self.binarizationWindow = Ui_SkeletonitationWindow()
        self.binarizationWindow.setupUi(self.baseBinarizationWindow)
        self.binarizationWindow.binarizationMethodChangedSignal.connect(self.setBinarizationMethod)
        self.binarizationWindow.thresholdValueChangedSignal.connect(self.setThresholdValue)
        self.binarizationWindow.binaryThresholdValueSpinBoxSignal.connect(self.setThresholdValue)
        self.binarizationWindow.gaussianCSpinBoxSignal.connect(self.setGaussianCValue)
        self.binarizationWindow.gaussianCValueSliderSignal.connect(self.setGaussianCValue)
        self.binarizationWindow.gaussianBlockSizeSpinBoxSignal.connect(self.setGaussianBlockSizeValue)
        self.binarizationWindow.gaussianBlockSizeValueSliderSignal.connect(self.setGaussianBlockSizeValue)
        self.baseBinarizationWindow.show()

    def setGaussianCValue(self, value):
        self.gaussianCValue = value
        self.applyBinarizationMethodToImage()

    def setGaussianBlockSizeValue(self, value):
        if value % 2 == 1:
            self.gaussianBlockSizeValue = value
        try:
            self.applyBinarizationMethodToImage()
        except ValueError as e:
            print("The value of the block size must be equal 'value % 2 == 1'. \n {}".format(e))

    def setThresholdValue(self, value):
        self.selectedThresholdValue = value
        self.applyBinarizationMethodToImage()

    def setBinarizationMethod(self, method):
        self.selectedBinarizationMethod = method
        self.applyBinarizationMethodToImage()

    def applyBinarizationMethodToImage(self):
        if self.selectedBinarizationMethod == 1:
            self.imageToChange = self.binarizationMethods.convertUsingThresholdBinarization(
                self.loadedImage, self.selectedThresholdValue
            )
        elif self.selectedBinarizationMethod == 2:
            self.imageToChange = self.binarizationMethods.convertUsingAdaptiveGaussianBinarization(
                self.loadedImage, self.gaussianBlockSizeValue, self.gaussianCValue
            )
        elif self.selectedBinarizationMethod == 3:
            self.imageToChange = self.binarizationMethods.convertUsingOtsuThresholding(self.loadedImage)
        else:
            pass

        self.viewImage(self.imageToChange)

    def performOPCASkeletonization(self):
        self.imageToChange = self.opcaSkeletonization.execute(self.imageToChange)
        self.viewImage(self.imageToChange)

    def performZSSkeletonization(self):
        self.imageToChange = self.zsSkeletonization.execute(self.imageToChange)
        self.viewImage(self.imageToChange)

    def resizeImage(self): 
        imageScalingVariant = [str(x) for x in range(1, 100, 1)]
        element, isSelected = QtWidgets.QInputDialog.getItem(
            MainWindow, "Resize", "%:", imageScalingVariant
        )

        if isSelected:
            try:
                self.imageToChange = self.imageUtils.resizeImage(self.imageToChange, int(element))
                self.viewImage(self.imageToChange)
            except Exception as e:
                print(e)

    def loadImage(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(filter="Image (*.png *.jpg)")[0]
        if not self.filename:
            return
        self.loadedImage = self.imageUtils.readImageFrom(self.filename)
        self.actionBinarization.setEnabled(True)
        self.viewImage(self.loadedImage)

    def saveImage(self):
        options = QtWidgets.QFileDialog.Options()
        saveToFilename, check = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", "", "All Files (*)", options=options)
        if check:
            self.imageUtils.writeImageTo(saveToFilename, self.imageToChange)

    def viewImage(self, image):
        image = imutils.resize(image, 800)
        image = self.imageUtils.BGR2RGB(image)
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0], QtGui.QImage.Format_RGB888)
        self.imageViewLabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "String Selector v0.2.1"))
        self.imageViewLabel.setText(_translate("MainWindow", "Image View"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuSkeletonization.setTitle(_translate("MainWindow", "Skeletonization"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionBinarization.setText(_translate("MainWindow", "Binarization"))
        self.actionResizeImage.setText(_translate("MainWindow", "Resize Image"))
        self.actionOPCAMethod.setText(_translate("MainWindow", "OPCA (One-Pass Combination Algorithm)"))
        self.actionZSMethod.setText(_translate("MainWindow", "ZS (Zhang-Suen Algorithm)"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
