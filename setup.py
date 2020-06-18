from setuptools import setup
import codecs
import os

def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
      # Basic information
      name='BioSim',
      version='0.1.0',

      # Packages to include
      packages=['biosim'],

      # Required packages not included in Python standard library
      requires=['pytest'],

      # Metadata
      description='A Simulation of Ecosystem of an island',
      long_description=read_readme(),
      author='Bishnu Poudel, NMBU',
      author_email='bishnu.poudel@nmbu.no',
      url='https://github.com/vsnupoudel/INF200_TA_Test',
      keywords='simulation ',
      license='MIT License',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Science :: Stochastic processes',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        ]
)