from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.buyer import Buyer
from be.model.ocr import OCR



@bp_buyer.route("/search", methods=["POST"])
def search():
    search_key: str = request.json.get("search_key")
    page: int = request.json.get("page")
    b = Buyer()
    code, message, result = b.search(search_key, page)
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/search_many", methods=["POST"])
def search_many():
    search_key: list = request.json.get("search_key")
    # page: str = request.json.get("page")
    b = Buyer()
    code, message, result = b.search_many(search_key)
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/upload",methods=["POST"])
def get_ocr():
    png = request.files.get('png')
    png.save('./math.png')
    path='./math.png'
    o = OCR()
    code, message, result=o.OCR_pic(path)
    return jsonify({"message": message, "result": result}), code


@bp_buyer.route("/upload_cv",methods=["POST"])
def get_ocr_cv():
    # png = request.files.get('png')
    # png.save('./math.png')
    # path='./math.png'
    o = OCR()
    code, message, result=o.OCR_pic_cv()
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/get_books_info", methods=["POST"])
def check_books_info():
    book_list: list = request.json.get("books")
    b = Buyer()
    code, message, result = b.get_book_info(book_list)
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/search_in_store", methods=["POST"])
def search_in_store():
    search_key: str = request.json.get("search_key")
    store_id: str = request.json.get("store_id")
    page: int = request.json.get("page")
    b = Buyer()
    code, message, result = b.search_in_store(store_id, search_key, page)
    return jsonify({"message": message, "result": result}), code