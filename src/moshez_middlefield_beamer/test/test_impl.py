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
            with open(src, 'rb') as inp:
                tex = inp.read()
            lines = tex.decode('ascii').splitlines()
            for line in lines:
                if not line.strip().startswith('\lstinputlisting'):
                    continue
                file_name = os.path.join(cwd, line.split('{')[1].split('}')[0])
                if not os.path.exists(file_name):
                    raise ValueError("Cannot find", file_name)
            shutil.copy(src, dest)
            return
        raise NotImplementedError(_cmd, args, kwargs)


class ImplTest(unittest.TestCase):

    def test_beamer(self):
        executor = seashore.Executor(FakeShell())
        self.addCleanup(lambda: shutil.rmtree(build_dir))
        build_dir = tempfile.mkdtemp()
        output_dir = os.path.join(build_dir, 'build')
        self.addCleanup(lambda: shutil.rmtree(source_dir))
        source_dir = tempfile.mkdtemp()
        source_name = os.path.join(source_dir, 'talk.tex')
        code_name = os.path.join(source_dir, 'foo.py')
        with open(source_name, 'wb') as filep:
            filep.write(b'''this is like a source
                            \lstinputlisting{foo.py}
                         ''')
            filep.flush()
        with open(code_name, 'wb') as filep:
            filep.write(b'import this\n')
        _impl.beamer(dict(input=source_name,
                          outdir=output_dir),
                     dict(executor=executor))
        with open(os.path.join(output_dir, 'talk.pdf')) as filep:
            slides = filep.read().splitlines()
        with open(os.path.join(output_dir, 'handout.pdf')) as filep:
            handout = filep.read().splitlines()
        self.assertEquals(slides.pop(), 'this is like a source')
        self.assertEquals(handout.pop(), 'this is like a source')
        self.assertEquals(slides.pop(0).split('{')[-1][:-1], 'beamer')
        self.assertEquals(handout.pop(0).split('{')[-1][:-1], 'article')
