from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext_modules = [Extension("perceptron_opt",
                     ["perceptron_opt.pyx", "MurmurHash3.cpp"],
                     language='c++',
                     )]


setup(name="perceptron_opt",
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules)
