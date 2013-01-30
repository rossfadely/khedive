from distutils.core import setup, Extension

extmod = Extension('_triweight_KDE_1D',
                   sources = ['_triweight_KDE_1D.c'])

setup (ext_modules = [extmod])
