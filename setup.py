from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='oracle_db_tools',
    version='1.1.0',
    description='Tools for working with an Oracle database from Pandas',
    long_description=long_description,
    url='https://github.com/cwade/oracle_db_tools',
    author='cwade',
    author_email='pysurveyhelper@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='oracle sql query insert insert_multiple pandas dataframe',
    packages=['oracle_db_tools'],
    install_requires=['pandas', 'cx_Oracle', 'pyaml'],
    package_data={
        'config_sample': ['config_sample.yml'],
    },
)
