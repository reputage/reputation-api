# ================================================== #
#                       SETUP                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext

import sys
import io
import os
import re

try:
    import Cython
except ImportError:
    Cython = None

v = sys.version_info
if v < (3, 6):
    msg = "FAIL: Requires Python 3.6 or later, but setup.py was run using {}.{}.{}"
    print(msg.format(v.major, v.minor, v.micro))
    print("NOTE: Installation failed. Run setup.py using python3")
    sys.exit(1)

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

if 'TOXENV' in os.environ and 'SETUPPY_CFLAGS' in os.environ:
    os.environ['CFLAGS'] = os.environ['SETUPPY_CFLAGS']

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

class optional_build_ext(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except Exception as e:
            self._unavailable(e)
            self.extensions = []

    def _unavailable(self, e):
        print('*' * 80)
        print('''WARNING:
    An optional code optimization (C extension) could not be compiled.
    Optimizations for this package will not be available!
        ''')

        print('CAUSE:')
        print('')
        print('    ' + repr(e))
        print('*' * 80)


setup(
    name='reputation',
    version='0.1.0',
    license='Apache2',
    description='Xaltry Project Backend',
    long_description="Automated Reputation Service",
    author='Brady M Hammond',
    author_email='brady.hammond@consensys.com',
    url='https://github.com/BradyHammond/Reputation-API-2.0.git',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache2 License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    keywords=[
    ],
    install_requires=[
        'click', 'falcon>=1.2', 'ioflo>=1.6.8', 'libnacl>=1.5.1',
        'ujson>=1.35', 'pytest-falcon>=0.4.2', 'arrow>=0.10.0',
    ],
    extras_require={
    },
    setup_requires=[
        'cython',
    ] if Cython else [],
    entry_points={
        'console_scripts': [
            'reputation = reputation.cli:main',
            'reputationd = reputation.reputationd:main',
        ]
    },
    cmdclass={'build_ext': optional_build_ext},
    ext_modules=[
        Extension(
            splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
            sources=[path],
            include_dirs=[dirname(path)]
        )
        for root, _, _ in os.walk('src')
        for path in glob(join(root, '*.pyx' if Cython else '*.c'))
    ],
)

# ================================================== #
#                        EOF                         #
# ================================================== #