from app import db

class Circle(db.Model):
    __tablename__ = "circle_model"
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text)
    library_name = db.Column(db.Text)
    exist_num = db.Column(db.Integer)

    def __init__(self, keyword, library_name, exist_num):
        self.keyword = keyword
        self.library_name = library_name
        self.exist_num = exist_num

    def __repr__(self):
        return """
            <CIRCLES ITEM>
            id: {}
            keyword: {}
            library_name: {}
            exist_num: {}
            """.format(self.id, self.keyword, self.library_name, self.exist_num)
