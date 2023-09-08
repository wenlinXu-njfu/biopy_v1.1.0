#!/usr/bin/env python
"""
File: gff_sort.py
Description: Sort the GFF file by sequence ID.
Date: 2022/3/31
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
import click
from Biolib import Gff, Displayer, __version__
displayer = Displayer(__file__.split('/')[-1], version=__version__)


def main(gff_file: TextIOWrapper, out_file: TextIOWrapper = None):
    gff_file_obj = Gff(gff_file)
    for line in gff_file_obj.gff_sort():
        click.echo(line, out_file)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--gff_file', 'gff_file', type=click.File('r'), required=True, help='Input unsorted GFF file.')
@click.option('-o', '--output_file', 'output_file', type=click.File('w'),
              help='Output sorted GFF file, if not specified, print results to terminal as stdout.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=displayer.version_info)
def run(gff_file, output_file):
    """Sort the GFF file by sequence ID."""
    main(gff_file, output_file)


if __name__ == '__main__':
    run()
