from app import db
from datetime import datetime

class Videocassette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # add a unique public_id to the vhs tape can be exposed to the user to allow them to easily access the vhs tape details. Also could be used in the url to access the vhs tape details.
    public_id = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

    details = db.relationship("Details", back_populates="videocassette", uselist=False, cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<Videocassette id={self.id}, title={self.title}>"

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    length = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    videocassette = db.relationship("Videocassette", back_populates="details")
    videocassette_id = db.Column(db.Integer, db.ForeignKey("videocassette.public_id"))


    def __repr__(self):
        return f"<Details id={self.id}, videocassette_id={self.videocassette_id}>"
