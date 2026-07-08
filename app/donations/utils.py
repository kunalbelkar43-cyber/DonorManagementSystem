from app.models.donation import Donation


def generate_receipt_number():
    """
    Generate receipt numbers like:
    RCP000001
    RCP000002
    """

    last = Donation.query.order_by(Donation.id.desc()).first()

    if last:
        number = int(last.receipt_no.replace("RCP", "")) + 1
    else:
        number = 1

    return f"RCP{number:06d}"