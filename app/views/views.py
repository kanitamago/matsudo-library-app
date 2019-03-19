from app import app
from flask import render_template, url_for, redirect, request
from app.scripts import getInfo, createFile, editFile, libraryData
from app import db
from app.models.circleModel import Circle
from app.models.bookModel import Books
from app.models.colorModel import Colors
from random import randint
import os
import shutil

@app.route("/")
def index():
    q = randint(1, 99999)
    head, div, script = editFile.get_elements()
    library_names = libraryData.get_library_names()
    each_library_dic = split_each_library(library_names)
    KeywordColors = get_keywordColors()
    return render_template("index.html", head=head, div=div, script=script, library_names=library_names, each_library_dic=each_library_dic, KeywordColors=KeywordColors, q=q)

@app.route("/", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        input_keyword = request.form["keyword"]
        checker = already_exist_check(input_keyword)
        if checker:
            print("Already Exist.")
            return redirect(url_for("index"))
        #存在しない登録キーワードをデータベースに登録
        else:
            library = getInfo.Library(input_keyword)
            all_library_info = library.scraping()
            all_exist_num = all_library_info["all_exist_num"]
            each_library = all_library_info["each_library"]
            circleChecker = register_circle(each_library)
            booksChecker = register_books(each_library)
            createChecker = create_file()
            return redirect(url_for('index'))
    else:
        return redirect(url_for("index"))

@app.route("/delete/<keyword>", methods=["GET", "POST"])
def deleteKeyword(keyword):
    try:
        if request.method == "POST":
            circles_items = Circle.query.filter(Circle.keyword == keyword).all()
            books_items = Books.query.filter(Books.keyword == keyword).all()
            colors_items = Colors.query.filter(Colors.keyword == keyword).all()
            for circle_item in circles_items:
                db.session.delete(circle_item)
                db.session.commit()
            for book_item in books_items:
                db.session.delete(book_item)
                db.session.commit()
            for color_item in colors_items:
                db.session.delete(color_item)
                db.session.commit()
            createChecker = create_file()
            return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
    except:
        return redirect(url_for("index"))

#大枠データベース(Circle)
def register_circle(each_library):
    try:
        for library in each_library:
            keyword = library["keyword"]
            library_name = library["library_name"]
            exist_num = library["exist_num"]
            circle = Circle(keyword, library_name, exist_num)
            db.session.add(circle)
            db.session.commit()
        return True
    except:
        return False

#書籍詳細データベース(Books)
def register_books(each_library):
    try:
        for library in each_library:
            keyword = library["keyword"]
            library_name = library["library_name"]
            books_info = library["books_info"]
            titles = books_info["title"]
            publishers = books_info["publisher"]
            publish_dates = books_info["publish_date"]
            authors = books_info["author"]
            lends = books_info["lend"]
            holdings = books_info["holding"]
            reserves = books_info["reserve"]
            if titles and publishers and publish_dates and authors and lends and holdings and reserves:
                for title, publisher, publish_date, author, lend, holding, reserve in zip(titles, publishers, publish_dates, authors, lends, holdings, reserves):
                    book = Books(keyword, library_name, title, publisher, publish_date, author, lend, holding, reserve)
                    db.session.add(book)
                    db.session.commit()
            else:
                book = Books(keyword, library_name, "", "", "", "", "", "", "")
                db.session.add(book)
                db.session.commit()
        return True
    except:
        return False

#キーワード色データベース(KeywordColor)
def register_keywordColor(keyword_color_dic):
    colors = Colors.query.order_by(Colors.id.desc()).all()
    #{'機械学習': 'rgb(31, 218, 153)', '乃木坂46': 'rgb(232, 245, 109)', 'Python': 'rgb(176, 242, 89)', 'JavaScript': 'rgb(161, 16, 202)'}
    for keyword, color in keyword_color_dic.items():
        if colors:
            existed_item = Colors.query.filter(Colors.keyword == keyword).first()
            if existed_item:
                existed_item.keyword_color = color
                db.session.commit()
            else:
                color_item = Colors(keyword, color)
                db.session.add(color_item)
                db.session.commit()
        else:
            color_item = Colors(keyword, color)
            db.session.add(color_item)
            db.session.commit()

def already_exist_check(input_keyword):
    books = Books.query.order_by(Books.id.desc()).all()
    book_keywords = set([book.keyword for book in books])
    circles = Circle.query.order_by(Circle.id.desc()).all()
    circle_keywords = set([circle.keyword for circle in circles])
    if input_keyword in book_keywords and input_keyword in circle_keywords:
        return True
    else:
        return False

def split_each_library(library_names):
    books = Books.query.order_by(Books.id.desc()).all()
    circles = Circle.query.order_by(Circle.id.desc()).all()
    circle_dic = {}
    books_dic = {}
    each_library_dic = {}
    for library in library_names:
        circle_dic[library] = [circle for circle in circles if circle.library_name in library]
        books_dic[library] = [book for book in books if book.library_name in library]
    for circle_item, books_item in zip(circle_dic.items(), books_dic.items()):
        if circle_item[0] == books_item[0]:
            temp_dic = {}
            temp_dic["basicInfo"] = circle_item[1]
            temp_dic["detailBooksInfo"] = books_item[1]
            each_library_dic[circle_item[0]] = temp_dic
    return each_library_dic

def get_keywordColors():
    KeywordColors = Colors.query.order_by(Colors.id.desc()).all()
    return KeywordColors

def clean_circle(circles):
    circle_keywords = set([circle.keyword for circle in circles])
    circle_dic = {}
    for keyword in circle_keywords:
        circle_dic[keyword] = [circle for circle in circles if circle.keyword == keyword]
    return (circle_dic, circle_keywords)

def create_file():
    circles = Circle.query.order_by(Circle.id.desc()).all()
    if circles:
        circle_dic, circle_keywords = clean_circle(circles)
        FileChecker, keyword_color = createFile.put_library_position(circle_dic, circle_keywords)
        colorChecker = register_keywordColor(keyword_color)
        message = createFile.create_library_file(FileChecker)
        return message
    else:
        filename = os.listdir("app/mapfile")[0]
        filename = "app/mapfile/"+filename
        os.remove(filename)
        print("Delete HTML File.")
        return "Delete HTML File."
