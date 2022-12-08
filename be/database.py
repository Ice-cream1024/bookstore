import enum

import psycopg2
from sqlalchemy import create_engine, Column
from sqlalchemy import BigInteger, String, Integer, ForeignKey, ForeignKeyConstraint, Text, DateTime, Boolean, LargeBinary, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from be.timeout import delay
import datetime

engine = create_engine('postgresql://root:123456@localhost:5432/bookstore')
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    terminal = Column(String, nullable=False)


class Store(Base):
    __tablename__ = 'store'
    store_id = Column(String,nullable=False,primary_key=True)
    owner = Column(String, ForeignKey('user.user_id'), nullable=False, index=True)


class Book_info(Base):
    __tablename__ = 'book_info'
    id = Column(String, primary_key=True)
    store_id = Column(String, ForeignKey('store.store_id'), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    inventory_count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)  # 原价


class Book_tag(Base):
    __tablename__ = 'book_tag'
    id = Column(String, primary_key=True)
    store_id = Column(String, ForeignKey('store.store_id'), primary_key=True)
    tag = Column(String, primary_key=True)


# 订单状态
class Order_status(enum.IntEnum):
    pending = 0  # 等待付款
    cancelled = 1  # 已取消
    paid = 2  # 已付款等待发货
    delivering = 3  # 已发货
    received = 4  # 已确认收货


Order_Status_String = [
    "pending",
    "cancelled",
    "paid",
    "delivering",
    "received"
]


# 订单概要
class Order(Base):
    __tablename__ = 'order'
    id = Column(String, primary_key=True)
    status = Column(Enum(Order_status), nullable=False)
    buyer_id = Column(String, ForeignKey('user.user_id'), nullable=False)
    store_id = Column(String, ForeignKey('store.store_id'), nullable=False)
    pt = Column(DateTime, nullable=False)


# 订单详情
class Order_info(Base):
    __tablename__ = 'order_info'
    order_id = Column(String, ForeignKey('order.id'), primary_key=True, nullable=False)
    book_id = Column(String, primary_key=True, nullable=False)
    store_id = Column(String)
    ForeignKeyConstraint(['store_id', 'book_id'], ['book_info.store_id', 'book_info.id'])
    count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    

# 书籍图片
class Book_pic(Base):
    __tablename__ = 'book_pic'
    store_id = Column(String, primary_key=True)
    book_id = Column(String, primary_key=True)
    pic_id = Column(Integer, primary_key=True, autoincrement=True)
    ForeignKeyConstraint(['store_id', 'book_id'], ['book_info.store_id', 'book_info.id'])
    picture = Column(LargeBinary,nullable=False)


def run_clear():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session.commit()
    Cancel_not_paid(session)
    print("finish")

@delay(1.0)
def Cancel_not_paid(session):
    cur_pt = datetime.datetime.now() - datetime.timedelta(seconds = 5)
    try:
        cursor = session.query(Order).filter(Order.status==Order_status.pending, Order.pt < cur_pt)
        rowcount = cursor.update({Order.status: Order_status.cancelled})

        session.commit()
    except BaseException as e:
        pass
    Cancel_not_paid(session)
