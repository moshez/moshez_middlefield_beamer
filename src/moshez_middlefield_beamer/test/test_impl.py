from __future__ import print_function

import unittest

from middlefield_echo import _impl


class ImplTest(unittest.TestCase):

    def test_echo_printer(self):
        res = _impl.echo_printer({}, {})
        self.assertIs(res, print)

    def test_echo(self):
        lst = []
        _impl.echo(dict(what=['hello', 'world']),
                   dict(echo_printer=lambda *args: lst.append(args)))
        self.assertEquals(lst.pop(0), ('hello', 'world'))
        self.assertEquals(lst, [])
