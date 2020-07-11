import os

pathThisFile = os.path.dirname(os.path.abspath(__file__))
module_list = sorted(os.listdir(pathThisFile))
try:
    module_list.remove('__init__.py')
    module_list.remove('__pycache__')
except:
    pass
module_list = [p[:-3] for p in module_list]

__all__ = module_list
