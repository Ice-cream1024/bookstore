from be.model import error
from be.database import User, Store, Order, Order_status, Book_pic
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Seller():
    def __init__(self):
        engine = create_engine('postgresql://root:123456@localhost:5432/bookstore')
        self.session = sessionmaker(bind=engine)()

    def add_book(self, user_id: str, store_id: str, book_info: dict):
        try:
            book_id = book_info.get('id')

            if not self.user_id_efoxist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            book = book_info()
            book.id = book_id
            book.title = book_info.get('title')
            book.store_id = store_id
            book.author = book_info.get("author", None)
            book.publisher = book_info.get("publisher", None)
            book.original_title = book_info.get("original_title", None)
            book.pub_year = book_info.get("pub_year", None)
            book.pages = book_info.get("pages", None)
            book.binding = book_info.get("binding", None)
            book.isbn = book_info.get("isbn", None)
            book.author_intro = book_info.get("author_intro", None)
            book.book_intro = book_info.get("book_intro", None)
            book.content = book_info.get("content", None)
            book.price = book_info.get("price", 0)

            book.inventory_count = stock_level
            
            self.session.add(book)

            book.tags= book_info.get("tags", [])
            for tag in book.tags:
                book_tag = Book_tag()
                book_tag.id = book.id
                book_tag.store_id = store_id
                book_tag.tag = tag
                self.session.add(book_tag)

            pictures = book_info.get("pictures", [])
            for pic in pictures:
                book_pic = Book_pic()
                book_pic.book_id = book.id
                book_pic.store_id = store_id
                book_pic.picture = pic.encode('ascii')
                self.session.add(book_pic)

            self.session.commit()
            self.session.close()


        except BaseException as e:
            return 540, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str):