"""
Demonstration of middlefield plugins
"""

from __future__ import print_function

import typing

from caparg import command, option
import middlefield


@middlefield.COMMANDS.command(
    parser=command('',
                   what=option(type=typing.List[str],
                               have_default=True)),
    )
def beamer(args, dependencies):
    return
