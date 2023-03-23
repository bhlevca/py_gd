#!/usr/bin/env python

"""
setup.py script for the py_gd package

Tested with:
  conda (with conda-forge libgd) on OS_X

On Windows, MacOS and Linux (CentoOS 7)

libgd is assumed to be installed (and its dependencies) already.
The conda package on conda-forge is a good way to get it:

https://anaconda.org/conda-forge/libgd

"""

import sys
import os
import glob
import shutil

from setuptools import setup, Extension
from distutils.command.clean import clean

from Cython.Build import cythonize

import numpy  # for the include dirs...

# could run setup from anywhere
SETUP_PATH = os.path.dirname(os.path.abspath(__file__))

include_dirs = [numpy.get_include()]
library_dirs = []
libraries = ['gd']
compile_args = []
link_args = []

if sys.platform.startswith('win'):
    # need the library and include for Windows Anaconda... <PREFIX>/Library
    include_dirs.append(os.path.join(sys.prefix, r'Library\include'))
    # dlls go in bin, rather than lib (??)
    library_dirs.append(os.path.join(sys.prefix, r'Library\lib'))

    compile_args.append('-EHsc')
    link_args.append('/MANIFEST')
elif sys.platform.startswith('linux'):
    library_dirs.append('/usr/local/lib')
    include_dirs.append('/usr/local/include')

# crazy kludge to find include dir in a conda build:
# check if we are running conda build:
if 'CONDA_BUILD' in os.environ:
    print("running in conda build, adding include dir")
    prefix = os.environ['PREFIX']
    include_dirs.append(os.path.join(prefix, 'include'))
    print("added:", include_dirs[-1])
else:
    print("not running in conda build")


class cleanall(clean):
    description = ("cleans files generated by 'develop' mode and files "
                   "autogenerated by cython")

    def run(self):
        # call base class clean
        clean.run(self)

        # clean remaining cython/cpp files
        t_path = [os.path.join(SETUP_PATH, 'py_gd')]
        exts = ['*.so', 'cy_*.pyd', 'cy_*.cpp', 'cy_*.c']

        for temp in t_path:
            for ext in exts:
                for f in glob.glob(os.path.join(temp, ext)):
                    print("Deleting auto-generated file: {0}".format(f))
                    try:
                        if os.path.isdir(f):
                            shutil.rmtree(f)
                        else:
                            os.remove(f)
                    except OSError as err:
                        print("Failed to remove {0}. Error: {1}"
                              .format(f, err))
                        # raise

        rm_dir = ['py_gd.egg-info', 'build']
        for dir_ in rm_dir:
            print("Deleting auto-generated directory: {0}".format(dir_))
            try:
                shutil.rmtree(dir_)
            except OSError as err:
                if err.errno != 2:  # ignore the not-found error
                    raise


# This setup requires libgd and its dependent libs
# It expects to find them in the "usual" locations
#   or where conda puts it...

ext_modules = [Extension("py_gd.py_gd",
                         ["py_gd/py_gd.pyx"],
                         include_dirs=include_dirs,
                         library_dirs=library_dirs,
                         libraries=libraries,
                         extra_compile_args=compile_args,
                         extra_link_args=link_args,
                         )]

ext_modules = cythonize(
                  ext_modules,
                  compiler_directives={'language_level': 3})

# def get_version():
#     """
#     get version from __init__.py
#     """
#     with open(os.path.join("py_gd", "__init__.py")) as initfile:
#         for line in initfile:
#             line = line.strip()
#             if line.startswith("__version__"):
#                 version = line.split("=")[1].strip(' "')
#                 return version


setup(# name="py_gd",
      # version=get_version(),
      # description="python wrappers around libgd graphics lib",
      # long_description=read('README'),
      # author="Christopher H. Barker",
      # author_email="chris.barker@noaa.gov",
      # url="https://github.com/NOAA-ORR-ERD/py_gd",
      #license="Public Domain",
      #keywords="graphics cython drawing",
      cmdclass={'cleanall': cleanall},
      ext_modules=cythonize(ext_modules),
      # zip_safe=False,  # dont want a compiled extension in a zipfile...
      #packages=['py_gd', 'py_gd.test'],
      #python_requires='>=3.8',
      # classifiers=["Development Status :: 2 - Pre-Alpha",
      #              "Topic :: Utilities",
      #              "License :: Public Domain",
      #              "Intended Audience :: Developers",
      #              "Operating System :: OS Independent",
      #              "Programming Language :: Cython",
      #              "Programming Language :: Python :: 3 :: Only",
      #              "Programming Language :: Python :: Implementation :: CPython",
      #              "Topic :: Multimedia :: Graphics",
      #              ],
      )
