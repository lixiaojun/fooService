# -*- coding: utf-8 -*-
'''
Created on 2012-1-7

@author: qianmu.lxj
'''
from apps.fooinc import FooResponse, notfound, internalerror, FooAuth
from libs.utils import encryptor
from models.mygift import mygift, User, NOW
import copy
import hashlib
import json
import web

try:
    import conf
except ImportError:
    import default_conf as conf

USER_PRIVILEGE_ADMIN = 0
USER_PRIVILEGE_MEMBER = 1
USER_PRIVILEGE_VIP = 2

COOKIE_FORMAT = {'uid':-1, 'login_time':''}
cookie_auth_time = conf.COOKIE_AUTH_MAX_TIME
cookie_auth_name = conf.COOKIE_AUTH_NAME

urls = (
        '/?', 'UserIndex',
        '/login/?', 'Login',
        '/logout', 'Logout',
        '/register', 'Register',
        )

def revocation():
    auth = copy.deepcopy(COOKIE_FORMAT)
    auth = encryptor.arc4_encode(json.dumps(auth))
    web.setcookie(cookie_auth_name, auth, expires=-7, httponly=True, path='/')
    
def accredit(user):
    if user is not None and user.id > 0:
        auth = copy.deepcopy(COOKIE_FORMAT)
        auth['uid'] = user.id
        auth['login_time'] = NOW
        auth = encryptor.arc4_encode(json.dumps(auth))
        print auth
        if auth:
            web.setcookie(cookie_auth_name, auth, expires=cookie_auth_time, httponly=True, path='/')

class UserIndex:
    def GET(self):
        render = web.template.render('templates')
        return render.test()

class UserResponse(FooResponse):
    
    def login_success(self, user):
        return self._login_success2json(user)
    
    def logout_success(self):
        return self.success()
    
    def register_success(self, user):
        return self._register_success2json(user)
    
    def register_failed(self, code=FooResponse.STATUS_CODE_FAILED):
        return self._register_failed2json(code)
    
    def _login_success2json(self,user):
        ret = self.ret
        if user is not None:
            ret['status'] = FooResponse.STATUS_CODE_SUCCESS
            ret['root']['uID'] = user.id
            ret['root']['nickName'] = user.nickname
            ret['root']['email'] = user.email
            ret['root']['status'] = user.status
            ret['root']['message'] = 'Request succeeded'
        return json.dumps(ret)
    
    def _register_success2json(self, user):
        ret = self.ret
        ret['status'] = FooResponse.STATUS_CODE_SUCCESS
        ret['root']['uID'] = user.id
        ret['root']['status'] = user.status
        ret['root']['message'] = 'Request succeeded'
        return json.dumps(ret)
    
    def _register_failed2json(self, code):
        ret = self.ret
        ret['status'] = code
        if code is FooResponse.STATUS_CODE_CONFLICT:
            ret['root']['message'] = 'User Already Exist.'
        else:
            ret['root']['message'] = 'Error message.'
        return json.dumps(ret)

render = web.template.render('templates/user')

class Login(UserResponse, FooAuth):
    def __init__(self):
        UserResponse.__init__(self)
        FooAuth.__init__(self)
    
    def GET(self):
        if not self.logged():
            return render.login()
        else:
            uid = self.uid
            query = mygift.query(User)
            userInfo = query.filter(User.id == uid).first()
            return render.home(userInfo)
    
    def POST(self):
        email, password = web.input().email, web.input().password
        try:
            query = mygift.query(User)
            user = query.filter(User.email == email).first()
            ret = self.forbidden()
            if user is not None:
                passwd = hashlib.md5(password).hexdigest()
                if(passwd == user.password):
                    ret = self.login_success(user)
                    accredit(user)
                else:
                    revocation()
            else:
                revocation()
        except:
            revocation()
            ret = self.error()
        return ret
     
    
class Logout(UserResponse):
    def __init__(self):
        UserResponse.__init__(self)
    
    def GET(self):
        revocation()
        return self.logout_success()
        
    
class Register(UserResponse, FooAuth):
    def __init__(self):
        UserResponse.__init__(self)
        FooAuth.__init__(self)
    
    def GET(self):
        return render.register()

    def POST(self):
        email, passwd, repasswd = web.input().email, web.input().password, web.input().repassword
        ret = self.register_failed()
        try:
            if passwd == repasswd:
                user_exsit = self._findUserByEmail(email)
                if not user_exsit:
                    new = User()
                    new.email = email
                    new.password = hashlib.md5(passwd).hexdigest()
                    new.register_time = NOW
                    new.register_ip = web.ctx.ip
                    mygift.add(new)
                    
                    query = mygift.query(User)
                    user = query.filter(User.email == email).first()
                    
                    #mygift.commit()
                    ret = self.register_success(user)
                    accredit(user)
                else:
                    ret = self.register_failed(FooResponse.STATUS_CODE_CONFLICT)
        except:
            ret = self.error()
        return ret
            
        
    def _findUserByEmail(self, email):
        flag = False
        if email is not None:
            query = mygift.query(User)
            user = query.filter(User.email == email).first()
            if user:
                flag = True   
        return flag
    
app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
