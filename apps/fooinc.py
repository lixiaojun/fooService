# -*- coding: utf-8 -*-
'''
Created on 2012-1-8

@author: qianmu.lxj
'''
import copy
import json
import web

def logged():
    if web.ctx.session.loggedin == True:
        return True
    else:
        return False
    
def notfound():
    res = FooResponse()
    return web.notfound(res.notfound())

def internalerror():
    res = FooResponse()
    return web.internalerror(res.error())

RET_JSON_FORMAT = {
                   'status':400,
                   'root':{}
                   }

class FooAuth:
    is_logged = False
    
    def __init__(self):
        self.is_logged = self.logged()
        
    def logged(self):
        if web.ctx.session.loggedin == True:
            return True
        else:
            return False

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
        self.ret =  copy.deepcopy(RET_JSON_FORMAT)
    
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
