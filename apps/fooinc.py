# -*- coding: utf-8 -*-
'''
Created on 2012-1-8

@author: qianmu.lxj
'''
from libs.utils import encryptor
from wsgilog import WsgiLog, LogStdout
import copy
import json
import logging
import os
import sys
import web

RET_JSON_FORMAT = {
                   'status':400,
                   'root':{}
                   }
  
def notfound():
    res = FooResponse()
    return web.notfound(res.notfound())

def internalerror():
    res = FooResponse()
    return web.internalerror(res.error())

try:
    import conf
except ImportError:
    import default_conf as conf

cookie_auth_name = conf.COOKIE_AUTH_NAME

class FooAuth:
    is_logged = False
    
    def __init__(self):
        self._load_cookie()
        
    def logged(self):
        return self.is_logged
    
    def _load_cookie(self):
        cookie = web.cookies().get(cookie_auth_name)
        self.cookie = cookie
        if cookie is not None:
            dec = encryptor.arc4_decode(cookie)
            if dec != False:
                dec = json.loads(dec)
                self.auth = dec
                self.uid = self.auth['uid']
                self.login_time = self.auth['login_time']
                self.is_logged = True if self.uid > 0 else False
            else:
                self.auth = None
                self.uid = None
                self.login_time = None
        

class FooResponse:
    '''
    200:Request success
    403:Permission denied
    404:Not found
    400:Request Failed, eg, Post data is error
    409:Request conflict; eg, Add data and data is exsit.
    500:Server internal error. 
    '''
    STATUS_CODE_SUCCESS = 200
    STATUS_CODE_FAILED = 400
    STATUS_CODE_FORBIDDEN = 403
    STATUS_CODE_NOTFOUND = 404
    STATUS_CODE_CONFLICT = 409
    STATUS_CODE_ERROR = 500
    
    def __init__(self):
        self.ret =  {'status':400,'root':{}}
    
    def success(self):
        return self._success2json()
    
    def _success2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_SUCCESS
        ret['root']['message'] = 'Request succeeded'
        return json.dumps(ret)
    
    def forbidden(self):
        return self._forbidden2json()
        
    def _forbidden2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_FORBIDDEN
        ret['root']['message'] = 'Permission denied'
        return json.dumps(ret)
    
    def error(self):
        return self._error2json()
    
    def _error2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_ERROR
        ret['root']['message'] = 'Server internal error.'
        return json.dumps(ret)
    
    def failed(self):
        return self._failed2json()
    
    def _failed2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_FAILED
        ret['root']['message'] = 'Request Failed.'
        return json.dumps(ret)
        
    def notfound(self):
        return self._notfound2json()
    
    def _notfound2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_NOTFOUND
        ret['root']['message'] = 'Not found.'
        return json.dumps(ret)
    
    def conflict(self):
        return self._conflict2json()
    
    def _conflict2json(self):
        ret = self.ret
        ret['status'] = self.STATUS_CODE_CONFLICT
        ret['root']['message'] = 'Data Already Exist.'
        return json.dumps(ret)

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = '%(message)s',
            tofile = True,
            file = conf.log_file,
            interval = conf.log_interval,
            backups = conf.log_backups
            )
        
        sys.stdout = LogStdout(self.logger, logging.INFO)
        sys.stderr = LogStdout(self.logger, logging.ERROR)