# -*- coding: utf-8 -*-
'''
Created on 2012-1-7

@author: qianmu.lxj
'''
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.types import *
import copy
import datetime
import time

NOW = time.strftime('%Y-%m-%d %X', time.localtime())

def tostring(dt):
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d %X')
    else:
        return dt

_con_str = "mysql://root:wishlist2012@localhost:3306/mygift?charset=utf8"
db = create_engine(_con_str, echo=True)

metadata = MetaData(db)

#Base = declarative_base()
user_tb = Table('user', metadata, autoload=True)
wishlist_tb = Table('wishlist', metadata, autoload=True)
product_tb = Table('product', metadata, autoload=True)
product_price_tb = Table('product_price', metadata, autoload=True)

class User(object):        
    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__,self.id,self.nickname, self.email)

class WishList(object):
    def _to_dict(self):
        _dict = {}
        key_list = ['product_pkey', 'is_shared', 'create_time', 'expect_time', 'status']
        for key in key_list:
            if key in self.__dict__.keys():
                _dict[key] = tostring(self.__dict__[key])
        return _dict
        
    def __repr__(self):
        return "%s(%r, %r, %r, %r)" % (self.__class__.__name__,self.id,self.user_id, self.product_pkey, self.status)

class ProductPrice(object):
    def _to_dict(self):
        _dict = {}
        key_list = ['update_time', 'price']
        for key in key_list:
            if key in self.__dict__.keys():
                _dict[key] = tostring(self.__dict__[key])
        return _dict
    
    def __repr__(self):
        return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.id, self.product_pkey, self.price, self.update_time)
    
class Product(object):
    def _to_dict(self):
        _dict = copy.deepcopy(self.__dict__)
        for key in _dict.keys():
            if key.find('_') >= 0:
                del(_dict[key])
        price_key = 'history_price'
        if price_key in dir(self):
            _dict[price_key] = []
            for one in self.history_price:
                _dict[price_key].append(one._to_dict())
        return _dict
    
    def __repr__(self):
        return "%s(%r, %r, %r, %r)" % (self.__class__.__name__, self.pkey, self.title, self.name, self.update_time)
    
mapper(User, user_tb)
mapper(WishList, wishlist_tb)
mapper(Product, product_tb, properties={'history_price' : relationship(ProductPrice)})
mapper(ProductPrice, product_price_tb)


MygiftSession = sessionmaker(db)
mygift = MygiftSession()
mygift.autocommit = True


if __name__ == "__main__":
    '''
    #like_search = '%'+'iphone 4'+'%'
    query = mygift.query(Product)
    query2 = mygift.query(ProductPrice)
    products = query.join(ProductPrice, Product.history_price).filter(Product.pkey == '879f1b6ecd74116e0f7e450e69b73bf2').all()
    
    for i in range(len(products)):
        print products[i]._to_dict()
        
    #print dir(products[0])
    dt = datetime.datetime(2012, 1, 11, 1, 6, 2)
    print type(dt)
    if isinstance(dt, datetime.datetime):
        print dt.strftime('%Y-%m-%d %X')
    '''
    pass
