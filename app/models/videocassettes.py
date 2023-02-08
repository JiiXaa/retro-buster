### Had the issue with the UUID type not being recognized by the database
### I found this solution on StackOverflow: https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid

class Videocassette(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

    details = db.relationship("Details", back_populates="videocassette", uselist=False, cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<Videocassette id={self.id}, title={self.title}>"

class Details(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    length = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    videocassette = db.relationship("Videocassette", back_populates="details")
    videocassette_id = db.Column(UUID(as_uuid=True), db.ForeignKey("videocassette.id"))


    def __repr__(self):
        return f"<Details id={self.id}, videocassette_id={self.videocassette_id}>"
