from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


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
