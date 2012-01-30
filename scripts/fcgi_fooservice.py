#! /usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''

from apps.fooinc import Log
import fooservice as fooservice_
import web

if __name__ == '__main__':
    
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    fooservice_.app.run(Log)
