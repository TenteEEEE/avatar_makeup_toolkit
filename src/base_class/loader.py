import os
from PIL import Image


class loader:
    def __init__(self, material='cheek', rootdir='./material/', options={}):
        self.rootdir = rootdir
        self.set_material(material)
    
    def set_material(self, material):
        self.material = material
        self.filelist = sorted(os.listdir(self.rootdir + self.material))

    def load_img(self, index):
        if 0 <= index and index < len(self.filelist):
            return Image.open(f'{self.rootdir}{self.material}/{self.filelist[index]}')
        else:
            return None
        
    def __len__(self):
        return len(self.filelist)
