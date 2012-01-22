# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''
from apps import my, user, search
import web
urls = (
        "/?", "Index", 
        "/my", my.app,
        "/user", user.app,
        "/search", search.app,
        )

web.config.session_parameters['ignore_expiry'] = True

app = web.application(urls, globals())


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),\
                                   initializer = {'loggedin':False, 'uid':0})
    web.config._session = session
else:
    session = web.config._session

class Index:
    def GET(self):
        return "Welcome to web.py"
    
def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))
    
if __name__ == "__main__" :
    
    app.run()
    