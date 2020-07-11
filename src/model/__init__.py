import os

pathThisFile = os.path.dirname(os.path.abspath(__file__))
model_list = sorted(os.listdir(pathThisFile))
try:
    model_list.remove('__init__.py')
    model_list.remove('__pycache__')
except:
    pass
model_list = [model[:-3] for model in model_list]

__all__ = model_list
