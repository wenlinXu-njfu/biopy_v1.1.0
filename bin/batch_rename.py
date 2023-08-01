#!/usr/bin/env python
"""
File: batch_rename.py
Description: Batch rename files
Date: 2021-10-06
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from os import listdir, rename
from re import sub
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_dir, old, new):
    files = listdir(in_dir)
    for file in files:
        if new:
            s = sub(old, new, file)
        else:
            s = sub(old, '', file)
        rename(f'{in_dir}/{file}', f'{in_dir}/{s}')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--input_dir_path', 'input_dir', help='The directory where the file to be renamed resides.')
@click.option('-old', '--old_name', 'old', help='The string to be replaced, it supports for regular expressions')
@click.option('-new', '--new_name', 'new', help='Replacement string, it supports for regular expressions')
def run(input_dir, old, new):
    """Batch rename files"""
    main(input_dir, old, new)


if __name__ == '__main__':
    run()