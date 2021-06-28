from distutils.core import setup, Extension

module = Extension("fibonacciModule", sources=["fibonacci_module.c"])

setup(
    name='fibonacciModule',
    version='1.0',
    description='',
    ext_modules=[module]
)
