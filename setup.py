import os
import io
from setuptools import setup, find_packages

from codeorigins import VERSION


PATH_BASE = os.path.dirname(__file__)


def get_readme():
    # This will return README (including those with Unicode symbols).
    with io.open(os.path.join(PATH_BASE, 'README.rst')) as f:
        return f.read()


setup(
    name='codeorigins',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/codeorigins',

    description='Code origins contest based on GitHub data',
    long_description=get_readme(),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'requests',
        'click',
        'Jinja2',
    ],
    setup_requires=[],

    entry_points={
        'console_scripts': ['codeorigins = codeorigins.cli:main'],
    },

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License'
    ],
)


