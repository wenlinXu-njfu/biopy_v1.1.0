#!/usr/bin/env python
"""
File: id_index_seq.py
Description: Extract sequences from FASTA file based on the id provided.
Date: 2022/3/25
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from typing import Tuple
from io import TextIOWrapper
from os.path import abspath
import click
from pybioinformatic import Fasta, Displayer, __version__
displayer = Displayer(__file__.split('/')[-1], version=__version__)


def main(fasta_files: Tuple[TextIOWrapper],
         parse_seqids: bool,
         id_file: TextIOWrapper,
         match: bool,
         log_file: TextIOWrapper,
         output_file: TextIOWrapper):
    raw_id_set = set(line.strip() for line in id_file)
    have_found_id_set = set()
    for fasta_file in fasta_files:
        file_name = abspath(fasta_file.name).replace('<', '').replace('>', '')
        for seq_obj in Fasta(fasta_file).parse(parse_seqids):
            if match and seq_obj.id in raw_id_set:
                have_found_id_set.add(seq_obj.id)
                seq_obj.id = f'{seq_obj.id} from={file_name}'
                click.echo(seq_obj, output_file)
            elif not match:
                for _id in raw_id_set:
                    if seq_obj.id in _id or _id in seq_obj.id:
                        have_found_id_set.add(_id)
                        seq_obj.id = f'{seq_obj.id} from={file_name}'
                        click.echo(seq_obj, output_file)
    # report sequence that not found.
    not_found_id = list(raw_id_set - have_found_id_set)
    if not_found_id:
        not_found_id.sort()
        msg = ' not found\n'.join(not_found_id) + ' not found\n'
        click.echo(f'\033[33m{msg}\033[0m', err=True, file=log_file)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('fasta_files', nargs=-1, metavar='<fasta files>', required=True, type=click.File('r'))
@click.option('-P', '--parse_seqids', 'parse_seqids',
              is_flag=True, flag_value=True,
              help='Parse sequence id in FASTA file.')
@click.option('-id', '--id_file', 'id_file',
              metavar='<file>', type=click.File('r'), required=True,
              help='Input id file (one id per line).')
@click.option('--match/--contain',
              default=True, show_default=True,
              help='Whether the id supplied should exactly match the ID of the sequence.')
@click.option('-log', '--log_file', 'log_file',
              metavar='<file>', type=click.File('w'),
              help='Output log file, if not specified, the log will print to terminal as stderr.')
@click.option('-o', '--output_file', 'outfile',
              metavar='<file>', type=click.File('w'),
              help='Output file, if not specified, print results to terminal as stdout.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=displayer.version_info)
def run(fasta_files, parse_seqids, id_file, match, log_file, outfile):
    """Extract sequences from FASTA file based on the id provided."""
    main(fasta_files, parse_seqids, id_file, match, log_file, outfile)


if __name__ == '__main__':
    run()
