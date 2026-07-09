from flask import render_template
from flask_login import login_required

from app.reports import reports
from app.reports.forms import DonationReportForm

from app.models import (
    Donor,
    PaymentMode,
    DonationPurpose
)


@reports.route("/donations", methods=["GET", "POST"])
@login_required
def donation_report():

    form = DonationReportForm()

    form.donor.choices = [(0, "All Donors")] + [
        (d.id, d.full_name)
        for d in Donor.query.order_by(Donor.full_name).all()
    ]

    form.payment_mode.choices = [(0, "All Payment Modes")] + [
        (p.id, p.name)
        for p in PaymentMode.query.order_by(PaymentMode.name).all()
    ]

    form.purpose.choices = [(0, "All Purposes")] + [
        (p.id, p.name)
        for p in DonationPurpose.query.order_by(DonationPurpose.name).all()
    ]

    return render_template(
        "reports/donations.html",
        form=form
    )