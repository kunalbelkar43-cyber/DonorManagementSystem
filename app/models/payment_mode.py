from app.extensions import db


class PaymentMode(db.Model):
    __tablename__ = "payment_modes"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable=False)