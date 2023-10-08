#!/usr/bin/env python
"""
File: get_TPM.py
Description: Standardize gene expression with TPM based on HTSeq results.
Date: 2023/6/16
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from pandas import read_table
import click
from pybioinformatic import get_TPM, Gtf, Gff, Displayer


def main(header_file: str, htseq_file: TextIOWrapper, anno_file: TextIOWrapper, min_exp: float, output_file: str):
    parse_anno_file = {'gff': Gff, 'gff3': Gff, 'gtf': Gtf}
    file_obj = parse_anno_file[anno_file.name.split('.')[-1]](anno_file)
    length_dict = {}
    for line in file_obj.parse():
        if line[2] == 'exon':
            length = int(line[4]) - int(line[3]) + 1
            if isinstance(file_obj, Gff):
                transcript_id = line[-1]['Parent']
            else:
                transcript_id = line[-1]['transcript_id']
            if transcript_id in length_dict:
                length_dict[transcript_id] += length
            else:
                length_dict[transcript_id] = length
    columns = [line.strip() for line in header_file]
    df = read_table(htseq_file, index_col=0, names=columns).iloc[:-5]
    df.insert(0, 'length', 0)
    for transcript_id in df.index.tolist():
        df.loc[transcript_id, 'length'] = length_dict[transcript_id]
    TPM = get_TPM(df, min_exp)
    TPM.to_csv(f'./{output_file}')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--header_infor', 'header_infor_file',
              metavar='<header file>', type=click.File('r'), required=True,
              help='Input header file. (eg. Gene_id\\nSample1\\nSample2\\netc\\n)')
@click.option('-I', '--htseq_result', 'htseq_result_file',
              metavar='<htseq file>', type=click.File('r'), required=True,
              help='Input Htseq results file.')
@click.option('-a', '--anno_file', 'anno_file',
              metavar='<anno file>', type=click.File('r'), required=True,
              help='Input genome annotation GFF or GTF file, must contain exon information.')
@click.option('-m', '--min_exp', 'min_exp',
              metavar='<float>', type=float, default=0, show_default=True,
              help='Gene minimum expression threshold in all samples.')
@click.option('-o', '--output_file', 'output_file',
              metavar='<str>', default='htseq_TPM.xls', show_default=True,
              help='Output file.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=Displayer(__file__.split('/')[-1]).version_info)
def run(header_infor_file, htseq_result_file, anno_file, min_exp, output_file):
    """Standardize gene expression with TPM based on HTSeq results."""
    main(header_infor_file, htseq_result_file, anno_file, min_exp, output_file)


if __name__ == '__main__':
    run()
