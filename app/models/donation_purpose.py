from app.extensions import db


class DonationPurpose(db.Model):
    __tablename__ = "donation_purposes"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)