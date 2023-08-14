#!/usr/bin/env python
"""
File: get_FPKM.py
Description: Standardize gene expression with FPKM.
Date: 2022/1/10
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import StringIO, TextIOWrapper
from Biolib.statistics import click, pd, get_FPKM
from Biolib.show_info import Displayer
file_content = """
# featureCounts command\n
Geneid  Chr  Start End Strand Length Sample1 Sample2 Sample3 ...\n
gene1   Chr1  1000 3000   +    2000     1       0       0    ...\n
gene2   Chr2  1000 2000   -    1000     21      51      34   ...\n
......  ....  .... .... ..... ...... ....... ....... ....... ...\n
gene100 Chr19 2100 4200   -    2100    2345    2137    1987  ...\n
"""


def main(featureCounts_result_file: TextIOWrapper, out_file_prefix: str = 'FPKM', min_value: float = None) -> None:
    """
    Standardize gene expression with FPKM
    :param featureCounts_result_file: gene expression matrix file generated by featureCounts software (TAB delimiters)

                                      # featureCounts command
                                      Geneid     Chr    Start    End    Strand   Length   Sample1   Sample2   Sample3
                                      gene1      Chr01   100     300      +       200        1         0         0
                                      gene2      Chr02   1000    2000     -      1000       21        51        34
                                      ......     ......  .....   .....  ......   ......   .......   .......   .......
                                      gene1000   Chr19   2100    4200     -      2100      2345      2137      1987

    :param min_value: Gene minimum expression (genes whose expression is less than the specified value in all samples
                      are filtered out). {type=float, default=None}
    :param out_file_prefix: Output file prefix. {type=str, default=FPKM}
    :return: None
    """
    if featureCounts_result_file.name == '<stdin>':
        featureCounts_result_file = ''.join(click.open_file('-').readlines())
        featureCounts_result_file = StringIO(featureCounts_result_file)
        df = pd.read_csv(featureCounts_result_file, lineterminator='\n', skiprows=1, sep='\t', index_col=0).iloc[:, 4:]
    else:
        df = pd.read_table(featureCounts_result_file, header=1, index_col=0).iloc[:, 4:]
    FPKM = get_FPKM(df, min_value)
    FPKM.to_csv(f'./{out_file_prefix}.csv')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--gene_exp', 'gene_exp_file', type=click.File('r'), required=True,
              help=f"""Gene expression matrix file generated by featureCounts software. (TAB delimiters)
              \033[33m\n{file_content}\033[0m""")
@click.option('-m', '--min_exp', 'min_exp', type=float, default=0, show_default=True,
              help='Gene minimum expression threshold in all samples.')
@click.option('-o', '--output_prefix', 'output_prefix', default='FPKM', show_default=True, help='Output file prefix.')
@click.option('-V', '--version', 'version', help='Show author and version information.',
              is_flag=True, is_eager=True, expose_value=False, callback=Displayer(__file__.split('/')[-1]).version_info)
def run(gene_exp_file, min_exp, output_prefix):
    """Standardize gene expression with FPKM."""
    main(gene_exp_file, output_prefix, min_exp)


if __name__ == '__main__':
    run()
