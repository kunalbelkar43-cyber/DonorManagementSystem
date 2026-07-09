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
    if form.payment_mode.data != 1 and not form.transaction_reference.data:
            flash("Transaction Reference is required.", "danger")
            return render_template("donations/add.html", form=form)
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
@donations.route("/add", methods=["GET", "POST"])
@login_required
def view_donation(donation_id):

    donation = Donation.query.get_or_404(donation_id)

    return render_template(
        "donations/view.html",
        donation=donation
    )
from io import BytesIO

from flask import send_file

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
@donations.route("/receipt/<int:donation_id>")
@login_required
def print_receipt(donation_id):

    donation = Donation.query.get_or_404(donation_id)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Shree Laxmikeshav Pratishthan, Satara</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Donation Receipt",
            styles["Heading2"]
        )
    )

    data = [

        ["Receipt No", donation.receipt_no],

        ["Date", donation.donation_date.strftime("%d-%m-%Y")],

        ["Donor", donation.donor.full_name],

        ["Mobile", donation.donor.mobile],

        ["Amount", f"₹ {donation.amount}"],

        ["Payment Mode", donation.payment_mode.name],

        ["Purpose", donation.purpose.name],

        ["Remarks", donation.remarks or "-"]

    ]

    table = Table(data, colWidths=[150, 300])

    table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

        ("BOTTOMPADDING", (0,0), (-1,-1), 8),

        ("TOPPADDING", (0,0), (-1,-1), 8),

    ]))

    elements.append(table)

    elements.append(
        Paragraph("<br/><br/>Received By: ____________________", styles["Normal"])
    )

    elements.append(
        Paragraph("Authorized Signature: ____________________", styles["Normal"])
    )

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name=f"{donation.receipt_no}.pdf",
        mimetype="application/pdf"
    )