from sqlalchemy import String, Column, Integer, DateTime, Float, ForeignKey, Text, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(String(80), primary_key=True)
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(BLOB)
    store_book = relationship("StoreBook",
                              cascade='save-update, delete, merge',
                              backref='book',
                              lazy=True)
    new_order = relationship('NewOrder',
                             cascade='save-update, delete, merge',
                             backref='book',
                             lazy=True)


# new definition of User
class User2(Base):
    __tablename__ = 'user'
    user_id = Column(String(80), primary_key=True, nullable=False)
    password = Column(String(80), nullable=False)
    balance = Column(Float, nullable=False)
    token = Column(Text, default=None)
    terminal = Column(String(80), default=None)
    order_list = relationship("OrderList",
                              cascade="save-update, delete, merge",
                              backref="user",
                              lazy=True)  # backref: many-to-one semantics
    user_store = relationship("UserStore",
                              cascade='save-update, delete, merge',
                              backref='user',
                              lazy=True)


class UserStore(Base):
    __tablename__ = 'user_store'
    store_id = Column(String(80), primary_key=True)
    user_id = Column(String(80), ForeignKey('user.user_id'))
    address_from = Column(String(80))
    order_list = relationship("OrderList",
                              cascade='save-update, delete, merge',
                              backref='user_store',
                              lazy=True)
    store_book = relationship('StoreBook',
                              cascade='save-update, delete, merge',
                              backref='user_store',
                              lazy=True)


class StoreBook(Base):
    __tablename__ = 'store_book'
    store_id = Column(String(80), ForeignKey('user_store.store_id'), primary_key=True)
    book_id = Column(String(80), ForeignKey('book.book_id'), primary_key=True)
    price = Column(Integer)
    stock_level = Column(Integer)


class NewOrder(Base):
    __tablename__ = 'new_order'
    book_id = Column(String(80), ForeignKey('book.book_id'), primary_key=True)
    order_id = Column(String(180), primary_key=True)
    count = Column(Integer)
    status = Column(Integer)


# 订单列表的新定义
class OrderList(Base):
    __tablename__ = 'order_list'
    order_id = Column(String(180), primary_key=True)
    user_id = Column(String(80), ForeignKey('user.user_id'))
    store_id = Column(String(80), ForeignKey('user_store.store_id'))
    total_price = Column(Integer)
    # status = Column(Integer)
    time = Column(DateTime)  # 下单时间 最近处理时间？
    address_to = Column(String(80), default=None)

Time = {
    'START': 10,
    'CONFIRM': 10
}


class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
    ]


print("初始化已完成")