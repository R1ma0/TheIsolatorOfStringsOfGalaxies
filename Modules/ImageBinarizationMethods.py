from Modules.ImageUtilities import IUtils
import cv2
import numpy

class ThresholdBinarization(object):
    """ The calss is used to perform threshold binarization

    Parameters
    ----------
    image : Mat
        The source image to convert
    thresholdValue : int
        The value of threshold binarizaton

    Methods
    -------
    convert() : 
        Converts the source image to binary
    """
    def __init__(self, image: cv2.Mat, thresholdValue: int):
        self.image = image
        self.thresholdValue = thresholdValue

    def convert(self):
        """ Convert to binary image """
        image = self.image
        dst, threshold = cv2.threshold(IUtils.BGR2GRAY(image), self.thresholdValue, 255, cv2.THRESH_BINARY)
        return dst, threshold

class BrightnessBinarization(object):
    """ Binarization based on the average brightness of the image 
    
    Parameters
    ----------
    sourceImage : Mat
        The source image to convert (a set of image pixels)

    Methods
    -------
    convert() : cv2.Mat
        Converts the source image to binary
    """
    def __init__(self, sourceImage: cv2.Mat):
        self.image = sourceImage
        self.width = sourceImage.shape[1]
        self.height = sourceImage.shape[0]
        self.pixelsBrightness = numpy.zeros([self.height, self.width], dtype=numpy.ubyte)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.averageImageBrightness = None

    def convert(self) -> cv2.Mat:
        """ Convert to binary image """
        self.averageImageBrightness = self.__calculateAverageBrightness()
        return self.__binarizeImage(self.image)

    def __calculateAverageBrightness(self) -> float:
        """ The method calculates the average brightnesss of the image """
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.pixelsBrightness[i, j] = self.__getPixelBrightness(self.image[i, j])

        return self.pixelsBrightness.sum() / (self.width * self.height)
    
    def __binarizeImage(self, image: cv2.Mat) -> cv2.Mat:
        """ The method for each pixel compares its average brightness
        with the average brightness of the image

        Parameters
        ----------
        image : Mat
            Local copy of the source image
        
        Returns
        -------
        image : Mat
            Binarized image
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                pxBrightGreaterAvg = self.pixelsBrightness[i, j] > self.averageImageBrightness
                image[i, j] = self.white if pxBrightGreaterAvg else self.black

        return image

    def __getPixelBrightness(self, pixel: list) -> float:
        """ The method calculates the brightness of the pixel
        
        Parameters
        ----------
        pixel : int 
            An pixel of image in BGR format
        """
        return 0.299 * pixel[2] + 0.587 * pixel[1] + 0.114 * pixel[0]