import uuid
import logging
from be.model import db_conn
from be.model import error
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import PyMongoError
from be.model.times import add_unpaid_order, delete_unpaid_order, check_order_time, get_time_stamp
from be.model.order import Order
from be.model.nlp import encrypt

class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
        self.page_size = 3

   

    def search(self, search_key, page=0) -> (int, str, list):
        try:
            if page > 0:
                page_lower = self.page_size * (page - 1)
                cursor = self.conn.execute(
                    "SELECT book_id, book_title, book_author from invert_index "
                    "where search_key = '%s' "
                    "ORDER BY search_id limit '%d' offset '%d';"
                    % (search_key, self.page_size, page_lower))
            else:
                cursor = self.conn.execute(
                    "SELECT book_id, book_title, book_author from invert_index "
                    "where search_key = '%s' "
                    "ORDER BY search_id  ;"
                    % (search_key))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                book = {
                    "bid": row[0],
                    "title": row[1],
                    "author": row[2]
                }
                result.append(book)

            self.conn.commit()
        except SQLAlchemyError as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result

    def search_many(self, word_list):
        try:
            tresult = []
            for word in word_list:
                code, message, sresult = self.search(word, 0)
                if code != 200:
                    continue
                tresult += sresult
            uni = {}
            for dic in tresult:
                if dic['bid'] in uni.keys():
                    continue
                uni[dic['bid']] = dic
            result = list(uni.values())
        except SQLAlchemyError as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result

    def get_book_info(self, bid_list):
        try:
            result = []
            for bid in bid_list:
                book = self.mongo['book'].find_one({'id': bid},{'_id':0})
                if book != None:
                    result.append(book)
        except PyMongoError as e:
            return 529, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result

    def search_in_store(self, store_id, search_key, page=0):
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if page > 0:
                page_lower = self.page_size * (page - 1)
                cursor = self.conn.execute(
                    "SELECT i.book_id, i.book_title, i.book_author, s.price, s.stock_level "
                    "from invert_index i, store s "
                    "where i.search_key = '%s' and i.book_id = s.book_id and s.store_id = '%s' "
                    "ORDER BY i.search_id limit '%d' offset '%d' ;"
                    % (search_key, store_id, self.page_size, page_lower))
            else:
                cursor = self.conn.execute(
                    "SELECT i.book_id, i.book_title, i.book_author, s.price, s.stock_level "
                    "from invert_index i, store s "
                    "where i.search_key = '%s' and i.book_id = s.book_id and s.store_id = '%s' "
                    "ORDER BY i.search_id ;"
                    % (search_key, store_id))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                book = {
                    "bid": row[0],
                    "title": row[1],
                    "author": row[2],
                    "price": row[3],
                    "storage": row[4]
                }
                result.append(book)

            self.conn.commit()
        except SQLAlchemyError as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        return 200, "ok", result