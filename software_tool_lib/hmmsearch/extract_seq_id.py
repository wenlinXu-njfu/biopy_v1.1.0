#!/usr/bin/env python
"""
File: extract_seq_id.py
Description: Extract sequence IDs from hmmsearch results
Date: 2022/4/12
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from re import sub
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(hmmseqrch_result_file, out_file):
    id_list = []
    for line in open(hmmseqrch_result_file):
        if line.startswith(' ') and not line.strip().startswith('---') and not line.strip().startswith('E-value'):
            split = sub(r' +', ' ', line.strip()).split(' ')
            seq_id = split[8]
            if seq_id not in id_list:
                id_list.append(seq_id)
        elif line.startswith('Domain'):
            break
    if out_file and id_list:
        with open(out_file, 'w') as o:
            o.write('\n'.join(id_list) + '\n')
    else:
        print('\n'.join(id_list))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--hmmsearch_result', 'hmmsearch_result_file', help='Input hmmsearch results file.')
@click.option('-o', '--output_file', 'output_file',
              help='[optional] Output file, if not specified, print sequences id to terminal as stdout.')
def run(hmmsearch_result_file, output_file):
    """Extract sequence IDs from hmmsearch results"""
    main(hmmsearch_result_file, output_file)


if __name__ == '__main__':
    run()