from flask import render_template
from flask_login import login_required
from flask import render_template, request, send_file
from io import BytesIO

from flask import send_file

from openpyxl import Workbook

from app.reports import reports
from app.reports.forms import DonationReportForm

from app.models import (
    Donation,
    Donor,
    PaymentMode,
    DonationPurpose
)


@reports.route("/donations", methods=["GET", "POST"])
@login_required
def donation_reports():

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

    query = Donation.query

    if form.validate_on_submit():

        if form.donor.data != 0:
            query = query.filter_by(donor_id=form.donor.data)

        if form.payment_mode.data != 0:
            query = query.filter_by(payment_mode_id=form.payment_mode.data)

        if form.purpose.data != 0:
            query = query.filter_by(purpose_id=form.purpose.data)

        if form.from_date.data:
            query = query.filter(
                Donation.donation_date >= form.from_date.data
            )

        if form.to_date.data:
            query = query.filter(
                Donation.donation_date <= form.to_date.data
            )

    donations = query.order_by(
        Donation.donation_date.desc()
    ).all()

    total_amount = sum(d.amount for d in donations)

    return render_template(
        "reports/donations.html",
        form=form,
        donations=donations,
        total_amount=total_amount
    )
@reports.route("/donations/export")
@login_required
def export_donations():

    donations = Donation.query.order_by(
        Donation.donation_date.desc()
    ).all()

    wb = Workbook()

    ws = wb.active

    ws.title = "Donation Report"

    ws.append([
        "Receipt No",
        "Date",
        "Donor",
        "Purpose",
        "Payment Mode",
        "Amount"
    ])

    for donation in donations:

        ws.append([
            donation.receipt_number,
            str(donation.donation_date),
            donation.donor.full_name,
            donation.purpose.name,
            donation.payment_mode.name,
            float(donation.amount)
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        download_name="Donation_Report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )@reports.route("/donations/export")
@login_required
def export_donations():

    donor = request.args.get("donor", type=int, default=0)
    payment_mode = request.args.get("payment_mode", type=int, default=0)
    purpose = request.args.get("purpose", type=int, default=0)

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    query = Donation.query

    if donor:
        query = query.filter(Donation.donor_id == donor)

    if payment_mode:
        query = query.filter(Donation.payment_mode_id == payment_mode)

    if purpose:
        query = query.filter(Donation.purpose_id == purpose)

    if from_date:
        query = query.filter(Donation.donation_date >= from_date)

    if to_date:
        query = query.filter(Donation.donation_date <= to_date)

    donations = query.order_by(
        Donation.donation_date.desc()
    ).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Donation Report"

    ws.append([
        "Receipt No",
        "Date",
        "Donor",
        "Purpose",
        "Payment Mode",
        "Amount"
    ])

    total = 0

    for donation in donations:

        ws.append([
            donation.receipt_number,
            donation.donation_date.strftime("%d-%m-%Y"),
            donation.donor.full_name,
            donation.purpose.name,
            donation.payment_mode.name,
            float(donation.amount)
        ])

        total += donation.amount

    ws.append([])
    ws.append(["", "", "", "", "Total", float(total)])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="Donation_Report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )