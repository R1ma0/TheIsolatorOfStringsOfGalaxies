import cv2
import numpy

class IUtils(object):
    @staticmethod
    def BGR2GRAY(bgrImage: cv2.Mat) -> cv2.Mat:
        return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def BGR2RGB(bgrImage: cv2.Mat) -> cv2.Mat:
        return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)

    @staticmethod
    def readImageFrom(path: str):
        return cv2.imread(path)

    @staticmethod
    def writeImageTo(path: str, image: cv2.Mat):
        try:
            cv2.imwrite(path, image)
            return None
        except IOError as e:
            return e.errno, e.strerror

    @staticmethod
    def resizeImage(image: cv2.Mat, scalePercent: int) -> cv2.Mat:
        scaleValue = scalePercent / 100
            
        width = int(image.shape[1] * scaleValue)
        height = int(image.shape[0] * scaleValue)

        return cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def convertToBinaryMatrix(image: cv2.Mat) -> numpy.array:
        height = image.shape[0] # rows
        width = image.shape[1] # columns
        matrix = numpy.zeros((height, width), dtype=numpy.ubyte)
        
        for x in range(0, height):
            for y in range(0, width):
                if image[x, y] == 255:
                    matrix[x, y] = 1
        
        return matrix

    @staticmethod
    def makeChangesToSourceImage(matrix: numpy.array, image: cv2.Mat) -> cv2.Mat:
        for x in range(0, image.shape[0]): # rows
            for y in range(0, image.shape[1]): # columns
                image[x, y] = 255 if matrix[x, y] == 1 else 0

        return image
