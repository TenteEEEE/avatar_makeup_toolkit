from time import time
import os
import sys
import importlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
sys.path.append('./src/')
import model

models = model.model_list
max_workers = int(os.cpu_count() / 2 + .5)


def gen_args(manager, part, itr, fdir):
    for i in itr:
        yield {'manager': manager, 'part': part, 'index': i, 'fdir': fdir}


def patch(args):
    try:
        out = args['manager'].patch_part(args['part'], args['index'], transparent=True)
        out.save(f'{args["fdir"]}{args["index"]+1:04}.png')
        return 1
    except:
        import traceback
        traceback.print_exc()
        return -1


def convert_all(model_name):
    outdir = './converted/publish/'
    module = importlib.import_module('model.' + model_name)
    manager = module.manager
    for part in manager.support_parts:
        components = manager.patchers_dict[part]
        for index, component in enumerate(components.keys()):
            options = {}
            flag = [-1] * len(components)
            flag[index] = 0
            options.update(zip(components, flag))
            manager.options = options
            fdir = f'{outdir}{model_name}/{part}/{component}/'
            os.makedirs(fdir, exist_ok=True)
            itr = range(manager.len_part('face')[index])
            try:
                with ThreadPoolExecutor(max_workers=max_workers) as e:
                    result = e.map(patch, gen_args(manager, part, itr, fdir))
            except:
                import traceback
                traceback.print_exc()
    print(f'Done: {model_name}')


def main():
    start = time()
    with ProcessPoolExecutor(max_workers=max_workers) as e:
        result = list(e.map(convert_all, models))
    print(time() - start)


if __name__ == '__main__':
    main()
