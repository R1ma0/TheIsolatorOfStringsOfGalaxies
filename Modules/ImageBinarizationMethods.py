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
    def __init__(self):
        self.imageUtils = IUtils()

    def convertUsingThresholdBinarization(self, image: cv2.Mat, thresholdValue: int) -> cv2.Mat:
        """
        Converts the source image to a binary using threshold binarization
        """
        return cv2.threshold(self.imageUtils.BGR2GRAY(image), thresholdValue, 255, cv2.THRESH_BINARY)[1]

    def convertUsingAdaptiveGaussianBinarization(self, image: cv2.Mat, blockSize: int, c: float) -> cv2.Mat:
        """
        Converts the source image to a binary using adaptive Gaussian binarization

        Parameters
        ----------
            image: cv2.Mat
                The source image to convert
            blockSize: int
                Pixel neighborhood size used to compute threshold value
            c: float
                This value simply lets us fine tune our threshold value
        """
        if blockSize == None: blockSize = 3
        if c == None: c = 0

        return cv2.adaptiveThreshold(
            self.imageUtils.BGR2GRAY(image), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c
        )

    def convertUsingOtsuThresholding(self, image: cv2.Mat):
        return cv2.threshold(self.imageUtils.BGR2GRAY(image), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
