#! /usr/bin/env python

import setuptools
import glob

import nm_chess_club

setuptools.setup(
    name='nm-chess-club',
    version=nm_chess_club.__version__,
    packages=setuptools.find_packages(),
    author='Daniel Abercrombie',
    author_email='daniel.r.abercrombie@gmail.com',
    url='https://github.com/dabercro/nm-chess-club',
    scripts=[s for s in glob.iglob('bin/*') if not s.endswith('~')],
    python_requires='>=3',
    )
