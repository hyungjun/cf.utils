#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'cf.util',
       version              = '0.5',
       description          = 'util sub module of coreFrame',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       url                  = '',
       package_dir          = {'cf.utils':'./'},
       packages             = ['cf.utils','cf.utils.table'],
#       install_requires     = ['numpy'],
      )
