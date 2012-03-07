'''
Created on 2012-2-26

@author: lixiaojun
'''
import redis
import threading

try:
    import conf
except ImportError:
    import default_conf as conf

REDIS_HOST = conf.REDISDB_CONF['host']
REDIS_PORT = conf.REDISDB_CONF['port']
REDIS_DB = conf.REDISDB_CONF['db']
REDIS_PWD = conf.REDISDB_CONF['passwd']

class CyeRedis(object):
    
    __inst = None
    __lock = threading.Lock()
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PWD)

    @staticmethod
    def getInstance():
        CyeRedis.__lock.acquire()
        if not CyeRedis.__inst:
            CyeRedis.__inst = CyeRedis()
        CyeRedis.__lock.release()
        return CyeRedis.__inst.redis_conn
    
redis_cli = CyeRedis.getInstance()
