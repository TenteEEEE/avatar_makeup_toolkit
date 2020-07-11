import os
import sys
import importlib

pathThisFile = os.path.dirname(os.path.abspath(__file__))
module_list = sorted(os.listdir(pathThisFile))
try:
    module_list.remove('__init__.py')
    module_list.remove('__pycache__')
except:
    pass
module_list = [p[:-3] for p in module_list]

for mod_name in module_list:
    myself = sys.modules[__name__]
    mod = importlib.import_module(__name__ + "." + mod_name)
    for m in mod.__dict__.keys():
        if not m in ['__builtins__', '__doc__', '__file__', '__name__', '__package__']:
            myself.__dict__[m] = mod.__dict__[m]
