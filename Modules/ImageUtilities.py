import cv2

class IUtils(object):
    @staticmethod
    def BGR2GRAY(bgrImage):
        return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def BGR2RGB(bgrImage):
        return cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)

    @staticmethod
    def readImageFrom(path):
        return cv2.imread(path)

    @staticmethod
    def writeImageTo(path, image):
        try:
            cv2.imwrite(path, image)
            return None
        except IOError as e:
            return e.errno, e.strerror