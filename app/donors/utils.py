from app.models.donor import Donor


def generate_donor_code():
    last_donor = Donor.query.order_by(Donor.id.desc()).first()

    if last_donor:
        number = int(last_donor.donor_code.replace("DNR", "")) + 1
    else:
        number = 1

    return f"DNR{number:06d}"