from __future__ import print_function

import os
import unittest
import shutil
import tempfile

import seashore

from moshez_middlefield_beamer import _impl

class FakeShell(object):

    def clone(self):
        return self

    def batch(self, _cmd, *args, **kwargs):
        if _cmd[0] == 'pdflatex':
            cwd = kwargs['cwd']
            src = os.path.join(cwd, _cmd[1])
            dest = os.path.splitext(src)[0] + '.pdf'
            shutil.copy(src, dest)
            return
        raise NotImplementedError(_cmd, args, kwargs)

class ImplTest(unittest.TestCase):

    def test_beamer(self):
        executor = seashore.Executor(FakeShell())
        self.addCleanup(lambda: shutil.rmtree(self.build_dir))
        self.build_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.build_dir, 'build')
        with tempfile.NamedTemporaryFile() as filep:
            filep.write(b'this is like a source\n')
            filep.flush()
            _impl.beamer(dict(input=filep.name,
                              outdir=self.output_dir),
                         dict(executor=executor))
        with open(os.path.join(self.output_dir, 'talk.pdf')) as filep:
            slides = filep.read().splitlines()
        with open(os.path.join(self.output_dir, 'handout.pdf')) as filep:
            handout = filep.read().splitlines()
        self.assertEquals(slides.pop(), 'this is like a source')
        self.assertEquals(handout.pop(), 'this is like a source')
        self.assertEquals(slides.pop(0).split('{')[-1][:-1], 'beamer')
        self.assertEquals(handout.pop(0).split('{')[-1][:-1], 'article')
