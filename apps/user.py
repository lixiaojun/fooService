# -*- coding: utf-8 -*-
'''
Created on 2012-1-7

@author: qianmu.lxj
'''
from apps.fooinc import FooResponse, notfound, internalerror, FooAuth, FooStatus
from libs.utils import encryptor, Validation
from models.mygift import User
import copy
import hashlib
import json
import time
import web

try:
    import conf
except ImportError:
    import default_conf as conf

COOKIE_FORMAT = {'uid':-1, 'login_time':''}
cookie_auth_time = conf.COOKIE_AUTH_MAX_TIME
cookie_auth_name = conf.COOKIE_AUTH_NAME

urls = (
        '/?', 'UserIndex',
        '/login/?', 'Login',
        '/logout', 'Logout',
        '/register', 'Register',
        '/nickname/?', 'Nickname',
        '/setpasswd/?', 'SetPassword',
        
        )

render = web.template.render('templates/user')

def revocation():
    auth = {'uid':-1, 'login_time':''}
    auth = encryptor.arc4_encode(json.dumps(auth))
    web.setcookie(cookie_auth_name, auth, expires=-7, httponly=True, path='/')
    
def accredit(user):
    if user is not None and user.id > 0:
        auth = {'uid':-1, 'login_time':''}
        auth['uid'] = user.id
        auth['login_time'] = time.strftime('%Y-%m-%d %X', time.localtime())
        auth = encryptor.arc4_encode(json.dumps(auth))
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
        ret = self._ret()
        if user is not None:
            ret['status'] = FooResponse.STATUS_CODE_SUCCESS
            ret['root']['uID'] = user.id
            ret['root']['nickName'] = user.nickname
            ret['root']['email'] = user.email
            ret['root']['ustatus'] = user.ustatus
            ret['root']['message'] = 'Request succeeded'
        return json.dumps(ret)
    
    def _register_success2json(self, user):
        ret = self._ret()
        ret['status'] = FooResponse.STATUS_CODE_SUCCESS
        ret['root']['uID'] = user.id
        ret['root']['ustatus'] = user.ustatus
        ret['root']['message'] = 'Request succeeded'
        return json.dumps(ret)
    
    def _register_failed2json(self, code):
        ret = self._ret()
        ret['status'] = code
        if code is FooResponse.STATUS_CODE_CONFLICT:
            ret['root']['message'] = 'User Already Exist.'
        else:
            ret['root']['message'] = 'Error message.'
        return json.dumps(ret)

class UserValidation(Validation):
    @classmethod
    def check_login(cls, email, password):
        ispass = False
        print email
        print type(email)
        print cls.isString(email)
        print cls.isEmail(email)
        print cls.isEmpty(password)
        if cls.isEmail(email) and not cls.isEmpty(password):
            ispass = True
        return ispass
    
    @classmethod
    def check_register(cls, email, passwd, repasswd):
        ispass = False
        if cls.isEmail(email) and not cls.isEmpty(passwd) \
            and not cls.isEmpty(repasswd):
            if passwd == repasswd:
                ispass = True
        return ispass
    
    @classmethod
    def check_nickname(cls, nickname):
        ispass = False
        if cls.isName(nickname):
            ispass = True
        return ispass
    
    @classmethod
    def check_setpassword(cls, passwd, newpasswd, rnewpasswd):
        ispass = False
        if cls.isString(passwd) and cls.isString(newpasswd) and Validation.isString(rnewpasswd):
            if newpasswd == rnewpasswd:
                ispass = True
        return ispass

class Login(UserResponse, FooAuth):
    def __init__(self):
        UserResponse.__init__(self)
        FooAuth.__init__(self)
    
    def GET(self):
        if not self.logged():
            return render.login()
        else:
            uid = self.uid
            query = web.ctx.mygift.query(User)
            userInfo = query.filter(User.id == uid).first()
            return render.home(userInfo)
    
    def POST(self):
        email, password = web.input().email, web.input().password
        if not UserValidation.check_login(email, password):
            return self.dataerror()
        try:
            query = web.ctx.mygift.query(User)
            user = query.filter(User.email == email).filter(User.ustatus == FooStatus.USER_STATUS_ACTIVE).first()
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
            raise
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
        if not UserValidation.check_register(email, passwd, repasswd):
            return self.dataerror()
        
        ret = self.register_failed()
        try:
            if passwd == repasswd:
                user_exsit = self._findUserByEmail(email)
                if not user_exsit:
                    new = User()
                    new.email = email
                    new.password = hashlib.md5(passwd).hexdigest()
                    new.register_time = time.strftime('%Y-%m-%d %X', time.localtime())
                    new.register_ip = web.ctx.ip
                    web.ctx.mygift.add(new)
                    
                    query = web.ctx.mygift.query(User)
                    user = query.filter(User.email == email).first()
                    
                    #mygift.commit()
                    ret = self.register_success(user)
                    accredit(user)
                else:
                    ret = self.register_failed(FooResponse.STATUS_CODE_CONFLICT)
        except:
            ret = self.error()
            raise
        return ret
            
        
    def _findUserByEmail(self, email):
        flag = False
        if email is not None:
            query = web.ctx.mygift.query(User)
            user = query.filter(User.email == email).first()
            if user:
                flag = True   
        return flag
    
class Nickname(UserResponse, FooAuth):
    def __init__(self):
        UserResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            nickname = web.input().nickname
            if not UserValidation.check_nickname(nickname):
                return self.dataerror()
            
            uid = self.uid
            user = self._getUserById(uid)
            uret = self.failed()
            if user:
                user.nickname = nickname
                if web.ctx.mygift.is_modified(user):
                    web.ctx.mygift.add(user)
                    uret = self.success()
                else:
                    uret = self.notmodified()
            return uret
        
        else:
            return self.forbidden()
    
    def _getUserById(self, uid):
        user = False
        if uid:
            query = web.ctx.mygift.query(User)
            row = query.filter(User.id == uid).first()
            if row:
                user = row
        return user
    
class SetPassword(UserResponse, FooAuth):
    def __init__(self):
        UserResponse.__init__(self)
        FooAuth.__init__(self)
        
    def POST(self):
        if self.is_logged:
            passwd, newpasswd, rnewpasswd = web.input().password, web.input().newpassword, web.input().rnewpassword
            if not UserValidation.check_setpassword(passwd, newpasswd, rnewpasswd):
                return self.dataerror()
            uid = self.uid
            user = self._getUserById(uid)
            uret = self.failed()
            if user:
                if user.password != hashlib.md5(passwd):
                    uret = self.forbidden()
                else:
                    newpasswd = hashlib.md5(newpasswd)
                    user.password = newpasswd
                    if web.ctx.mygift.is_modified(user):
                        web.ctx.mygift.add(user)
                        uret = self.success()
                    else:
                        uret = self.notmodified()
            return uret
        else:
            return self.forbidden()
        
    def _getUserById(self, uid):
        user = False
        if uid:
            query = web.ctx.mygift.query(User)
            row = query.filter(User.id == uid).first()
            if row:
                user = row
        return user
    
app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
