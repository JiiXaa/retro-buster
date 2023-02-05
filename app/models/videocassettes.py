from app import db


class Videocassette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Videocassette id={self.id}, title={self.title}>"
