from Modules.ImageUtilities import IUtils
import cv2
import numpy

binaryMethods = [
    "Threshold Binary",
    "Adaprive Gaussian",
    "Otsu`s Threshold"
]

class ImageBinarization(object):
    """ 
    The class implements image binarization methods
    """
    def convertUsingThresholdBinarization(self, image: cv2.Mat, thresholdValue: int) -> cv2.Mat:
        """
        Converts the source image to a binary using threshold binarization
        """
        return cv2.threshold(IUtils.BGR2GRAY(image), thresholdValue, 255, cv2.THRESH_BINARY)[1]

    def convertUsingAdaptiveGaussianBinarization(self, image: cv2.Mat, blockSize: int, c: float, maxThreshold: int) -> cv2.Mat:
        """
        Converts the source image to a binary using adaptive Gaussian binarization
        """
        blockSize = 3 if blockSize == None else blockSize
        c = 0 if c == None else c
        maxThreshold = 255 if maxThreshold == None else maxThreshold

        return cv2.adaptiveThreshold(
            IUtils.BGR2GRAY(image), maxThreshold, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c
        )

    def convertUsingOtsuThresholding(self, image: cv2.Mat):
        return cv2.threshold(IUtils.BGR2GRAY(image), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
