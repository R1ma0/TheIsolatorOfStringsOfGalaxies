from Modules.ImageUtilities import IUtils
import cv2

class ThresholdBinarization(object):
    def __init__(self, image, thresholdValue):
        self.image = image
        self.thresholdValue = thresholdValue

    def convert(self):
        image = self.image
        dst, threshold = cv2.threshold(
            IUtils.BGR2GRAY(image),
            self.thresholdValue,
            255,
            cv2.THRESH_BINARY
        )
        return dst, threshold