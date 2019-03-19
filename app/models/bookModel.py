from app import db

class Books(db.Model):
    __tablename__ = "book_model"
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text)
    library_name = db.Column(db.Text)
    title = db.Column(db.Text)
    publisher = db.Column(db.Text)
    publish_date = db.Column(db.Text)
    author = db.Column(db.Text)
    lend = db.Column(db.Text)
    holding = db.Column(db.Text)
    reserve = db.Column(db.Text)

    def __init__(self, keyword, library_name, title, publisher, publish_date, author, lend, holding, reserve):
        self.keyword = keyword
        self.library_name = library_name
        self.title = title
        self.publisher = publisher
        self.publish_date = publish_date
        self.author = author
        self.lend = lend
        self.holding = holding
        self.reserve = reserve

    def __repr__(self):
        return """
            <BOOKS ITEM>
            id: {}
            keyword: {}
            library_name: {}
            title: {}
            publisher: {}
            publish_date: {}
            author: {}
            lend: {}
            holding: {}
            reserve: {}
            """.format(self.id, self.keyword, self.library_name, self.title, self.publisher, self.publish_date, self.author, self.lend, self.holding, self.reserve)
