"""
File: blast.py
Description: Instantiate a blast result file object.
Date: 2021/12/4
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from typing import Union, Tuple
from click import open_file


class Blast:
    def __init__(self, path: Union[str, TextIOWrapper]):
        if isinstance(path, str):
            self.name = path
            self.__open = open(path)
            self.line_num = sum(1 for _ in self.__open)
            self.__open.seek(0)
        else:
            if path.name == '<stdin>':
                self.name = 'stdin'
                self.__open = open_file('-').readlines()
                self.line_num = sum(1 for _ in self.__open)
            else:
                self.name = path.name
                self.__open = path
                self.line_num = sum(1 for _ in self.__open)
                self.__open.seek(0)

# Basic method==========================================================================================================
    def parse(self) -> Tuple[str]:
        """Parse information of each column of BLAST6 file line by line."""
        for line in self.__open:
            split = line.strip().split('\t')
            querry_id, sbject_id, align_rate = split[0], split[1], split[2]
            align_len, mismatch, gap = split[3], split[4], split[5]
            querry_start, querry_end = split[6], split[7]
            sbject_start, sbject_end = split[8], split[9]
            e_value, score = split[10], split[11]
            yield querry_id, sbject_id, align_rate, align_len, \
                querry_start, querry_end, sbject_start, sbject_end, e_value, score

    def get_pair_dict(self, top: int = 3):
        pair_dict = {}  # {query1: {sbject1: [], sbject2: [], ...}, query2: {}, ...}
        for line in self.parse():
            if line[0] not in pair_dict:
                pair_dict[line[0]] = {line[1]: '\t'.join(line[2:])}
            else:
                if len(pair_dict[line[0]]) < top:
                    pair_dict[line[0]][line[1]] = '\t'.join(line[2:])
        return pair_dict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__open.close()
        except AttributeError:
            pass

# File format conversion method=========================================================================================
    def to_bed(self, query_is_chr: bool = False) -> str:
        """Transform the result of align the query sequence with the reference sequence into a BED file."""
        content = ''
        for line in self.parse():
            if not query_is_chr:
                if int(line[6]) - int(line[7]) > 0:
                    content += f'{line[1]}\t{int(line[7]) - 1}\t{line[6]}\t{line[0]}\t.\t-\n'
                else:
                    content += f'{line[1]}\t{int(line[6]) - 1}\t{line[7]}\t{line[0]}\t.\t+\n'
            else:
                if int(line[4]) - int(line[5]) > 0:
                    content += f'{line[0]}\t{int(line[5]) - 1}\t{line[4]}\t{line[1]}\t.\t-\n'
                else:
                    content += f'{line[0]}\t{int(line[4]) - 1}\t{line[5]}\t{line[1]}\t.\t+\n'
        return content