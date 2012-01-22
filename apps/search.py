# -*- coding: utf-8 -*-
'''
Created on 2012-1-10

@author: qianmu.lxj
'''

from apps.fooinc import FooResponse, notfound, internalerror, FooAuth
from models.mygift import Product, mygift
import json
import web

urls = (
        "/?", "SearchIndex",
        "/product/?", "SearchProduct",
        "/product/title/?", "SearchProduct",
        "/product/id/?", "SearchProductById",
        )

class SearchResponse(FooResponse):
    
    def product_success(self, products):
        return self._product_success2json(products)
        
    def _product_success2json(self, products):
        ret = self.ret
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

class SearchProduct(SearchResponse, FooAuth):
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
            search = web.input().search
            products = self._search_product(search)
            return self.product_success(products)
        else:
            return self.forbidden()
        
    def _search_product(self, search):
        if search is None:
            search = 'Nothing'
                 
        like_search = '%'+search+'%'    
        query = mygift.query(Product)
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
        query = mygift.query(Product)
        products = query.filter(Product.id == search).all()
        return products

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
