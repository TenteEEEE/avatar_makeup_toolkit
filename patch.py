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
    parser.add_argument('-p', '--part', help='Patch part', type=str)
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
        args.part = args.options['texture_type']
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

    args.module = importlib.import_module('model.' + args.model)
    args.manager = args.module.manager

    if args.part is None and len(args.manager.support_parts) > 1:
        for i, part in enumerate(args.manager.support_parts):
            print(str(i + 1) + ':' + part, end=', ')
        print('q:quit')
        num = -1
        while num > len(args.manager.support_parts) or num < 1:
            print('\nSet part number: ', end='')
            num = input()
            try:
                num = int(num)
            except:
                if num == 'q':
                    exit()
                else:
                    num = -1
        args.part = args.manager.support_parts[num - 1]
    else:
        args.part = args.manager.support_parts[0]
    args.manager.options = args.options
    return args


def patcher_itr(itr, args):
    for i in itr:
        yield i, args


def patch_and_save(args):
    index = args[0]
    args = args[1]
    print(f'Processing:{index+1:04}')
    try:
        out = args.manager.patch_part(args.part, index, transparent=args.transparent)
        out.save(f'{args.fdir}{index+1:04}.png')
        return 1
    except:
        import traceback
        traceback.print_exc()
        return -1


def main():
    args = setup()
    os.makedirs(args.fdir, exist_ok=True)
    file_num = min(args.manager.len_part(args.part))
    if args.all:
        itr = range(file_num)
        with ThreadPoolExecutor(max_workers=int(os.cpu_count() / 2 + .5)) as exe:
            result = exe.map(patch_and_save, patcher_itr(itr, args))
    else:
        if args.index < 0:
            args.index = file_num - 1
        elif args.index > file_num:
            print('The index is out of bounds')
            return -1
        print(f'Processing:{args.index+1:04d}')
        out = args.manager.patch_part(args.part, args.index, transparent=args.transparent)
        out.save(args.output)


if __name__ == '__main__':
    main()
