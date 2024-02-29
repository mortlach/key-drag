# setup.py
from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules = [
    Extension("numerical_methods", sources=["numerical_methods.pyx"], language='c',
              extra_compile_args=['-Ofast', '-march=native'], include_dirs=[numpy.get_include()]),
    Extension("ngram_model", sources=["ngram_model.pyx"], language='c++',
              extra_compile_args=['-Ofast', '-march=native'])
]

setup(
    name="key_drag",
    ext_modules=cythonize(ext_modules,
                          compiler_directives={'language_level': "3"}
                          )

)
