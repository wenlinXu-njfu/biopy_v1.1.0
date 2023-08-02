#!/usr/bin/env python
"""
File: fasta_conversion.py
Description: Make each sequence to be displayed on a single line or in multiple lines
Date: 2022/3/23
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file, char_num, out_file):
    fa_file_obj = Fasta(in_file)
    content = []
    if char_num == 0:
        for seq in fa_file_obj.merge_sequence():
            if not out_file:
                print(seq.strip())
            else:
                content.append(seq)
    else:
        generator = fa_file_obj.split_sequence(char_num)
        for line in generator:
            if out_file:
                content.append(line)
            else:
                print(line.strip())
    if out_file and content:
        with open(out_file, 'w') as o:
            o.write(''.join(content))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--fasta_file', 'fasta_file', help='Input FASTA file.')
@click.option('-n', '--char_num', 'char_num', type=int, default=60,
              help='Specify how many character show in per line, 0 presents one line show per sequence. {default: 60}')
@click.option('-o', '--output_file', 'outfile',
              help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(fasta_file, char_num, outfile):
    """Make each sequence to be displayed on a single line or in multiple lines."""
    main(fasta_file, char_num, outfile)


if __name__ == '__main__':
    run()
