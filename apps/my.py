# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''

from apps.fooinc import FooResponse, notfound, internalerror, FooAuth, FooStatus
from libs.utils import Validation
from models.mygift import WishList, Product, ProductPrice
from sqlalchemy.sql.expression import or_
import json
import time
import web

urls = (
        "/wish/?", "MyWish",
        "/wish/follow/?", "MyWishAdd",
        "/wish/undo/?", "MyWishUndo",
        "/wish/buyed/?", "MyWishBuyed",
        "/wish/price/?", "MyWishExpectPrice",
        )

class MyResponse(FooResponse):
    
    def mywish_success(self, wishlist):
        ret = self._ret()
        ret['status'] = FooResponse.STATUS_CODE_SUCCESS
        count = len(wishlist)        
        ret['root']['count'] = count
        ret['root']['data'] = wishlist
        return json.dumps(ret)
    
    
    pass

class MyValidation(Validation):
    
    @staticmethod
    def check_pkey(pkey):
        ispass = False
        if Validation.isMd5(pkey):
            ispass = True
        return ispass
    
    @staticmethod
    def check_mywishadd(pkey):
        return MyValidation.check_pkey(pkey)
    
    @staticmethod
    def check_mywishexpectprice(price, pkey):
        ispass = False
        if Validation.isMd5(pkey) and Validation.isPrice(price):
            ispass = True
        return ispass
    
    @staticmethod
    def check_mywishundo(pkey):
        return MyValidation.check_pkey(pkey)

    @staticmethod
    def check_mywishbuyed(pkey):
        return MyValidation.check_pkey(pkey)          
class MyWishAdd(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
            
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            if not MyValidation.check_mywishadd(pkey):
                return self.dataerror()
            
            uid = self.uid
            gift = self._gift_exsit(uid, pkey)
            
            if not gift:
                new = WishList()
                new.user_id = uid
                new.product_pkey = pkey
                new.create_time = time.strftime('%Y-%m-%d %X', time.localtime())
                new.wlstatus = FooStatus.MY_WISH_STATUS_FOLLOW
                web.ctx.mygift.add(new)
                
                return self.success()
            else:
                if gift.wlstatus == FooStatus.MY_WISH_STATUS_DELETED:
                    gift.wlstatus = FooStatus.MY_WISH_STATUS_FOLLOW
                if web.ctx.mygift.is_modified(gift):
                    web.ctx.mygift.add(gift)
                    return self.success()
        else:
            return self.forbidden()
    
    def _gift_exsit(self, uid, pkey):
        flag = False
        query = web.ctx.mygift.query(WishList)
        gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid).first()
        if gift:
            flag = gift
        return flag

class MyWishExpectPrice(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            price = web.input().price
            pkey = web.input().pkey
            if not MyValidation.check_mywishexpectprice(price, pkey):
                return self.dataerror()
            
            uid = self.uid
            query = web.ctx.mygift.query(WishList)
            gift = query.filter(WishList.product_pkey == pkey).\
                filter(WishList.user_id == uid).filter(WishList.wlstatus == FooStatus.MY_WISH_STATUS_FOLLOW).first()
            mret = self.failed()
            if gift:
                gift.expect_price = price
                if web.ctx.mygift.is_modified(gift):
                    web.ctx.mygift.add(gift)
                    mret = self.success()
                else:
                    mret = self.notmodified()
            return mret
            
        else:
            return self.forbidden()
    
class MyWishUndo(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            if not MyValidation.check_mywishundo(pkey):
                return self.dataerror()
            
            uid = self.uid
            query = web.ctx.mygift.query(WishList)
            gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid).first()
            mret = self.failed()
            if gift is not None:
                gift.wlstatus = FooStatus.MY_WISH_STATUS_DELETED
                if web.ctx.mygift.is_modified(gift):
                    web.ctx.mygift.add(gift)
                    mret = self.success()
                else:
                    mret = self.notmodified()
            return mret
            
        else:
            return self.forbidden()

class MyWishBuyed(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            if not MyValidation.check_mywishbuyed(pkey):
                return self.dataerror()
            
            uid = self.uid
            query = web.ctx.mygift.query(WishList)
            gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid)\
                .filter(WishList.wlstatus == FooStatus.MY_WISH_STATUS_FOLLOW).first()
            mret = self.failed()
            if gift:
                gift.wlstatus = FooStatus.MY_WISH_STATUS_BUYED
                if web.ctx.mygift.is_modified(gift):
                    web.ctx.mygift.add(gift)
                    mret = self.success()
                else:
                    mret = self.notmodified()
            return mret
            
        else:
            return self.forbidden()
    
    def _get_buyed_val_byPkey(self, pkey):
            my_flag = FooStatus.MY_WISH_STATUS_BUYED
            query = web.ctx.mygift.query(ProductPrice)
            pPrice = query.filter(ProductPrice.product_pkey == pkey).order_by(ProductPrice.update_time.desc()).first()
            if pPrice:
                my_flag = pPrice.id
            return my_flag
                       
class MyWish(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
            
    def POST(self):
        if self.is_logged:
            uid = self.uid
            query = web.ctx.mygift.query(WishList)
            product_query = web.ctx.mygift.query(Product)
            wishlist = query.filter(WishList.user_id == uid).\
                filter(or_(WishList.wlstatus == FooStatus.MY_WISH_STATUS_FOLLOW, WishList.wlstatus == FooStatus.MY_WISH_STATUS_BUYED)).all()
            count = len(wishlist)
            for i in range(count):
                wishlist[i] = wishlist[i]._to_dict()
                pkey = wishlist[i]['product_pkey']
                product = product_query.filter(Product.pkey == pkey).first()
                wishlist[i] = dict(wishlist[i])
                wishlist[i].update(product._to_dict())
                del wishlist[i]['product_pkey']
            return self.mywish_success(wishlist)
        else:
            return self.forbidden()
        
app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
