import os
import sys
import argparse
import importlib
import random
import json
from concurrent.futures import ThreadPoolExecutor
sys.path.append('./src/')
import model

def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='Choose your model', choices=model.model_list)
    parser.add_argument('-a', '--all', help='',  action='store_true')
    parser.add_argument('-o', '--output', help='File name of the output', type=str, default='patched.png')
    parser.add_argument('-i', '--index', help='Index of the material', type=int, default=0)
    parser.add_argument('-d', '--directory', help='Output directory name when you set all flag', type=str, default='default')
    parser.add_argument('-t', '--transparent', help='Make transparent images for easy overlaying', action='store_true')
    parser.add_argument('-j', '--json', help='Load options from json file. When you set true, all arguments are ignored', type=str)
    args = parser.parse_args()

    args.index -= 1
    if args.json is not None:
        try:
            with open(args.json, 'r') as f:
                args.options = json.load(f)
        except IOError:
            import traceback
            traceback.print_exc()
            return -1
        args.model = args.options['model']
        args.all = args.options['all']
        args.index = args.options['index']
        args.directory = args.options['directory']
        args.transparent = args.options['transparent']
        args.output = args.options['output']
    else:
        args.options = {}

    if args.model is None:
        for i, avatar in enumerate(model.model_list):
            print(str(i + 1) + ':' + avatar, end=', ')
        print('q:quit')
        num = -1
        while num > len(model.model_list) or num < 1:
            print('\nSet your model number: ', end='')
            num = input()
            try:
                num = int(num)
            except:
                if num == 'q':
                    exit()
                else:
                    num = -1
        args.model = model.model_list[num - 1]
        
    if args.directory == 'default':
        args.fdir = f'./converted/{args.model}/'
    else:
        args.fdir = args.directory
        
    if args.fdir[-1] != '/':
        args.fdir += '/'
    return args


def gen_args(module, itr, transp, fdir, options):
    for i in itr:
        yield {'module': module, 'index': i, 'is_transp': transp, 'fdir': fdir, 'options': options}


def patch_and_save(args):
    print(f'Processing:{args["index"]+1:04}')
    p = args['module'].patcher(options=args['options'])
    try:
        out = p.patch(args['index'], transparent=args['is_transp'])
        out.save(f'{args["fdir"]}{args["index"]:04}.png')
        return 1
    except:
        import traceback
        traceback.print_exc()
        return -1


def main():
    args = setup()
    if args == -1:
        return
    os.makedirs(args.fdir, exist_ok=True)
    module = importlib.import_module('model.' + args.model)
    patcher = module.patcher(options = args.options)

    if args.all:
        args.itr = range(len(patcher))
        with ThreadPoolExecutor(max_workers=int(os.cpu_count() / 2 + .5)) as exe:
            result = exe.map(patch_and_save, gen_args(module, args.itr, args.transparent, args.fdir, args.options))
    else:
        if args.index < 0:
            args.index = len(patcher) - 1
        elif args.index > len(patcher):
            print('The index is out of bounds')
            return -1
        print(f'Processing:{args.index+1:04d}')
        out = patcher.patch(args.index, transparent=args.transparent)
        out.save(args.output)


if __name__ == '__main__':
    main()
