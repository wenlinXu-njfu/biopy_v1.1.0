#!/usr/bin/env python
"""
File: show_info.py
Description: Show other information.
Date: 2023/8/4
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from io import TextIOWrapper
from typing import Union
from os import system
from datetime import datetime
from click import echo


class Displayer:
    def __init__(self,
                 program: str,
                 author: str = 'Wenlin Xu',
                 contact: str = 'wenlinxu.njfu@outlook.com',
                 version: str = '1.1.0'):
        self.program = program
        self.author = author
        self.contact = contact
        self.version = version

    @staticmethod
    def echo_and_execute_command(command: str, file: Union[str, TextIOWrapper] = None):
        command_prompt = f'[{datetime.now().replace(microsecond=0)}]$ '
        if isinstance(file, str):
            echo(f'\033[33m{command_prompt}\033[0m\033[36m{command}\033[0m', err=True, file=open(file, 'a'))
        elif isinstance(file, TextIOWrapper):
            echo(f'\033[33m{command_prompt}\033[0m\033[36m{command}\033[0m', err=True, file=file)
        else:
            echo(f'\033[33m{command_prompt}\033[0m\033[36m{command}\033[0m', err=True)
        system(command)

    def version_info(self, ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        echo(f'Program: {self.program}\n'
             f'Author: {self.author:>10}\n'
             f'Contact: {self.contact}\n'
             f'Version: {self.version}',
             err=True)
        ctx.exit()
