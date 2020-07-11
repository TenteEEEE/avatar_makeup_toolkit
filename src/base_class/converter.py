from PIL import Image


class converter():
    """
    converter provides the converted image and the normalized position
    """

    def __init__(self, position=[.0, .0], options={}):
        self.position = position
        self.converted = {'image': None, 'position': self.position}
        self.options = options

    def convert(self, image):
        return image

    def get_converted(self, image):
        self.converted['image'] = self.convert(image)
        self.converted['position'] = self.position
        return self.converted

    def save(self, fname):
        try:
            self.image.save(fname)
            return 0
        except:
            return -1
