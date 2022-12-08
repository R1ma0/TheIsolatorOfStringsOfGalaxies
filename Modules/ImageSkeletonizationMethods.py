from Modules.ImageUtilities import IUtils
import cv2
import numpy

class OPCASkeletonization(object):
    """
    Implementation of the One-Pass Combination Algorithm skeletonization method
    """
    def execute(self, srcImage: cv2.Mat) -> cv2.Mat:
        self.matrix = IUtils.convertToBinaryMatrix(srcImage)
        rows = srcImage.shape[0]
        colums = srcImage.shape[1]
        notAllElementsRemoved = True

        # Iterative processing of the image matrix
        while notAllElementsRemoved:
            self.deletedElementsCounter = 0

            # Removing extra matrix elements
            for row in range(1, rows - 2):
                for col in range(1, colums - 2):
                    if self.matrix[row, col] == 1:
                        neighbours = self.__getNeighbours(row, col)
                        if self.__isSatisfiesFirstCondition(neighbours) and \
                           self.__isSatisfiesSecondCondition(neighbours) and \
                           self.__isSatisfiesThirdCondition(neighbours):
                            self.matrix[row, col] = 0

                            self.deletedElementsCounter += 1

            if self.deletedElementsCounter == 0:
                notAllElementsRemoved = False

        # Removing extra matrix elements
        for row in range(1, rows - 2):
            for col in range(1, colums - 2):
                if self.matrix[row, col] == 1:
                    neighbours = self.__getNeighbours(row, col)
                    if self.__isSatisfiesFourthCondition(neighbours):
                        self.matrix[row, col] = 0

        # IUtils.deleteSinglePixels(self.matrix, self.__getNeighbours, rows, colums, 2)
        # print("OPCA skeletonization is done")

        return IUtils.makeChangesToSourceImage(self.matrix, srcImage)

    def __getNeighbours(self, row: int, col: int) -> numpy.array:
        return numpy.array([
            self.matrix[row    , col    ], # p1
            self.matrix[row - 1, col    ], # p2
            self.matrix[row - 1, col + 1], # p3
            self.matrix[row    , col + 1], # p4
            self.matrix[row + 1, col + 1], # p5
            self.matrix[row + 1, col    ], # p6
            self.matrix[row + 1, col - 1], # p7
            self.matrix[row    , col - 1], # p8
            self.matrix[row - 1, col - 1], # p9
            self.matrix[row    , col + 2], # p10
            self.matrix[row + 2, col    ], # p11
        ])

    def __isSatisfiesFirstCondition(self, neighbours: numpy.array) -> bool: 
        pixelsSum = 0
        for k in range(1, 9):
            pixelsSum += neighbours[k]
        return True if pixelsSum >= 2 and pixelsSum <= 6 else False

    def __isSatisfiesSecondCondition(self, neighbours: numpy.array) -> bool:
        sumOfValues = 0
        for k in range(1, 9):
            sumOfValues += abs(neighbours[k] - neighbours[((k - 1) % 8) + 2])
        return True if sumOfValues == 2 else False

    def __isSatisfiesThirdCondition(self, neighbours: numpy.array) -> bool:
        return not (
            neighbours[3]  == 1 and 
            neighbours[7]  == 0 and 
            neighbours[9]  == 0 or 
            neighbours[5]  == 1 and 
            neighbours[1]  == 0 and 
            neighbours[10] == 0
        )

    def __isSatisfiesFourthCondition(self, neighbours: numpy.array) -> bool:
        indexes = [2, 4, 6, 8]
        results = numpy.zeros([4], dtype=numpy.int8)
        for index, value in enumerate(indexes):
            result = neighbours[value] == 0 and \
                     neighbours[((value + 1) % 8) + 2] == 1 and \
                     neighbours[((value + 3) % 8) + 2] == 1
            if result == True:
                results[index] = 1
        return True if numpy.sum(results) == 4 else False



class ZSSkeletonization(object):
    """
    Implementation of the Zhang-Suen skeletonization method
    """
    def execute(self, image: cv2.Mat) -> cv2.Mat:
        self.matrix = IUtils.convertToBinaryMatrix(image)
        stepOneChanges = stepTwoChanges = 1
        rows = image.shape[0] # height
        columns = image.shape[1] # width
        
        while stepOneChanges or stepTwoChanges:
            # Step 1
            stepOneChanges = []
            for x in range(1, rows - 1):
                for y in range(1, columns - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = IUtils.getPixelNeighbours(self.matrix, x, y)
                    if (
                        self.matrix[x, y] == 1 and
                        2 <= sum(n) <= 6 and
                        self.__getTransitions(n) == 1 and
                        P2 * P4 * P6 == 0 and
                        P4 * P6 * P8 == 0
                    ):
                        stepOneChanges.append((x, y))

            for x, y in stepOneChanges:
                self.matrix[x, y] = 0
            # Step 2
            stepTwoChanges = []
            for x in range(1, rows - 1):
                for y in range(1, columns - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = IUtils.getPixelNeighbours(self.matrix, x, y)
                    if (
                        self.matrix[x, y] == 1 and
                        2 <= sum(n) <= 6 and
                        self.__getTransitions(n) == 1 and
                        P2 * P4 * P8 == 0 and
                        P2 * P6 * P8 == 0
                    ):
                        stepTwoChanges.append((x, y))

            for x, y in stepTwoChanges:
                self.matrix[x, y] = 0

        # self.matrix = IUtils.deleteSinglePixels(self.matrix, IUtils.getPixelNeighbours, rows, columns, 1)
        # print("ZS skeletonization is done")
        
        return IUtils.makeChangesToSourceImage(self.matrix, image)

    def __getTransitions(self, neighbours: list) -> int:
        """
        Return sum of transitionf fro m 0 to 1 in pixel neighbours
        """
        n = neighbours + neighbours[0:1] # P2, P3, ... , P9, P2
        return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:])) # (P2, P3), (P3, P4), ..., (P8, P9), (P9, P2)
