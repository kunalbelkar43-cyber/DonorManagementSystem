from app.extensions import db


class DonorType(db.Model):
    __tablename__ = "donor_types"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable=False)