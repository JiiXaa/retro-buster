from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class VhsRental(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_rented = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_returned = db.Column(db.DateTime, default=None, nullable=True)

    # Customer relationship with VhsRental table (one-to-many)
    customer_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("customer.id"), nullable=False
    )
    customer = db.relationship("Customer", back_populates="rentals")

    # Movie relationship with VhsRental table (one-to-many)
    movie = db.relationship("Movie", back_populates="rentals")

    movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey("movie.id"), nullable=False)

    # VhsTapeCopy relationship with VhsRental table (one-to-many)
    vhs_tape_copy_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("vhs_tape_copy.id"), nullable=False
    )
    vhs_tape_copy = db.relationship("VhsTapeCopy", back_populates="rentals")

    def __repr__(self):
        return f"<VhsRental id={self.id}, vhs_tape_copy_id={self.vhs_tape_copy_id}, customer_id={self.customer_id}>"
