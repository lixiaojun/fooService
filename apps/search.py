# -*- coding: utf-8 -*-
'''
Created on 2012-1-10

@author: qianmu.lxj
'''

from apps.fooinc import FooResponse, notfound, internalerror, FooAuth
from apps.my import FooStatus
from libs.utils import Validation
from models.mygift import Product, WishList
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

class MyProductFlag:
    
    @staticmethod
    def setMyFlag(uid, products):
        query = web.ctx.mygift.query(WishList.product_pkey, WishList.wlstatus)
        wishlist_follow = query.filter(WishList.user_id == uid).\
                filter(WishList.wlstatus == FooStatus.MY_WISH_STATUS_FOLLOW).all()
        wishlist_follow_p, wishlist_follow_s = MyProductFlag._to_list(wishlist_follow)
        wishlist_buyed  = query.filter(WishList.user_id == uid).\
            filter(WishList.wlstatus == FooStatus.MY_WISH_STATUS_BUYED).all()
                #filter(or_(WishList.wlstatus == FooStatus.MY_WISH_STATUS_BUYED, 'wlstatus REGEXP "[0-9]+" ')).all()
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
    
class SearchValidation(Validation):
    @staticmethod
    def check_string(search):
        ispass = False
        if Validation.isString(search) and not Validation.isEmpty(search):
            ispass = True
        return ispass
    
    @staticmethod
    def check_searchproduct(search):
        return SearchValidation.check_string(search)
    
    @staticmethod
    def check_searchproductbyid(search):
        return SearchValidation.check_string(search) and Validation.isIntId(search)
    
    @staticmethod
    def check_searchproductbypkey(search):
        return Validation.isMd5(search)

class SearchProduct(SearchResponse, FooAuth):
    def __init__(self):
        SearchResponse.__init__(self)
        FooAuth.__init__(self)
        
    def POST(self):
        if self.is_logged:
            search = web.input().search
            if not SearchValidation.check_searchproduct(search):
                return self.dataerror()
            sret = self.failed()
            try:
                products = self._search_product(search)
                products = MyProductFlag.setMyFlag(self.uid, products)
                sret = self.product_success(products)
            except:
                pass
                raise
            
            return sret
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
        
    def POST(self):
        if self.is_logged:
            ptid = web.input().search
            if not SearchValidation.check_searchproductbyid(ptid):
                return self.dataerror()
            
            mret = self.failed()
            try:
                products = self._search_product_by_id(ptid)
                mret = self.product_success(products)
            except:
                pass
                raise
            
            return mret
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
            if not SearchValidation.check_searchproductbypkey(product_pkey):
                return self.dataerror()
            
            sret = self.failed()
            try:
                products = self._search_product_by_pkey(product_pkey)
                products = MyProductFlag.setMyFlag(self.uid, products)
                sret = self.product_success(products)
            except:
                pass
                raise
            
            return sret
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
