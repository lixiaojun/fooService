# -*- coding: utf-8 -*-
'''
Created on 2012-1-10

@author: qianmu.lxj
'''

from apps.fooinc import FooResponse, notfound, internalerror, FooAuth
from apps.my import MY_WISH_STATUS_FOLLOW, MY_WISH_STATUS_BUYED
from models.mygift import Product, WishList
from sqlalchemy.sql.expression import or_
import json
import web

urls = (
        "/?", "SearchIndex",
        "/product/?", "SearchProduct",
        "/product/title/?", "SearchProduct",
        "/product/id/?", "SearchProductById",
        "/product/pkey/?", "SearchProductByPkey",
        )

class SearchResponse(FooResponse):
    
    def product_success(self, products):
        return self._product_success2json(products)
        
    def _product_success2json(self, products):
        ret = self._ret()
        ret['status'] = FooResponse.STATUS_CODE_SUCCESS
        count = len(products)
        for i in range(count):
            products[i] = products[i]._to_dict()
        ret['root']['count'] = count
        ret['root']['data'] = products
        
        return json.dumps(ret)

class SearchIndex:
    def GET(self): 
        raise web.seeother('/product/title')

render = web.template.render('templates/search')

class MyProductFlag:
    
    @staticmethod
    def setMyFlag(uid, products):
        query = web.ctx.mygift.query(WishList.product_pkey, WishList.wlstatus)
        wishlist_follow = query.filter(WishList.user_id == uid).\
                filter(WishList.wlstatus == MY_WISH_STATUS_FOLLOW).all()
        wishlist_follow_p, wishlist_follow_s = MyProductFlag._to_list(wishlist_follow)
        wishlist_buyed  = query.filter(WishList.user_id == uid).\
                filter(or_(WishList.wlstatus == MY_WISH_STATUS_BUYED, 'wlstatus REGEXP "[0-9]+.?[0-9]*" ')).all()
        wishlist_buyed_p, wishlist_buyed_s = MyProductFlag._to_list(wishlist_buyed)
        for i in range(len(products)):
            if products[i].pkey in wishlist_follow_p:
                products[i].myflag = wishlist_follow_s[wishlist_follow_p.index(products[i].pkey)]
            elif products[i].pkey in wishlist_buyed_p:
                products[i].myflag = wishlist_buyed_s[wishlist_buyed_p.index(products[i].pkey)]
        return products
                            
    @staticmethod            
    def _to_list(grows):
        count = len(grows)
        pkeys = [] 
        status = []
        for i in range(count):
            pkeys.append(grows[i][0])
            status.append(grows[i][1])
        return pkeys, status

class SearchProduct(SearchResponse, FooAuth):
    def __init__(self):
        SearchResponse.__init__(self)
        FooAuth.__init__(self)
    
    def GET(self, search = None):
        if self.is_logged:
            return render.product()
        else:
            raise web.SeeOther('/user/login')
        
    def POST(self):
        if self.is_logged:
            search = web.input().search
            products = self._search_product(search)
            products = MyProductFlag.setMyFlag(self.uid, products)
            return self.product_success(products)
        else:
            return self.forbidden()
    
        
    def _search_product(self, search):
        if search is None:
            search = 'Nothing'
                 
        like_search = '%'+search+'%'    
        query = web.ctx.mygift.query(Product)
        products = query.filter(Product.title.like(like_search)).all()
        return products
        


class SearchProductById(SearchResponse, FooAuth):
    def __init__(self):
        SearchResponse.__init__(self)
        FooAuth.__init__(self)
    
    def GET(self, search = None):
        if self.is_logged:
            return render.product()
        else:
            return web.SeeOther('../user')
        
    def POST(self):
        if self.is_logged:
            ptid = web.input().search
            products = self._search_product_by_id(ptid)
            return self.product_success(products)
        else:
            return self.forbidden()
        
    def _search_product_by_id(self, search):
        if search is None:
            search = 'Nothing'  
        query = web.ctx.mygift.query(Product)
        products = query.filter(Product.id == search).all()
        return products
    
class SearchProductByPkey(SearchResponse, FooAuth):
    def __init__(self):
        SearchResponse.__init__(self)
        FooAuth.__init__(self)
    
    def POST(self):
        if self.is_logged:
            product_pkey = web.input().search
            products = self._search_product_by_pkey(product_pkey)
            products = MyProductFlag.setMyFlag(self.uid, products)
            return self.product_success(products)
        else:
            return self.forbidden()
        
    def _search_product_by_pkey(self, search):
        if search is None:
            search = 'Nothing'  
        query = web.ctx.mygift.query(Product)
        products = query.filter(Product.pkey == search).all()
        return products

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
