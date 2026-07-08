from datetime import date

from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db
from app.donations import donations
from app.donations.forms import DonationForm

from app.models.donor import Donor
from app.models.payment_mode import PaymentMode
from app.models.donation_purpose import DonationPurpose
from app.models.donation import Donation

@donations.route("/add", methods=["GET", "POST"])
@login_required
def add_donation():

    form = DonationForm()

    form.donor.choices = [
        (
            donor.id,
            f"{donor.donor_code} - {donor.full_name}"
        )
        for donor in Donor.query.order_by(Donor.full_name).all()
    ]

    form.payment_mode.choices = [
        (mode.id, mode.name)
        for mode in PaymentMode.query.order_by(PaymentMode.name).all()
    ]

    form.purpose.choices = [
        (purpose.id, purpose.name)
        for purpose in DonationPurpose.query.order_by(DonationPurpose.name).all()
    ]

    if form.validate_on_submit():

        flash(
            "Donation form validated successfully.",
            "success"
        )

        return redirect(
            url_for("donations.list_donations")
        )

    form.donation_date.data = date.today()

    return render_template(
        "donations/add.html",
        form=form
    )