from app.extensions import db


class Donation(db.Model):
    __tablename__ = "donations"

    # ==========================
    # Primary Key
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    receipt_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    # ==========================
    # Foreign Keys
    # ==========================
    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=False
    )

    payment_mode_id = db.Column(
        db.Integer,
        db.ForeignKey("payment_modes.id"),
        nullable=True
    )

    purpose_id = db.Column(
        db.Integer,
        db.ForeignKey("donation_purposes.id"),
        nullable=False
    )

    received_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ==========================
    # Common Fields
    # ==========================
    donation_date = db.Column(
        db.Date,
        nullable=False
    )

    donation_type = db.Column(
        db.String(30),
        nullable=False,
        default="Monetary"
    )

    remarks = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # =====================================================
    # Monetary Donation Fields
    # =====================================================

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    transaction_reference = db.Column(
        db.String(100)
    )

    bank_name = db.Column(
        db.String(100)
    )

    account_number = db.Column(
        db.String(50)
    )

    ifsc_code = db.Column(
        db.String(20)
    )

    cheque_number = db.Column(
        db.String(50)
    )

    cheque_date = db.Column(
        db.Date
    )

    utr_number = db.Column(
        db.String(100)
    )

    # =====================================================
    # In-Kind Donation Fields
    # =====================================================

    item_name = db.Column(
        db.String(200)
    )

    category = db.Column(
        db.String(100)
    )

    quantity = db.Column(
        db.String(100)
    )

    estimated_value = db.Column(
        db.Numeric(10, 2)
    )

    # ==========================
    # Relationships
    # ==========================
    donor = db.relationship(
        "Donor",
        back_populates="donations"
    )

    payment_mode = db.relationship(
        "PaymentMode"
    )

    purpose = db.relationship(
        "DonationPurpose"
    )

    receiver = db.relationship(
        "User"
    )