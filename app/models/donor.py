from app.extensions import db


class Donor(db.Model):
    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True)

    donor_code = db.Column(db.String(20), unique=True, nullable=False)

    full_name = db.Column(db.String(150), nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    email = db.Column(db.String(120))

    address = db.Column(db.Text)

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    pincode = db.Column(db.String(10))

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    status = db.Column(db.Boolean, default=True)
    donor_type_id = db.Column(
        db.Integer,
        db.ForeignKey("donor_types.id"),
        nullable=False
    )

    