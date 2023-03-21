from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class Customer(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    # phone_number = db.Column(db.String(100), nullable=False)
    # address = db.Column(db.String(100), nullable=False)
    # city = db.Column(db.String(100), nullable=False)
    # postcode = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # VhsRental relationship with Customer table (one-to-many)
    rentals = db.relationship("VhsRental", back_populates="customer")

    # ArchivedRental relationship with Customer table (one-to-many)
    archived_rentals = db.relationship("ArchivedRental", back_populates="customer")

    def __repr__(self):
        return f"<Customer id={self.id}, first_name={self.first_name}, last_name={self.last_name}>"
