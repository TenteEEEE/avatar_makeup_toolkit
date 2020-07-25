import os
import sys
import importlib
import pytest
# sys.path.append('./src/')
import model
from base_class import *


def gen_options(models):
    for m in models:
        module = importlib.import_module('model.' + m)
        manager = module.manager
        for part in manager.support_parts:
            components = manager.patchers_dict[part].keys()
            for index, component in enumerate(components):
                options = {}
                flag = [0] * len(components)
                flag[index] = -1
                options.update(zip(components, flag))
                yield m, manager, part, options


@pytest.mark.parametrize("model, manager, part, options", gen_options(model.model_list))
def test_model_error(model, manager, part, options):
    manager.options = options
    try:
        out = manager.patch_part(part, 0)
        assert True
    except:
        assert False
