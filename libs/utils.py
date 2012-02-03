# -*- coding: utf-8 -*-
'''
Created on 2012-2-4

@author: qianmu.lxj
'''
from Crypto.Cipher import ARC4
import base64
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
