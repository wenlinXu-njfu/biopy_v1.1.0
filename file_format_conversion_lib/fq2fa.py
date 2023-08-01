#!/usr/bin/env python
"""
File: fq2fa.py
Description: Convert FASTQ to FASTA
Date: 2022/4/22
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from gzip import GzipFile
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fq_file, out_file):
    content = []
    try:
        with open(fq_file) as f:
            while 1:
                read_id = f.readline().replace('@', '>')
                if not read_id:
                    break
                seq = f.readline()
                f.readline()
                f.readline()
                if out_file:
                    content.extend([read_id, seq])
                else:
                    print(read_id.strip())
                    print(seq.strip())
    except UnicodeDecodeError:
        with GzipFile(fq_file) as f:
            while 1:
                read_id = str(f.readline(), 'utf8').replace('@', '>')
                if not read_id:
                    break
                seq = str(f.readline(), 'utf8')
                f.readline()
                f.readline()
                if out_file:
                    content.extend([read_id, seq])
                else:
                    print(read_id.strip())
                    print(seq.strip())


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--fastq_file', 'fastq_file', help='Input FASTQ file(XXX.fq) or FASTQ compressed files(XXX.fq.gz).')
@click.option('-o', '--output_fasta', 'fasta_file',
              help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(fastq_file, fasta_file):
    """Convert FASTQ to FASTA."""
    main(fastq_file, fasta_file)


if __name__ == '__main__':
    run()
