import cv2

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

        return cv2.resize(image, (width, height))