# -*- coding: utf-8 -*-
'''
Created on 2012-1-30

@author: qianmu.lxj
'''
import os

debug = True

# path
PWD = os.path.dirname(os.path.realpath(__file__))

sessions_path = os.path.join(PWD, '../data/sessions')
log_path = os.path.join(PWD, '../logs')

#log
log_file = log_path+'/wsgi.log'
log_interval = 'h'
log_backups = 1

#cookies
COOKIE_AUTH_KEY_ARC4 = 'YNDtvGbzRCKzEOoPKDTwo3ZTzVYX'
COOKIE_AUTH_NAME = 'CYE_SESSIONID'
COOKIE_AUTH_MAX_TIME = 24*60*60*90