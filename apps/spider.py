'''
Created on 2012-2-26

@author: lixiaojun
'''
from apps.fooinc import FooResponse, FooAuth
from libs.utils import Validation
from models.nosql import redis_cli
import re
import string
import web
try:
    import conf
except ImportError:
    import default_conf as conf

urls = (
        "/update/lite", "SpiderUpdateLite",
        )

class SpiderResponse(FooResponse):
    
    pass

class SpiderValidation(Validation):
    @classmethod
    def check_update_lite(cls,url, score):
        ispass = False
        if cls.isUrl(url):
            ispass = True
        return ispass
    
    @classmethod
    def isJingdongProduct(cls, varobj):
        flag = False
        if cls.isString(varobj):
            rule = r'http://www.360buy\.com/product/\d+\.[a-zA-Z]+'
            match = re.match(rule, varobj)
            if match:
                flag = True
        return flag


class SpiderUpdateLite(SpiderResponse, FooAuth):
    def __init__(self):
        SpiderResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            url = web.input().url
            score = web.input().score
            score = 0
            if score is not None:
                rule = '\.'
                match = re.search(rule, score)
                try:
                    if match:
                        score = string.atof(score)
                    else:
                        score = string.atoi(score)
                except ValueError:               
                    pass
            if not SpiderValidation.check_update_lite(url, score):
                return self.dataerror()
            
            if self._push_url(url, score):
                return self.success()
            else:
                return self.failed()
            pass
        else:
            return self.forbidden()
        
    def _push_url(self, url, score=0):
        ret = False
        if SpiderValidation.isJingdongProduct(url):
            namespace = 'jingdong'
            update_urls_key = conf.REDIS_UPDATE_URLS_KEY % namespace
            print update_urls_key
            if redis_cli.zadd(update_urls_key, url, score):
                ret = True
        return ret
    