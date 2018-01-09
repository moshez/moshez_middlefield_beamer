"""
Demonstration of middlefield plugins
"""

from __future__ import print_function

import os
import shutil
import typing
import subprocess

from caparg import command, option
import middlefield


@middlefield.COMMANDS.command(
    parser=command('',
                   outdir=option(type=str),
                   input=option(type=str),
    ),
    dependencies=['executor'])
def beamer(args, dependencies):
    xctor = dependencies['executor']
    outdir = os.path.abspath(args.get('outdir', 'build'))
    input = args.get('input', 'talk.tex')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(input, 'rb') as filep:
       source = filep.read()
    with open(os.path.join(outdir, 'talk.tex'), 'wb') as filep:
       filep.write(b'\\documentclass{beamer}\n')
       filep.write(source)
    xctor.command(['pdflatex', 'talk.tex']).batch(cwd=outdir)
    with open(os.path.join(outdir, 'handout.tex'), 'wb') as filep:
       filep.write(b'\\documentclass{article}\n')
       filep.write(b'\\usepackage{beamerarticle}\n')
       filep.write(source)
    xctor.command(['pdflatex', 'talk.tex']).batch(cwd=outdir)
    xctor.command(['pdflatex', 'handout.tex']).batch(cwd=outdir)
