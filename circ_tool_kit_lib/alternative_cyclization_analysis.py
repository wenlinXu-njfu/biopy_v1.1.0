#!/usr/bin/env python
"""
File: alternative_cyclization_analysis.py
Description: CircRNA alternative cyclization sites analysis.
Date: 2023/3/26
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from re import findall
import click
from Biolib.show_info import Displayer


def main(circ_bed_file: str, alt_cyc_min: int, out_file: str, circ_seq_fasta_file: str = None):
    raw_circ_type_dict = None
    if circ_seq_fasta_file:
        raw_circ_type_dict = {line.split(' ')[0].replace('>', ''): line.split(' ')[1].replace('type=', '').strip()
                              for line in open(circ_seq_fasta_file) if line.startswith('>')}
    circ_list = []
    circ_type_dict = {}  # {'Chr01:100|x\t+': 'exonic', 'Chr01:x|1000\t-': 'exonic,intronic'}
    for line in open(circ_bed_file):
        split = line.strip().split('\t')
        circ_id, strand = split[3], split[5]
        alternative_three = circ_id.replace(circ_id.split('|')[1], 'x') + f'\t{strand}'  # Chr01:100|x\t+
        alternative_five = circ_id.replace(circ_id.split(':')[1].split('|')[0], 'x') + f'\t{strand}'  # Chr01:x|100\t+
        circ_list.extend([alternative_three, alternative_five])
        if raw_circ_type_dict:
            try:
                circ_type = raw_circ_type_dict[circ_id]
            except KeyError:
                circ_type = 'unclassified'
            if alternative_three in circ_type_dict:
                if circ_type not in circ_type_dict[alternative_three]:
                    circ_type_dict[alternative_three] += f',{circ_type}'
            else:
                circ_type_dict[alternative_three] = circ_type
            if alternative_five in circ_type_dict:
                if circ_type not in circ_type_dict[alternative_five]:
                    circ_type_dict[alternative_five] = f',{circ_type}'
            else:
                circ_type_dict[alternative_five] = circ_type
    unique_circ = list(set(circ_list))
    unique_circ.sort(key=lambda i: (findall(r'[a-zA-Z]+', i.split(':')[0])[0],
                                    int(findall(r'\d+', i.split(':')[0])[0]),
                                    int(findall(r'\d+', i.split(':')[1])[0])))
    content = []
    for j in unique_circ:
        if circ_list.count(j) >= alt_cyc_min:
            if raw_circ_type_dict:
                circ_type = circ_type_dict[j]
                if circ_type.startswith(','):
                    circ_type = circ_type.replace(',', '', 1)
                content.append(f'{j}\t{circ_list.count(j)}\t{circ_type}\n')
            else:
                content.append(f'{j}\t{circ_list.count(j)}\n')
    content = ''.join(content)
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-b', '--circ_bed', 'circ_bed_file',
              help='Input circRNA BED file.\n(Chr_num\\tStart\\tEnd\\tCirc_ID\\tFrame\\tStrand\\tEtc)')
@click.option('-f', '--circ_fasta', 'circ_fasta_file',
              help='CircRNA sequence FASTA file generated by CircToolKit subcommand "get_circ_seq" '
                   'to annotate the type of circRNA.')
@click.option('-n', '--alt_circ_num', 'alt_circ_num', type=int, default=2, show_default=True,
              help='Output sites which the number of alternative cyclization site exceeds specified value.')
@click.option('-o', '--output_file', 'outfile',
              help='Output file, if not specified, print results to terminal as stdout.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=Displayer(__file__.split('/')[-1]).version_info)
def run(circ_bed_file, circ_fasta_file, alt_circ_num, outfile):
    """CircRNA alternative cyclization sites analysis."""
    main(circ_bed_file, alt_circ_num, outfile, circ_fasta_file)


if __name__ == '__main__':
    run()
