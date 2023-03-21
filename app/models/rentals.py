from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class VhsRental(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_rented = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_returned = db.Column(db.DateTime, default=None, nullable=True)
    is_removed = db.Column(db.Boolean, default=False, nullable=False)

    # Customer relationship with VhsRental table (one-to-many)
    customer_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("customer.id"),
        nullable=True,
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


class ArchivedRental(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_rented = db.Column(db.DateTime, nullable=False)
    date_returned = db.Column(db.DateTime, nullable=False)
    date_archived = db.Column(db.DateTime, nullable=False)

    # TODO: Add date_archived column
    # need to fix rest of the code: views, forms, etc.
    # when vhs_tape_copy is removed, it should be archived and not be available for renting/deleting/returning

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="archived_rentals")

    customer_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("customer.id"),
        nullable=True,
    )

    customer = db.relationship("Customer", back_populates="archived_rentals")

    movie_id = db.Column(UUID(as_uuid=True), db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship("Movie", back_populates="archived_rentals")

    vhs_tape_copy_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("vhs_tape_copy.id"), nullable=False
    )
    vhs_tape_copy = db.relationship("VhsTapeCopy", back_populates="archived_rentals")


def __repr__(self):
    return f"<ArchivedRental id={self.id}, vhs_tape_copy_id={self.vhs_tape_copy_id}, user_id={self.user_id}>"
