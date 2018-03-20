# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 09:52:52 2017

@author: Owner
"""

from cx_Freeze import setup, Executable

base = None
includefiles = ["readme.txt"]

setup(name="game",
      version="1.0",
      description="BlackJack",
      options={"build_exe": {"include_files": includefiles}},
      executables=[Executable("blackjack.py", base=base)])
