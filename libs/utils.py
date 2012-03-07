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
    
    @classmethod
    def arc4_encode(cls, text, key=COOKIE_AUTH_KEY_ARC4):
        if text is not None and len(text) > 0:
            encryptor = ARC4.new(key)
            ciphertext = encryptor.encrypt(text)
            ciphertext = base64.encodestring( ciphertext )
        else:
            ciphertext = False
        return ciphertext
    
    @classmethod
    def arc4_decode(cls, ciphertext, key=COOKIE_AUTH_KEY_ARC4):
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
    @classmethod
    def isName(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = ur"^[a-zA-Z0-9\u4e00-\u9fa5]+$"
            varobj = u_(varobj)
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isMd5(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = '^[a-z0-9A-Z]{32}$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isIntId(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = '^[1-9][0-9]*$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isChs(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = ur'^[\u4e00-\u9fa5]+$'
            varobj = u_(varobj)
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isString(cls, varobj):
        return isinstance(varobj, str) or cls.isUnicode(varobj)
    
    @classmethod
    def isEmail(cls, varobj):
        flag = False
        if cls.isUnicode(varobj):
            rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isUnicode(cls, varobj):
        flag = False
        if isinstance(varobj, unicode):
            flag = True
        return flag
    
    @classmethod
    def isEmpty(cls, varobj):
        flag = False
        if type(varobj) is types.NoneType or len(varobj) == 0:
            flag = True
        return flag
    
    @classmethod
    def isUrl(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = '[a-zA-z]+://[^\s]*'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag
    
    @classmethod
    def isPrice(cls, varobj):
        flag = False
        if cls.isUnicode(varobj) or cls.isString(varobj):
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
    
    @classmethod
    def isInjection(cls, varobj):
        flag = False
        if cls.isString(varobj) and not cls.isEmpty(varobj):
            flag = cls.check_sql_injection(varobj)
        return flag
        
    @classmethod
    def check_sql_injection(cls, varobj):
        injection = False
        if not cls.isEmpty(varobj):
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
    

    
            