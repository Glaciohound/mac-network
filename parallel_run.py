#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : parallel_run.py
# Author            : Chi Han
# Email             : haanchi@gmail.com
# Date              : 17.10.2019
# Last Modified Date: 17.10.2019
# Last Modified By  : Chi Han
#
# Welcome to this little kennel of Glaciohound!


import os
import argparse
from multiprocessing import Process


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', type=str)
    parser.add_argument('--gpus', nargs=4)
    parser.add_argument('--log_dir',
                        default='../data/log/mac/tf_version/results')
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    return args


def get_expName(command):
    splits = command.split(' ')
    index = splits.index('--expName') + 1
    expName = splits[index]
    return expName


def main():
    args = get_args()
    processes = []

    for i in range(4):
        command_head = f'python main.py --gpus {args.gpus[i]}'
        command_body = args.command.format(i)
        expName = get_expName(command_body)

        if i == 0:
            command_output = ''
        else:
            output_file = os.path.join(args.log_dir, expName, 'log.txt')
            os.makedirs(os.path.dirname(os.path.abspath(output_file)),
                        exist_ok=True)
            command_output = f'> {output_file} 2> {output_file}'

        command = ' '.join([command_head, command_body, command_output])

        print('\nCommand:')
        print(command)
        if args.run:
            print('Running the command above...')
            processes.append(Process(target=os.system, args=(command,)))
            print('Done')

    for p in processes:
        p.start()
    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
