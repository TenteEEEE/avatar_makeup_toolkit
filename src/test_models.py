import os
import sys
import importlib
import pytest
# sys.path.append('./src/')
import model
from base_class import *

def gen_options():
    imgloader = loader()
    for index, component in enumerate(imgloader.components):
        options = {}
        flag = [0]*len(imgloader.components)
        flag[index] = -1
        options.update(zip(imgloader.components, flag))
        yield options

@pytest.mark.parametrize("model_name", model.model_list)
@pytest.mark.parametrize("options", gen_options())
def test_model_error(model_name, options):
    # Testing each model with index overwrite options
    module = importlib.import_module('model.' + model_name)
    patcher = module.patcher(options=options)
    try:
        out = patcher.patch(0)
        assert True
    except:
        assert False
