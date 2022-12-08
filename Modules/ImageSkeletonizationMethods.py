from Modules.ImageUtilities import IUtils
import cv2
import numpy



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
