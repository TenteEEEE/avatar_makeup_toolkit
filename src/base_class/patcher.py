try:
    from util import improc
except:  # Jupyter env
    from src.util import improc


class patcher:
    def __init__(self, loader, converter, position=[0., 0.], basesize=2048, options={}):
        self.loader = loader
        self.converter = converter
        self.basesize = basesize
        self.position = position
        # when the position is > 1.0, it normalizes the position by basesize
        if True in [p > 1. for p in self.position]:
            self.position = [p / basesize for p in self.position]
        self.options = options
        self.set_options(self.options)

    def __len__(self):
        return len(self.loader)

    def patch(self, texture, index, material=None, mask=None):
        if material is None:
            material = self.load_img(index)
        material = self.convert(material)
        position = [round(self.position[i] * texture.size[i]) for i in range(2)]
        if material is not None:  # if index is out of bounds or <0, material is None
            if mask is None:
                texture = improc.overlay(texture, material, position)
            else:
                texture = improc.overlay_with_mask(texture, material, mask, position)
        return texture

    def set_options(self, options):
        self.loader.options = options
        self.converter.options = options

    def load_img(self, index):
        return self.loader.load_img(index)

    def convert(self, image):
        return self.converter.convert(image)
