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
    length = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)

    vhs_details = db.relationship(
        "VhsDetails",
        back_populates="videocassette",
        uselist=False,
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return f"<Videocassette id={self.id}, title={self.title}>"


class VhsDetails(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    copies_available = db.Column(db.Integer, nullable=False)
    copy_number = db.Column(db.Integer, nullable=False)

    videocassette_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("videocassette.id"), nullable=False
    )
    videocassette = db.relationship("Videocassette", back_populates="vhs_details")
    rentals = db.relationship("VhsRental", back_populates="vhs_details")

    def __repr__(self):
        return f"<VhsDetails id={self.id}, videocassette_id={self.videocassette_id}>"

    class VhsRental(db.Model):
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        date_rented = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        date_returned = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

        customer_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("customer.id"), nullable=False
        )
        customer = db.relationship("Customer", back_populates="rentals")
        vhs_details_id = db.Column(
            UUID(as_uuid=True), db.ForeignKey("vhs_details.id"), nullable=False
        )
        vhs_details = db.relationship("VhsDetails", back_populates="rentals")

        def __repr__(self):
            return f"<VhsRental id={self.id}, vhs_details_id={self.vhs_details_id}, customer_id={self.customer_id}>"
