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
    def binarizeBinaryImage(image: cv2.Mat, threshold: int) -> cv2.Mat:
        for x in range(0, image.shape[0]): # rows
            for y in range(0, image.shape[1]): # columns
                image[x, y] = 255 if image[x, y] > threshold else 0

        return image

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

    @staticmethod
    def performFollowingOperationWithPixels(operation: str, matrix: numpy.array) -> numpy.array:
        """ Remove extra pixels: operation = "remove"
        Fill missing pixels: operation = "fill"
        """
        isRemoveOperation = operation == "remove"
        isFillOperation = operation == "fill"
        isNotAllPixelsChanged = True

        while isNotAllPixelsChanged:
            pixelsToChange = []

            for i in range(1, matrix.shape[0] - 1):
                for j in range(1, matrix.shape[1] - 1):
                    neighbours = IUtils.getPixelNeighbours(matrix, i, j)
                    if isRemoveOperation and matrix[i, j] == 1:
                        if IUtils.isPixelCanBeRemoved(neighbours):
                            pixelsToChange.append((i, j))
                    if isFillOperation and matrix[i, j] == 0:
                        if IUtils.isPixelCanBeFilled(neighbours):
                            pixelsToChange.append((i, j))

            for i, j in pixelsToChange:
                matrix[i, j] = 0 if isRemoveOperation else 1

            if not pixelsToChange:
                isNotAllPixelsChanged = False

        return matrix

    @staticmethod
    def isPixelCanBeRemoved(N: tuple) -> bool:
        """ N - list of neighbours 
        Background - black color (0)
        Image      - white color (1)
        """
        if numpy.sum(N) == 0: return True

        # 2, 6 - background; other - image
        statement1 = numpy.sum([N[:2] + N[3:6] + N[7:]]) == 6
        statement2 = numpy.sum([N[2] + N[6]]) == 0
        if statement1 and statement2: return True

        # 0, 4 - background; other - image
        statement1 = numpy.sum([N[1:4] + N[5:]]) == 6
        statement2 = numpy.sum([N[0] + N[4]]) == 0
        if statement1 and statement2: return True

        # 7, 0, 1 - image; other - background
        statement1 = numpy.sum([N[7:] + N[:2]]) == 3
        statement2 = numpy.sum(N[2:7]) == 0
        if statement1 and statement2: return True

        # 7, 6, 5 - image; other - background
        statement1 = numpy.sum(N[5:]) == 3
        statement2 = numpy.sum(N[:5]) == 0
        if statement1 and statement2: return True

        # 3, 4, 5 - image; other - background
        statement1 = numpy.sum(N[3:6]) == 3
        statement2 = numpy.sum([N[:3] + N[6:]]) == 0
        if statement1 and statement2: return True

        # 1, 2, 3 - image; other - background
        statement1 = numpy.sum(N[1:4]) == 3
        statement2 = numpy.sum([N[4:] + N[0:1]]) == 0
        if statement1 and statement2: return True

        # 1, 3, 5, 7 - image; other - background
        statement1 = numpy.sum(N[1::2]) == 4
        statement2 = numpy.sum(N[::2]) == 0
        if statement1 and statement2: return True

        # 7, 0, 1, 3, 5 - image; other - background
        statement1 = numpy.sum([N[1::2] + N[0:1]]) == 5
        statement2 = numpy.sum(N[2::2]) == 0
        if statement1 and statement2: return True

        # 7, 6, 1, 3, 5 - image; other - background
        statement1 = numpy.sum([N[1::2] + N[6:7]]) == 5
        statement2 = numpy.sum(N[:6:2]) == 0
        if statement1 and statement2: return True

        # 7, 1, 3, 4, 5 - image; other - background
        statement1 = numpy.sum([N[3:6] + N[1:2] + N[7:]]) == 5
        statement2 = numpy.sum([N[0] + N[2] + N[6]]) == 0
        if statement1 and statement2: return True

        # 1, 2, 3, 5, 7 - image; other - background
        statement1 = numpy.sum([N[1:4] + N[5:6] + N[7:]]) == 5
        statement2 = numpy.sum([N[0] + N[4] + N[6]]) == 0
        if statement1 and statement2: return True

        return False

    @staticmethod
    def isPixelCanBeFilled(N: tuple) -> bool:
        """ N - list of neighbours 
        Background - black color (0)
        Image      - white color (1)
        """
        # All white
        if numpy.sum(N) == 8: return True

        # All white except one of them
        if numpy.sum(N) == 7: return True
        
        # 0, 2, 4, 6 - white
        statement1 = numpy.sum(N[::2]) == 4
        statement2 = numpy.sum(N[1::2]) == 0
        if statement1 and statement2: return True
        
        # 6, 5, 4, 3, 2 - white
        statement1 = numpy.sum(N[2:7]) == 5
        statement2 = numpy.sum([N[7:] + N[:2]]) == 0
        if statement1 and statement2: return True
        
        # 6, 7, 0, 1, 2 - white
        statement1 = numpy.sum([N[6:] + N[:3]]) == 5
        statement2 = numpy.sum(N[3:6]) == 0
        if statement1 and statement2: return True
        
        # 0, 1, 2, 3, 4 - white
        statement1 = numpy.sum(N[:5]) == 5
        statement2 = numpy.sum(N[5:]) == 0
        if statement1 and statement2: return True
        
        # 0, 7, 6, 5, 4 - white
        statement1 = numpy.sum([N[0:1] + N[4:]]) == 5
        statement2 = numpy.sum(N[1:4]) == 0
        if statement1 and statement2: return True

        # 0, 1, 2, 4, 5, 6 - white
        statement1 = numpy.sum([N[:3] + N[4:7]]) == 6
        statement2 = numpy.sum([N[3] + N[7]]) == 0
        if statement1 and statement2: return True

        # 6, 7, 0, 2, 3, 4 - white
        statement1 = numpy.sum([N[6:] + N[0:1] + N[2:5]]) == 6
        statement2 = numpy.sum([N[1] + N[5]]) == 0
        if statement1 and statement2: return True

        # 7, 0 - black; other - white
        statement1 = numpy.sum([N[1:7]]) == 6
        statement2 = numpy.sum([N[7] + N[0]]) == 0
        if statement1 and statement2: return True

        # 4, 5 - black; other - white
        statement1 = numpy.sum([N[:4] + N[6:]]) == 6
        statement2 = numpy.sum([N[4] + N[5]]) == 0
        if statement1 and statement2: return True

        # 0, 1 - black; other - white
        statement1 = numpy.sum([N[2:]]) == 6
        statement2 = numpy.sum(N[:2]) == 0
        if statement1 and statement2: return True

        # 3, 4 - black; other - white
        statement1 = numpy.sum([N[:3] + N[5:]]) == 6
        statement2 = numpy.sum(N[3:5]) == 0
        if statement1 and statement2: return True
        
        # 3, 5, 7 - black; other - white
        statement1 = numpy.sum([N[:3] + N[4:5] + N[6:7]]) == 5
        statement2 = numpy.sum(N[3::2]) == 0
        if statement1 and statement2: return True

        # 1, 3, 5 - black; other - white
        statement1 = numpy.sum([N[0:1] + N[2:3] + N[4:5] + N[6:]]) == 5
        statement2 = numpy.sum(N[1:6:2]) == 0
        if statement1 and statement2: return True

        # 1, 3, 7 - black; other - white
        statement1 = numpy.sum([N[0:1] + N[2:3] + N[4:7]]) == 5
        statement2 = numpy.sum([N[3] + N[1] + N[7]]) == 0
        if statement1 and statement2: return True

        # 1, 5, 7 - black; other - white
        statement1 = numpy.sum([N[0:1] + N[6:7] + N[2:5]]) == 5
        statement2 = numpy.sum([N[1] + N[5] + N[7]]) == 0
        if statement1 and statement2: return True

        return False

    @staticmethod
    def getPixelNeighbours(matrix: numpy.array, x: int, y: int) -> tuple:
        """ Return 8-neighbours of image pixel
        t - target pixel
        0, 1, ..., 7 - neighbour pixel index
        7 0 1
        6 t 2
        5 4 3
        """
        return (
            matrix[x - 1, y    ],
            matrix[x - 1, y + 1],
            matrix[x    , y + 1],
            matrix[x + 1, y + 1],
            matrix[x + 1, y    ],
            matrix[x + 1, y - 1],
            matrix[x    , y - 1],
            matrix[x - 1, y - 1],
        )