from setuptools import setup
from Cython.Build import cythonize

setup(
    name='TarjemVid-AI',
    ext_modules=cythonize("main.py", compiler_directives={'binding': False}),
    zip_safe=False,
)