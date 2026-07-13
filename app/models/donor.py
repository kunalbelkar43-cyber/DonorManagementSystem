from app.extensions import db
from datetime import datetime


class Donor(db.Model):
    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True)

    donor_code = db.Column(db.String(20), unique=True, nullable=False)
    
    dob = db.Column(db.Date, nullable=True)

    full_name = db.Column(db.String(150), nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    email = db.Column(db.String(120))

    dob = db.Column(db.Date, nullable=True)

    pan_number = db.Column(db.String(10), unique=True, nullable=True)

    address = db.Column(db.Text)

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    pincode = db.Column(db.String(10))

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    status = db.Column(db.Boolean, default=True)

    donations = db.relationship(
    "Donation",
    back_populates="donor",
    lazy=True,
    cascade="all, delete-orphan"
)
    
    donor_type_id = db.Column(
        db.Integer,
        db.ForeignKey("donor_types.id"),
        nullable=False
    )

    donor_type = db.relationship(
    "DonorType",
    backref="donors"
)


    