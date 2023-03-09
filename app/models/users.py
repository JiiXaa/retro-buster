from sqlalchemy.dialects.postgresql import UUID
from app import db
from datetime import datetime
import uuid


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(25), nullable=False, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User id={self.id}, last_name={self.last_name}, email={self.email}>"
