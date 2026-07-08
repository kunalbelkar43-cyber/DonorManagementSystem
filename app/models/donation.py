from app.extensions import db


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)

    receipt_no = db.Column(db.String(30), unique=True, nullable=False)

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=False
    )

    purpose_id = db.Column(
        db.Integer,
        db.ForeignKey("donation_purposes.id"),
        nullable=False
    )

    payment_mode_id = db.Column(
        db.Integer,
        db.ForeignKey("payment_modes.id"),
        nullable=False
    )

    amount = db.Column(db.Numeric(10, 2), nullable=False)

    donation_date = db.Column(db.Date, nullable=False)

    remarks = db.Column(db.Text)

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(db.DateTime, server_default=db.func.now())