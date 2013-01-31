from distutils.core import setup, Extension

extmod = Extension('_khedive',
                   sources = ['_khedive.c'])

setup (ext_modules = [extmod])
