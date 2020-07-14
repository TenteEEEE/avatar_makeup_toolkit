from time import time
import os
import sys
import importlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
sys.path.append('./src/')
import model

models = model.model_list
max_workers = int(os.cpu_count() / 2 + .5)


def gen_args(patcher, itr, fdir):
    for i in itr:
        yield {'patcher': patcher, 'index': i, 'fdir': fdir}


def patch(args):
    try:
        out = args['patcher'].patch(args['index'], transparent=True)
        out.save(f'{args["fdir"]}{args["index"]:04}.png')
        return 1
    except:
        import traceback
        traceback.print_exc()
        return -1


def convert_all(model):
    outdir = './converted/publish/'
    module = importlib.import_module('model.' + model)
    patcher = module.patcher()
    for key in patcher.converters.keys():
        options = {'cheek': -1, 'eye_brow': -1, 'eye_line': -1, 'eye_shadow': -1, 'lip': -1}
        options[key] = 0
        patcher.options = options
        fdir = f'{outdir}{model}/{key}/'
        os.makedirs(fdir, exist_ok=True)
        itr = range(len(patcher))
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as e:
                result = e.map(patch, gen_args(patcher, itr, fdir))
        except:
            import traceback
            traceback.print_exc()
    print(f'Done: {model}')

def main():
    start = time()
    with ProcessPoolExecutor(max_workers=max_workers) as e:
        result = list(e.map(convert_all, models))
    print(time() - start)

if __name__ == '__main__':
    main()
