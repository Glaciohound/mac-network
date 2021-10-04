#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : inspect_results.py
# Author            : Chi Han
# Email             : haanchi@gmail.com
# Date              : 27.10.2019
# Last Modified Date: 28.10.2019
# Last Modified By  : Chi Han
#
# Welcome to this little kennel of Glaciohound!


import numpy as np
import argparse
import os
from IPython import embed


def stat(data_dir, series, indexes, split):
    results = []
    for i in indexes:
        name = f'{series}{i}'
        with open(os.path.join(data_dir, f'{name}/results-{name}.csv'),
                  'r') as f:
            last_line = f.readlines()[-1]
        split_i = {'train': 1, 'val': 2, 'test': 3}[split]
        last_test = float(last_line.split(',')[split_i])
        results.append(last_test)
    output = {'mean': np.mean(results),
              'std': np.std(results, ddof=1),
              'raw': results}
    return output


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str,
                        default='../data/log/mac/tf_version/results/')
    parser.add_argument('--series', type=str, required=True)
    parser.add_argument('--ipython', action='store_true')
    parser.add_argument('--indexes', type=int, nargs='+',
                        default=[0, 1, 2, 3])
    parser.add_argument('--split', default='test',
                        choices=['train', 'test', 'val'])
    args = parser.parse_args()
    return args


def main(args):
    results = stat(args.data_dir, args.series, args.indexes, args.split)
    print(results)
    if args.ipython:
        embed()


if __name__ == '__main__':
    args = get_args()
    main(args)
