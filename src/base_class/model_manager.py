import os
from PIL import Image

class model_manager:
    def __init__(self, model, displayname='キッシュ', rootdir="./avatar_texture/", patchers={}, options={}):
        self.model = model
        self.displayname = displayname
        self.rootdir = rootdir + '/' if rootdir[-1] != '/' else rootdir
        self.patchers_dict = patchers
        self.support_parts = list(patchers.keys())
        self.options = options

    def __len__(self):
        return len(self.patchers)

    def len_part(self, part):
        return [len(p[1][0]) for p in self.patchers_dict[part].items()]

    def patch_part(self, part, setindex, transparent=False):
        patched = Image.open(f'{self.rootdir}{self.model}/{part}.png')
        if transparent:
            patched = Image.new("RGBA", patched.size)
        if os.path.exists(f'{self.rootdir}{self.model}/{part}_mask.png'):
            mask = Image.open(f'{self.rootdir}{self.model}/{part}_mask.png').convert('L')
        else:
            mask = None

        part_patchers = self.patchers_dict[part]
        for material in part_patchers.keys():
            index = setindex
            if material in self.options.keys():
                if self.options[material] < 0:  # Ignore patching
                    continue
                elif self.options[material] > 0:  # Index overwite
                    index = self.options[material]
            for p in part_patchers[material]:
                p.set_options(self.options)
                patched = p.patch(patched, index, mask=mask)
        return patched

    def ask(self, question, default=False, default_msg=None):
        if default_msg is None:
            default_msg = 'y' if default else 'n'
        message = question + ' [default:' + default_msg + '] (y/n):'
        while True:
            ans = input(message)
            if ans in ['', 'y', 'n']:
                break
        matching_char = ['', 'y'] if default else ['', 'n']

        if ans in matching_char:
            return True if default else False
        else:
            return False if default else True
