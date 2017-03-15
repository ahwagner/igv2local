#!/usr/bin/env python

from distutils.core import setup

import sys
if sys.version_info < (3, 6):
    sys.exit("This package requires Python v3.6 or higher.")

setup(name='igv2local',
      version='0.2.2',
      description='IGV session remote host to local file organizer',
      author='Alex Wagner',
      url='https://github.com/ahwagner/igv2local',
      author_email='awagner24@wustl.edu',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='igv local copy',
      packages=['igv2local'],
      install_requires=['gmstk'],
      entry_points={
          'console_scripts': ['igv2local=igv2local.igv2local:main']
      },
      dependency_links=[
          'https://github.com/ahwagner/gmstk/tarball/master#egg=gmstk-0.2'
          ]
      )
