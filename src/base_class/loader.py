import os
from PIL import Image
from queue import Queue
from threading import Thread


class loader:
    def __init__(self, fdir='./material/', queuesize=8):
        self.fdir = fdir
        self.set_components(os.listdir(fdir))
        self.Q = Queue(maxsize=queuesize)

    def set_components(self, components):
        self.components = components
        self.flist = {}
        self.data_num = 0
        for component in self.components:
            self.flist[component] = sorted(os.listdir(self.fdir + component))
            if len(self.flist[component]) > self.data_num:
                self.data_num = len(self.flist[component])

    def make_query(self, index):
        query = {}
        for key in self.components:
            try:
                query[key] = self.flist[key][index]
            except:
                pass
        return query

    def load_img(self, index, key):
        return Image.open(f'{self.fdir}{key}/{self.flist[key][index]}')

    def load_imgs(self, index):
        query = self.make_query(index)
        return self.load_imgs_by_query(query)

    def load_imgs_by_query(self, query):
        imgs = {}
        for k in query.keys():
            imgs[k] = Image.open(f'{self.fdir}{k}/{query[k]}')
        return imgs

    def len(self):
        return self.Q.qsize()

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

    def update(self):
        index = 0
        while True:
            query = self.make_query(index)
            if len(query) != 0:
                imgs = self.load_imgs(query)
                self.Q.put(imgs)
                index += 1
            else:
                break

    def read(self):
        return self.Q.get()
