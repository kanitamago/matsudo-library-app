from app import db

class Colors(db.Model):
    __tablename__ = "color_model"
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text)
    keyword_color = db.Column(db.Text)

    def __init__(self, keyword, keyword_color):
        self.keyword = keyword
        self.keyword_color = keyword_color

    def __repr__(self):
        return """
            <COLORS ITEM>
            id: {}
            keyword: {}
            keyword_color: {}
            """.format(self.id, self.keyword, self.keyword_color)
