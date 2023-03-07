### Had the issue with the UUID type not being recognized by the database
### I found this solution on StackOverflow: https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class Movie(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    # VhsCopy relationship with Movie table (one-to-many)
    vhs_tape_copy = db.relationship(
        "VhsTapeCopy",
        back_populates="movie",
        uselist=True,
        cascade="all, delete-orphan",
    )

    # VhsRental relationship with Movie table (one-to-many)
    rentals = db.relationship(
        "VhsRental", back_populates="movie", cascade="all, delete-orphan"
    )

    def available_count(self):
        return sum(1 for tape in self.vhs_tape_copy if tape.is_available)

    def to_dict(self):
        return {
            "id": self.id,
            "date_added": self.date_added.strftime("%d-%m-%Y %H:%M:%S"),
            "title": self.title,
            "director": self.director,
            "genre": self.genre,
            "length": self.length,
            "year": self.year,
            "rating": self.rating,
            "description": self.description,
            "image": self.image,
            "available_count": self.available_count(),
            "vhs_copies": [
                {
                    "copy_number": vhs_tape_copy.copy_number,
                    "is_available": vhs_tape_copy.is_available,
                }
                for vhs_tape_copy in self.vhs_tape_copy
            ],
        }

    def __repr__(self):
        return f"<Movie id={self.id}, title={self.title}>"


class VhsTapeCopy(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    copy_number = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    # Movie relationship with VhsTapeCopy table (one-to-many)
    # ondelete="CASCADE" deletes the VhsTapeCopy record if the Movie record is deleted
    # https://docs.sqlalchemy.org/en/13/orm/cascades.html
    # https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    movie_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("movie.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Movie relationship with VhsTapeCopy table (one-to-many)
    # cascade="all, delete-orphan" deletes the VhsTapeCopy record if the Movie record is deleted. The 'delete-orphan' option deletes the VhsTapeCopy record if the Movie record is deleted
    rentals = db.relationship(
        "VhsRental",
        back_populates="vhs_tape_copy",
        cascade="all, delete-orphan",
    )

    movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey("movie.id"), nullable=True)
    movie = db.relationship("Movie", back_populates="vhs_tape_copy")
    rentals = db.relationship("VhsRental", back_populates="vhs_tape_copy")

    def __repr__(self):
        return f"<VhsTapeCopy id={self.id}, movie_id={self.movie_id}>"
