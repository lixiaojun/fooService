# -*- coding: utf-8 -*-
'''
Created on 2012-1-6

@author: qianmu.lxj
'''

from apps.fooinc import FooResponse, notfound, internalerror, FooAuth
from models.mygift import WishList, NOW, mygift, Product
import json
import web

urls = (
        "/wish/?", "MyWish",
        "/wish/follow", "MyWishAdd",
        "/wish/undo", "MyWishUndo",
        "/wish/buyed", "MyWishBuyed",
        "/wish/again", "MyWishAgain",
        )

MY_WISH_STATUS_FOLLOW = 'follow'
MY_WISH_STATUS_DELETED = 'deleted'
MY_WISH_STATUS_BUYED = 'buyed'



class MyResponse(FooResponse):
    
    def mywish_success(self, wishlist):
        ret = self.ret
        ret['status'] = FooResponse.STATUS_CODE_SUCCESS
        count = len(wishlist)        
        ret['root']['count'] = count
        ret['root']['data'] = wishlist
        return json.dumps(ret)
    
    
    pass

render = web.template.render('templates/my')

class MyIndex(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
        
    def GET(self): 
        if self.is_logged:
            return render.myindex()
        else:
            web.SeeOther('../user/login')
            
class MyWishAdd(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
        
    def GET(self):
        if self.is_logged:
            return render.addwish()
        else:
            web.SeeOther('../user/login')
            
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            uid = self.uid
            gift = self._gift_exsit(uid, pkey)
            if not gift:
                new = WishList()
                new.user_id = uid
                new.product_pkey = pkey
                new.create_time = NOW
                mygift.add(new)
                
                return self.success()
            else:
                if gift.status == MY_WISH_STATUS_DELETED:
                    gift.status = MY_WISH_STATUS_DELETED
                if mygift.is_modified(gift):
                    print mygift.add(gift)
        else:
            return self.forbidden()
    
    def _gift_exsit(self, uid, pkey):
        flag = False
        query = mygift.query(WishList)
        gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid).first()
        if gift:
            flag = gift
        return flag
    
class MyWishUndo(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            uid = self.uid

            query = mygift.query(WishList)
            gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid).first()
            if gift is not None:
                gift.status = MY_WISH_STATUS_DELETED
                if mygift.is_modified(gift):
                    print mygift.add(gift)
                    return self.success()
            else:
                return self.failed()
            
        else:
            return self.forbidden()
        
class MyWishAgain(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            pkey = web.input().pkey
            uid = self.uid

            query = mygift.query(WishList)
            gift = query.filter(WishList.product_pkey == pkey).filter(WishList.user_id == uid).first()
            if gift is not None and gift.status == MY_WISH_STATUS_BUYED:
                gift.status = MY_WISH_STATUS_FOLLOW
                if mygift.is_modified(gift):
                    print mygift.add(gift)
                    return self.success()
            else:
                return self.failed()
            
        else:
            return self.forbidden()
            
class MyWish(MyResponse, FooAuth):
    def __init__(self):
        MyResponse.__init__(self)
        FooAuth.__init__(self)
        
    def GET(self):
        if self.is_logged:
            return render.mywish()
        else:
            web.SeeOther('../user/login')
            
    def POST(self):
        if self.is_logged:
            uid = self.uid
            query = mygift.query(WishList)
            product_query = mygift.query(Product)
            wishlist = query.filter(WishList.user_id == uid).\
                filter(WishList.status == MY_WISH_STATUS_FOLLOW).filter(WishList.status == MY_WISH_STATUS_BUYED).all()
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
