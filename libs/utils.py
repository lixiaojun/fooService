# -*- coding: utf-8 -*-
'''
Created on 2012-2-4

@author: qianmu.lxj
'''
from Crypto.Cipher import ARC4
import base64
import re
import string
import types
try:
    import conf
except ImportError:
    import default_conf as conf
    
COOKIE_AUTH_KEY_ARC4 = conf.COOKIE_AUTH_KEY_ARC4
if COOKIE_AUTH_KEY_ARC4 is None:
    COOKIE_AUTH_KEY_ARC4 = 'YNDtvGbzRCKzEOoPKDTwo3ZTzVYX'

class encryptor:
    
    @staticmethod
    def arc4_encode(text, key=COOKIE_AUTH_KEY_ARC4):
        if text is not None and len(text) > 0:
            encryptor = ARC4.new(key)
            ciphertext = encryptor.encrypt(text)
            ciphertext = base64.encodestring( ciphertext )
        else:
            ciphertext = False
        return ciphertext
    
    @staticmethod
    def arc4_decode(ciphertext, key=COOKIE_AUTH_KEY_ARC4):
        try:
            ciphertext = base64.decodestring(ciphertext)
            decryptor = ARC4.new(key)
            plain = decryptor.decrypt(ciphertext)
        except:
            plain = False
        return plain
    
def u_(varobj):
    if isinstance(varobj, str):
        try:
            varobj = varobj.decode('utf-8')
        except:
            varobj = varobj.decode('gbk')
    return varobj    
    
class Validation:
    @staticmethod
    def isName(varobj):
        flag = False
        if Validation.isString(varobj):
            rule = ur"^[a-zA-Z0-9\u4e00-\u9fa5]+$"
            varobj = u_(varobj)
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @staticmethod
    def isMd5(varobj):
        flag = False
        if Validation.isString(varobj):
            rule = '^[a-z0-9A-Z]{32}$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @staticmethod
    def isIntId(varobj):
        flag = False
        if Validation.isString(varobj):
            rule = '^[1-9][0-9]*$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @staticmethod
    def isChs(varobj):
        flag = False
        if Validation.isString(varobj):
            rule = ur'^[\u4e00-\u9fa5]+$'
            varobj = u_(varobj)
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @staticmethod
    def isString(varobj):
        return isinstance(varobj, str) or Validation.isUnicode(varobj)
    
    @staticmethod
    def isEmail(varobj):
        flag = False
        if Validation.isUnicode(varobj):
            rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @staticmethod
    def isUnicode(varobj):
        flag = False
        if isinstance(varobj, unicode):
            flag = True
        return flag
    
    @staticmethod
    def isEmpty(varobj):
        flag = False
        if type(varobj) is types.NoneType or len(varobj) == 0:
            flag = True
        return flag
    
    @staticmethod
    def isPrice(varobj):
        flag = False
        if Validation.isUnicode(varobj) or Validation.isString(varobj):
            rule = '\.'
            price = ''
            match = re.search(rule, varobj)
            try:
                if match:
                    price = string.atof(varobj)
                else:
                    price = string.atoi(varobj)
            except ValueError:
                pass
            else:
                if price > 0:
                    flag = True
        return flag
    
    @staticmethod
    def isInjection(varobj):
        flag = False
        if Validation.isString(varobj) and not Validation.isEmpty(varobj):
            flag = Validation.check_sql_injection(varobj)
        return flag
        
    @staticmethod
    def check_sql_injection(varobj):
        injection = False
        if not Validation.isEmpty(varobj):
            varobj = string.lower(varobj)
            rules = [
                    'select [^ ]+ from ', 'update [^ ]+ set ', 'delete [^ ]+ from ', ' union all select ', ' union select ', ' limit ', 'create database ', 'create table ',
                    'drop database ', 'drop table ', 'insert into ', 'alter table ', 'exec ', '\w*\(\)', 'is_srvrolemember ', 'is_member ', ' or ', ' and ', 
                    ]
            varobj_len = len(varobj)
            for rule in rules:
                if len(rule) <= varobj_len:
                    match = re.search(rule, varobj)
                    if match:
                        injection = True
                        break
        return injection
    

    
            