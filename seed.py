from app import create_app
from app.extensions import db
from app.models.donor_type import DonorType
from app.models.payment_mode import PaymentMode
from app.models.donation_purpose import DonationPurpose

app = create_app()

with app.app_context():

    # -------------------------
    # Donor Types
    # -------------------------
    donor_types = [
        "Individual",
        "Organization",
        "Company",
        "Trust",
        "Government"
    ]

    for name in donor_types:
        if not DonorType.query.filter_by(name=name).first():
            db.session.add(DonorType(name=name))

    # -------------------------
    # Payment Modes
    # -------------------------
    payment_modes = [
        "Cash",
        "UPI",
        "Cheque",
        "Bank Transfer",
        "Online"
    ]

    for name in payment_modes:
        if not PaymentMode.query.filter_by(name=name).first():
            db.session.add(PaymentMode(name=name))

    # -------------------------
    # Donation Purposes
    # -------------------------
    purposes = [
        "General Fund",
        "Education",
        "Medical Assistance",
        "Food Distribution",
        "Temple Maintenance",
        "Other"
    ]

    for name in purposes:
        if not DonationPurpose.query.filter_by(name=name).first():
            db.session.add(DonationPurpose(name=name))

    db.session.commit()

    print("✅ Master data inserted successfully.")