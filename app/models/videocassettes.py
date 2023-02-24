### Had the issue with the UUID type not being recognized by the database
### I found this solution on StackOverflow: https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class Videocassette(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    # VhsDetails relationship with Videocassette table (one-to-many)
    vhs_details = db.relationship(
        "VhsDetails", back_populates="videocassette", uselist=True
    )

    # VhsRental relationship with Videocassette table (one-to-many)
    rentals = db.relationship("VhsRental", back_populates="videocassette")

    def available_count(self):
        return sum(1 for detail in self.vhs_details if detail.is_available)

    def __repr__(self):
        return f"<Videocassette id={self.id}, title={self.title}>"


class VhsDetails(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    copy_number = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    # Videocassette relationship with VhsDetails table (one-to-many)
    # ondelete="CASCADE" deletes the VhsDetails record if the Videocassette record is deleted
    # https://docs.sqlalchemy.org/en/13/orm/cascades.html
    # https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    videocassette_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("videocassette.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Videocassette relationship with VhsDetails table (one-to-many)
    # cascade="all, delete-orphan" deletes the VhsDetails record if the Videocassette record is deleted. The 'delete-orphan' option deletes the VhsDetails record if the Videocassette record is deleted
    rentals = db.relationship(
        "VhsRental",
        back_populates="vhs_details",
        cascade="all, delete-orphan",
    )

    videocassette_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("videocassette.id"), nullable=True
    )
    videocassette = db.relationship("Videocassette", back_populates="vhs_details")
    rentals = db.relationship("VhsRental", back_populates="vhs_details")

    def __repr__(self):
        return f"<VhsDetails id={self.id}, videocassette_id={self.videocassette_id}>"
