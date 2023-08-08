#!/usr/bin/env python
"""
File: extract_single_sequence.py
Description: Extract one sub-sequence from reference sequence file
Date: 2022/5/3
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from _io import TextIOWrapper
import click
from Biolib.fasta import Fasta
from Biolib.show_info import Displayer


def main(fasta_file: TextIOWrapper,
         chr_num: str,
         start: int,
         end: int,
         strand: click.Choice(['+', '-']),
         output_file: TextIOWrapper = None):
    for nucl in Fasta(fasta_file).parse():
        if nucl.id == chr_num:
            sub_seq = nucl[start - 1:end]
            if strand == '-':
                sub_seq = sub_seq.get_reverse_complementary_seq()
            sub_seq.id = f'{chr_num}:{start}-{end}({strand})'
            if output_file:
                with output_file as o:
                    o.write(f">{sub_seq.id}\n{sub_seq.seq}\n")
            else:
                print(sub_seq)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-r', '--ref_fasta', 'ref_fasta_file', type=click.File('r'), help='Input reference sequence file. (format: FASTA)')
@click.option('-c', '--chr_name', 'chr_name', help='Chromosome name. (eg:Chr01)')
@click.option('-s', '--start_site', 'start_site', type=int, help='Start site on chromosome.')
@click.option('-e', '--end_site', 'end_site', type=int, help='End site on chromosome.')
@click.option('-S', '--strand', 'strand', type=click.Choice(['+', '-']), help='Direction of the chain.')
@click.option('-o', '--output_file', 'output_file', type=click.File('w'),
              help='Output file, if not specified, print result to terminal as stdout.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=Displayer(__file__.split('/')[-1]).version_info)
def run(ref_fasta_file, chr_name, start_site, end_site, strand, output_file):
    """Extract one sub sequence from reference sequence file."""
    main(ref_fasta_file, chr_name, start_site, end_site, strand, output_file)


if __name__ == '__main__':
    run()
