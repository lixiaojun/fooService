#! /usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''

import fooservice as fooservice_
from apps.fooinc import Log


if __name__ == '__main__':
    
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run(Log)
