from os import path

from setuptools import setup

REQUIREMENTS = ['pytest', 'six']

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'rb') as f:
    long_description = f.read().decode('utf8')

setup(
    name='pytest-parametrization',
    version='2022.2.1',
    py_modules=['parametrization'],
    provides=['parametrization'],
    description='Simpler PyTest parametrization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Singular Labs, Inc",
    author_email='devs@singular.net',
    url='https://github.com/singular-labs/parametrization',
    keywords="pytest, parametrize, parametrization, singular",
    install_requires=REQUIREMENTS,
    license="MIT License",
    python_requires='>=3.7',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
