"""
Demonstration of middlefield plugins
"""

from __future__ import print_function

import typing

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
    shutil.copy(input, os.path.join(outdir, 'talk.tex'))
    executor.command(['pdflatex', 'talk.tex']).batch(cwd=outdir)
