#!/usr/bin/env python
"""
File: draw_chr_distribution.py
Description: Draw snp distribution.
CreateDate: 2024/5/12
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import StringIO
from pandas import read_table
from natsort import natsort_key
import matplotlib.pyplot as plt
import click
from pybioinformatic import TaskManager, Displayer
displayer = Displayer(__file__.split('/')[-1], version='0.1.0')


def main(chr_len_file: str,
         snp_ref_file: str,
         window_size: int = 100000,
         n: int = 8,
         cmap: str = 'RdYlGn',
         output_file: str = 'snp.distribution.pdf'):
    # Step1: parse chromosome length file.
    with open(chr_len_file) as len_file:
        len_dict = {
            line.strip().split('\t')[0]: int(line.strip().split('\t')[1])
            for line in len_file if line.strip()
        }
    len_dict = {key: len_dict[key] for key in sorted(len_dict, key=natsort_key, reverse=False)}

    # Step3: stat snp for each window.
    tkm = TaskManager(num_processing=1)
    snp_ref = r"awk -F'\t' '{print $2,$3-1,$3}' OFS='\t' %s | sort -uV" % snp_ref_file
    cmd = f"bedtools makewindows -g <(sort -uV {chr_len_file}) -w {window_size} | intersectBed -a - -b <({snp_ref}) -c"
    stdout = tkm.echo_and_exec_cmd(cmd)
    snp_count = read_table(
        filepath_or_buffer=StringIO(stdout),
        header=None,
        names=['BedChr', 'BedStart', 'BedEnd', 'SnpCount'],
        dtype={'BedChr': str, 'BedStart': int, 'BedEnd': int, 'SnpCount': int}
    )
    snp_count.loc[snp_count.SnpCount >= n, 'SnpCount'] = n
    snp_count['X-coordinate'] = snp_count.BedStart + (snp_count.BedEnd - snp_count.BedStart) / 2
    y = len(len_dict)
    for chromosome in len_dict.keys():
        snp_count.loc[snp_count.BedChr == chromosome, 'Y-coordinate'] = y
        y -= 1

    # Step4: draw snp distribution.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # delete y ticks
    plt.tick_params('y', length=0)
    # hide three frames
    ax.spines['top'].set_color(None)
    ax.spines['right'].set_color(None)
    ax.spines['left'].set_color(None)
    # set x, y ticks and labels
    y_ticks = range(len(len_dict), 0, -1)
    y_labels = list(len_dict.keys())
    plt.yticks(ticks=y_ticks, labels=y_labels)
    x_ticks = [i for i in range(0, max(len_dict.values()) - 10 ** 8, 10 ** 8)]
    x_ticks.append(max(len_dict.values()))
    x_labels = ['%.2f' % int(i / 10 ** 6) for i in range(0, max(len_dict.values()) - 10 ** 8, 10 ** 8)]
    x_labels.append('%.2f' % (max(len_dict.values()) / 10**6))
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.xlabel('Mb', loc='right')
    plt.xlim(0, max(len_dict.values()) + 10*6)
    # draw snp distribution
    if cmap == 'RdYlGn':
        cmap = plt.get_cmap('RdYlGn').reversed()
    scatter = ax.scatter(
        x='X-coordinate',
        y='Y-coordinate',
        c='SnpCount',
        s=100,
        marker='|',
        cmap=cmap,
        data=snp_count
    )
    colorbar_tickslabel = []
    for i in range(0, n + 1):
        colorbar_tickslabel.append(str(i)) if i < n else colorbar_tickslabel.append(f'>{n}')
    cbar = plt.colorbar(mappable=scatter, ticks=range(n + 1))
    cbar.ax.set_yticklabels(colorbar_tickslabel)
    plt.savefig(output_file, bbox_inches='tight')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--snp-ref', 'snp_ref',
              metavar='<file>', required=True,
              help=r'Input snp.ref.xls file. (ID\tChr\tPos\tEtc)')
@click.option('-l', '--chr-len', 'chr_len',
              metavar='<file>', required=True,
              help=r'Input chromosome length file. (ChrName\tChrLength)')
@click.option('-w', '--window-size', 'window_size',
              metavar='<int>', type=int, default=100000, show_default=True,
              help='Window size.')
@click.option('-n', '--max-count', 'max_count',
              metavar='<int>', type=int, default=4, show_default=True,
              help='Max count of colormap.')
@click.option('-cmap', '--color-map', 'color_map',
              metavar='<str>', default='RdYlGn', show_default=True,
              help='Color map of colorbar.')
@click.option('-o', '--output-file', 'output_file',
              metavar='<file>', default='snp.distribution.pdf', show_default=True,
              help='Output file.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=displayer.version_info)
def run(snp_ref, chr_len, window_size, max_count, color_map, output_file):
    """Draw snp distribution."""
    main(chr_len_file=chr_len,
         snp_ref_file=snp_ref,
         window_size=window_size,
         n=max_count,
         cmap=color_map,
         output_file=output_file)


if __name__ == '__main__':
    run()
