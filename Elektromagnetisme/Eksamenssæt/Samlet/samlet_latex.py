import numpy as np
import os
from dataclasses import dataclass
import re

@dataclass
class latex_tekst:
    path: str

    def get_tekst(self):
        f = [open(self.path, 'r').read()][0].split('\n')
        for i in range(len(f)):
            if 'begin{document}' in f[i]:
                f = f[i+3:-2]
                print('hej')
                break
        return f

def find_paths():
    paths = []
    for f in os.walk('../'):
        if [f for f in f[2] if '.tex' in f] != []:
            paths.append(f[0] + '/' + str([f for f in f[2] if '.tex' in f][0]))
    return paths

print(find_paths())

def make_latex():
    tekst = []

    for f in find_paths():
        if 'preamble' in f:
            continue

        # latex_tekst.append(latex_tekst(f).get_tekst())
        print(latex_tekst(f).get_tekst())

    return latex_tekst

print(make_latex())






