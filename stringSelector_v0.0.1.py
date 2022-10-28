# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from Widgets.skeletonizationWindow import Ui_SkeletonitationWindow
from Modules.ImageUtilities import IUtils
from Modules.ImageBinarizationMethods import ThresholdBinarization, BrightnessBinarization
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
        self.actionOpen_Image.triggered.connect(self.loadImage)
        self.actionSave_Image = QtWidgets.QAction(MainWindow)
        self.actionSave_Image.setObjectName("actionSave_Image")
        self.actionSave_Image.setShortcut("Ctrl+S")
        self.actionSave_Image.triggered.connect(self.saveImage)
        self.actionSkeletonization = QtWidgets.QAction(MainWindow)
        self.actionSkeletonization.setObjectName("actionSkeletonization")
        self.actionSkeletonization.triggered.connect(self.openSkeletonizationWindow)
        self.menuFile.addAction(self.actionOpen_Image)
        self.menuFile.addAction(self.actionSave_Image)
        self.menuTools.addAction(self.actionSkeletonization)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.filename = None # Stores the name of the uploaded file
        self.loadedImage = None # Stores the original uploaded image
        self.selectedBinarizationMethod = None

    def openSkeletonizationWindow(self):
        self.baseSkeletonizationWindow = QtWidgets.QMainWindow()
        self.skeletonizationWindow = Ui_SkeletonitationWindow()
        self.skeletonizationWindow.setupUi(self.baseSkeletonizationWindow)
        self.skeletonizationWindow.binarizationMethodChangedSignal.connect(self.setBinarizationMethod)
        self.skeletonizationWindow.thresholdValueChangedSignal.connect(self.setThresholdValue)
        self.baseSkeletonizationWindow.show()

    def setThresholdValue(self, value):
        self.applyBinarizationMethodToImage(self.selectedBinarizationMethod, value=value)

    def setBinarizationMethod(self, method):
        self.applyBinarizationMethodToImage(method)

    def applyBinarizationMethodToImage(self, method, value=125):
        self.selectedBinarizationMethod = method
        thresholdImage = None

        if self.loadedImage is None:
            return

        if method == 1:
            thresholdMethod = ThresholdBinarization(self.loadedImage, value)
            _, thresholdImage = thresholdMethod.convert()
        elif method == 2:
            thresholdMethod = BrightnessBinarization(self.loadedImage)
            thresholdImage = thresholdMethod.convert()
        else:
            pass

        if thresholdImage is not None:
            self.viewImage(thresholdImage)

    def loadImage(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(filter="Image (*.png *.jpg)")[0]
        self.loadedImage = IUtils.readImageFrom(self.filename)
        self.viewImage(self.loadedImage)

    def saveImage(self):
        options = QtWidgets.QFileDialog.Options()
        saveToFilename, check = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", "", "All Files (*)", options=options)
        if check:
            IUtils.writeImageTo(saveToFilename, self.changedImage)

    def viewImage(self, image):
        image = imutils.resize(image, 800)
        image = IUtils.BGR2RGB(image)
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.strides[0], QtGui.QImage.Format_RGB888)
        self.imageViewLabel.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "String Selector v0.0.1"))
        self.imageViewLabel.setText(_translate("MainWindow", "Image View Label"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionOpen_Image.setText(_translate("MainWindow", "Open Image"))
        self.actionSave_Image.setText(_translate("MainWindow", "Save Image"))
        self.actionSkeletonization.setText(_translate("MainWindow", "Skeletonization"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
