#! /usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''
from apps import my, user, search
from apps.fooinc import Log
from models.mygift import MygiftSession
from sqlalchemy.orm import scoped_session
import web

try:
    import conf
except ImportError:
    import default_conf as conf

urls = (
        "/?", "Index", 
        "/my", my.app,
        "/user", user.app,
        "/search", search.app,
        )

web.config.debug = conf.debug
#web.config.session_parameters['timeout'] = 86400
#web.config.session_parameters['ignore_expiry'] = True

app = web.application(urls, globals())
'''
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore(conf.sessions_path),\
                                   initializer = {'loggedin':False, 'uid':0})
    web.config._session = session

else:
    session = web.config._session
    
def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))
''' 

def hook_sql_con(handler):
    web.ctx.mygift = scoped_session(MygiftSession)
    try:
        return handler()
    except web.HTTPError:
        web.ctx.mygift.commit()
        raise
    except:
        web.ctx.mygift.rollback()
        raise
    finally:
        web.ctx.mygift.commit()

app.add_processor(hook_sql_con)

class Index:
    def GET(self):
        return "Welcome to web.py"
    
if __name__ == "__main__" :
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
    
