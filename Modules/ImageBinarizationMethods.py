from Modules.ImageUtilities import IUtils
import cv2
import numpy

binaryMethods = [
    "Threshold Binary",
    "Brightness Threshold",
    "Adaprive Gaussian"
]

class ImageBinarization(object):
    """ 
    The class implements image binarization methods

    Methods
    -------
        convertUsingThresholdBinarization(self, image: cv2.Mat, thresholdValue: int) -> cv2.Mat

        convertUsingBrightnessBinarization(self, image: cv2.Mat) -> cv2.Mat

        convertUsingAdaptiveGaussianBinarization(self, image: cv2.Mat, blockSize: int, c: float) -> cv2.Mat
    """
    def __init__(self):
        self.brightnessBinarization = BrightnessBinarization()
        self.imageUtils = IUtils()

    def convertUsingThresholdBinarization(self, image: cv2.Mat, thresholdValue: int) -> cv2.Mat:
        """
        Converts the source image to a binary using threshold binarization
        """
        return cv2.threshold(self.imageUtils.BGR2GRAY(image), thresholdValue, 255, cv2.THRESH_BINARY)[1]

    def convertUsingBrightnessBinarization(self, image: cv2.Mat) -> cv2.Mat:
        """
        Converts the source image to a binary using brightness binarization
        """
        return self.brightnessBinarization.convert(image)

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

    def convertUsingOtsuThresholding(self):
        pass

class BrightnessBinarization(object):
    """ 
    The class implements binarization based on the average brightness of the image 
    
    Methods
    -------
        convert(sourceImage: cv2.Mat) -> cv2.Mat
            Converts the source image to binary

        __calculateAverageBrightness() -> float
            The method calculates the average brightnesss of the image

        __binarizeImage(self, image: cv2.Mat) -> cv2.Mat
            The method for each pixel compares its average brightness
            with the average brightness of the image

        __getPixelBrightness(self, pixel: list) -> float
            The method calculates the brightness of the pixel
    """
    def __init__(self, ):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def convert(self, sourceImage: cv2.Mat) -> cv2.Mat:
        """ 
        Convert to binary image 

        Parameters
        ----------
            sourceImage: cv2.Mat
                The source image to convert (a set of image pixels)
        """
        self.height, self.width, _ = sourceImage.shape
        self.averageImageBrightness = self.__calculateAverageBrightness()
        return self.__binarizeImage(sourceImage)

    def __calculateAverageBrightness(self) -> float:
        """ 
        The method calculates the average brightnesss of the image 

        Returns
        -------
            averageImageBrightness: float
                Average brightness of image
        """
        self.pixelsBrightness = numpy.zeros([self.height, self.width], dtype=numpy.ubyte)

        for i in range(0, self.height):
            for j in range(0, self.width):
                self.pixelsBrightness[i, j] = self.__getPixelBrightness(self.image[i, j])

        return self.pixelsBrightness.sum() / (self.width * self.height)
    
    def __binarizeImage(self, image: cv2.Mat) -> cv2.Mat:
        """ 
        The method for each pixel compares its average brightness
        with the average brightness of the image

        Parameters
        ----------
            image: Mat
                Local copy of the source image
        
        Returns
        -------
            image: Mat
                Binarized image
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                pxBrightGreaterAvg = self.pixelsBrightness[i, j] > self.averageImageBrightness
                image[i, j] = self.white if pxBrightGreaterAvg else self.black

        return image

    def __getPixelBrightness(self, pixel: list) -> float:
        """ 
        The method calculates the brightness of the pixel
        
        Parameters
        ----------
            pixel: list
                An pixel of image in BGR format
        """
        return 0.299 * pixel[2] + 0.587 * pixel[1] + 0.114 * pixel[0]