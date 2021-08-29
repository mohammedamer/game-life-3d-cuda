from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension("pyevolve",
              sources=["pyevolve.pyx"],
              include_dirs=['.'],
              library_dirs=['.'],
              runtime_library_dirs=['.'],
              libraries=["evolve"]
              )
]

setup(name="PyEvolve",
      ext_modules=cythonize(ext_modules))