"""
Demonstration of middlefield plugins
"""

from __future__ import print_function

import os
import shutil

from caparg import command, option
import middlefield


@middlefield.COMMANDS.command(
    parser=command('',
                   outdir=option(type=str),
                   input=option(type=str)),
    dependencies=['executor'])
def beamer(args, dependencies):
    """
    Produce slides and handouts
    """
    xctor = dependencies['executor']
    outdir = os.path.abspath(args.get('outdir', 'build'))
    my_input = args.get('input', 'talk.tex')
    my_input_dir = os.path.dirname(os.path.abspath(my_input))
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(my_input, 'rb') as filep:
        source = filep.read()
    for line in source.decode('utf-8').splitlines():
        line = line.strip()
        if not line.startswith(r'\lstinputlisting'):
            continue
        fname = line.split('{')[1].split('}')[0]
        shutil.copy(os.path.join(my_input_dir, fname),
                    os.path.join(outdir, fname))
    with open(os.path.join(outdir, 'talk.tex'), 'wb') as filep:
        filep.write(b'\\documentclass[ignorenonframetext]{beamer}\n')
        filep.write(source)
    xctor.command(['pdflatex', 'talk.tex']).batch(cwd=outdir)
    with open(os.path.join(outdir, 'handout.tex'), 'wb') as filep:
        filep.write(b'\\documentclass{article}\n')
        filep.write(b'\\usepackage{beamerarticle}\n')
        filep.write(source)
    xctor.command(['pdflatex', 'talk.tex']).batch(cwd=outdir)
    xctor.command(['pdflatex', 'handout.tex']).batch(cwd=outdir)
