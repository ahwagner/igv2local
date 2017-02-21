#!/usr/bin/env python

from distutils.core import setup

import sys
if sys.version_info[0] < (3,6):
    sys.exit("This package requires Python v3.6 or higher.")

setup(name='igv2local',
      version='0.1',
      description='IGV session remote host to local file organizer',
      author='Alex Wagner',
      author_email='awagner24@wustl.edu',
      py_modules=['igv2local'],
      requires=['gmstk']
)
