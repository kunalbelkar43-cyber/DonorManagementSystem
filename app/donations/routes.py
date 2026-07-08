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
from app.donations.utils import generate_receipt_number

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
        if (
            form.payment_mode.data
            and form.payment_mode.data != 1
            and not form.transaction_reference.data
        ):
            form.transaction_reference.errors.append(
        "Transaction Reference is required for non-cash payments."
    )

        donation = Donation(
        receipt_no=generate_receipt_number(),
        donor_id=form.donor.data,
        donation_date=form.donation_date.data,
        amount=form.amount.data,
        payment_mode_id=form.payment_mode.data,
        purpose_id=form.purpose.data,
        transaction_reference=form.transaction_reference.data,
        remarks=form.remarks.data,
        received_by=current_user.id
    )

    db.session.add(donation)
    db.session.commit()

    flash("Donation recorded successfully.", "success")

    return redirect(
    url_for(
        "donations.view_donation",
        donation_id=donation.id
    )
)

@donations.route("/")
@login_required
def list_donations():

    donations = Donation.query.order_by(
        Donation.id.desc()
    ).all()

    return render_template(
        "donations/list.html",
        donations=donations
    )
@donations.route("/view/<int:donation_id>")
@login_required
def view_donation(donation_id):

    donation = Donation.query.get_or_404(donation_id)

    return render_template(
        "donations/view.html",
        donation=donation
    )
