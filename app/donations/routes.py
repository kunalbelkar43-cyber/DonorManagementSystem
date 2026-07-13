from io import BytesIO

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
)

from flask_login import (
    login_required,
    current_user,
)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from app.extensions import db
from app.donations import donations
from app.donations.forms import DonationForm
from app.donations.utils import generate_receipt_number

from app.models.donor import Donor
from app.models.payment_mode import PaymentMode
from app.models.donation_purpose import DonationPurpose
from app.models.donation import Donation


# ===================================================
# Add Donation
# ===================================================

@donations.route("/add", methods=["GET", "POST"])
@login_required
def add_donation():

    form = DonationForm()

    form.donor.choices = [

    (
        d.id,
        f"{d.donor_code} | {d.full_name} | {d.mobile}"
    )

    for d in Donor.query.order_by(Donor.full_name).all()

]

    form.purpose.choices = [
        (p.id, p.name)
        for p in DonationPurpose.query.order_by(
            DonationPurpose.name
        ).all()
    ]

    form.payment_mode.choices = [
        (p.id, p.name)
        for p in PaymentMode.query.order_by(
            PaymentMode.name
        ).all()
    ]

    if form.validate_on_submit():

        # =====================================
        # Validation
        # =====================================

        if form.donation_type.data == "MONETARY":

            if not form.amount.data:
                flash("Amount is required.", "danger")
                return render_template(
                    "donations/add.html",
                    form=form
                )

            payment = PaymentMode.query.get(
                form.payment_mode.data
            )

            if payment:

                mode = payment.name.lower()

                if mode == "bank":

                    if not form.bank_name.data:
                        flash("Bank Name is required.", "danger")
                        return render_template(
                            "donations/add.html",
                            form=form
                        )

                    if not form.account_number.data:
                        flash("Account Number is required.", "danger")
                        return render_template(
                            "donations/add.html",
                            form=form
                        )

                    if not form.ifsc_code.data:
                        flash("IFSC Code is required.", "danger")
                        return render_template(
                            "donations/add.html",
                            form=form
                        )

                elif mode == "cheque":

                    if not form.cheque_number.data:
                        flash("Cheque Number is required.", "danger")
                        return render_template(
                            "donations/add.html",
                            form=form
                        )

                elif mode == "upi":

                    if not form.utr_number.data:
                        flash("UTR Number is required.", "danger")
                        return render_template(
                            "donations/add.html",
                            form=form
                        )

        else:

            if not form.item_name.data:
                flash("Item Name is required.", "danger")
                return render_template(
                    "donations/add.html",
                    form=form
                )

        # =====================================
        # Create Donation
        # =====================================

        donation = Donation(

            receipt_no=generate_receipt_number(),

            donor_id=form.donor.data,

            donation_date=form.donation_date.data,

            donation_type=form.donation_type.data,

            purpose_id=form.purpose.data,

            remarks=form.remarks.data,

            received_by=current_user.id

        )

        # =====================================
        # Monetary Donation
        # =====================================

        if form.donation_type.data == "MONETARY":

            donation.amount = form.amount.data

            donation.payment_mode_id = form.payment_mode.data

            donation.transaction_reference = form.transaction_reference.data

            donation.bank_name = form.bank_name.data

            donation.account_number = form.account_number.data

            donation.ifsc_code = form.ifsc_code.data

            donation.cheque_number = form.cheque_number.data

            donation.cheque_date = form.cheque_date.data

            donation.utr_number = form.utr_number.data

        # =====================================
        # In-Kind Donation
        # =====================================

        else:

            donation.amount = form.estimated_value.data or 0

            donation.payment_mode_id = None

            donation.transaction_reference = None

            donation.bank_name = None

            donation.account_number = None

            donation.ifsc_code = None

            donation.cheque_number = None

            donation.cheque_date = None

            donation.utr_number = None

            donation.item_name = form.item_name.data

            donation.category = form.category.data

            donation.quantity = form.quantity.data

            donation.estimated_value = form.estimated_value.data

        db.session.add(donation)
        db.session.commit()

        flash("Donation recorded successfully.", "success")

        return redirect(
            url_for(
                "donations.view_donation",
                donation_id=donation.id
            )
        )

    return render_template(
        "donations/add.html",
        form=form
    )


# ===================================================
# Donation List
# ===================================================

@donations.route("/")
@login_required
def list_donations():

    donations_list = Donation.query.order_by(
        Donation.id.desc()
    ).all()

    return render_template(
        "donations/list.html",
        donations=donations_list
    )


# ===================================================
# View Donation
# ===================================================

@donations.route("/view/<int:donation_id>")
@login_required
def view_donation(donation_id):

    donation = Donation.query.get_or_404(
        donation_id
    )

    return render_template(
        "donations/view.html",
        donation=donation
    )


# ===================================================
# Edit Donation
# ===================================================

@donations.route("/edit/<int:donation_id>", methods=["GET", "POST"])
@login_required
def edit_donation(donation_id):

    donation = Donation.query.get_or_404(donation_id)

    form = DonationForm(obj=donation)

    # -------------------------
    # Dropdowns
    # -------------------------

    form.donor.choices = [
        (d.id, f"{d.donor_code} - {d.full_name}")
        for d in Donor.query.order_by(Donor.full_name).all()
    ]

    form.purpose.choices = [
        (p.id, p.name)
        for p in DonationPurpose.query.order_by(DonationPurpose.name).all()
    ]

    form.payment_mode.choices = [
        (p.id, p.name)
        for p in PaymentMode.query.order_by(PaymentMode.name).all()
    ]

    # -------------------------
    # Save Changes
    # -------------------------

    if form.validate_on_submit():

        donation.donor_id = form.donor.data
        donation.donation_date = form.donation_date.data
        donation.donation_type = form.donation_type.data
        donation.purpose_id = form.purpose.data
        donation.remarks = form.remarks.data

        # =============================
        # Monetary Donation
        # =============================

        if form.donation_type.data == "MONETARY":

            donation.amount = form.amount.data

            donation.payment_mode_id = form.payment_mode.data

            donation.transaction_reference = form.transaction_reference.data

            donation.bank_name = form.bank_name.data

            donation.account_number = form.account_number.data

            donation.ifsc_code = form.ifsc_code.data

            donation.cheque_number = form.cheque_number.data

            donation.cheque_date = form.cheque_date.data

            donation.utr_number = form.utr_number.data

            # Clear In-Kind fields

            donation.item_name = None
            donation.category = None
            donation.quantity = None
            donation.estimated_value = None

        # =============================
        # In-Kind Donation
        # =============================

        else:

            donation.item_name = form.item_name.data

            donation.category = form.category.data

            donation.quantity = form.quantity.data

            donation.estimated_value = form.estimated_value.data

            donation.amount = form.estimated_value.data or 0

            # Clear Monetary fields

            donation.payment_mode_id = None

            donation.transaction_reference = None

            donation.bank_name = None

            donation.account_number = None

            donation.ifsc_code = None

            donation.cheque_number = None

            donation.cheque_date = None

            donation.utr_number = None

        db.session.commit()

        flash("Donation updated successfully.", "success")

        return redirect(
            url_for(
                "donations.view_donation",
                donation_id=donation.id
            )
        )

    return render_template(
        "donations/edit.html",
        form=form,
        donation=donation
    )

# ===================================================
# Delete Donation
# ===================================================

@donations.route("/delete/<int:donation_id>", methods=["POST"])
@login_required
def delete_donation(donation_id):

    donation = Donation.query.get_or_404(
        donation_id
    )

    db.session.delete(donation)
    db.session.commit()

    flash(
        "Donation deleted successfully.",
        "success"
    )

    return redirect(
        url_for("donations.list_donations")
    )


# ===================================================
# Print Receipt
# ===================================================

@donations.route("/receipt/<int:donation_id>")
@login_required
def print_receipt(donation_id):

    donation = Donation.query.get_or_404(
        donation_id
    )

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

    payment_mode = "-"

    if donation.payment_mode:
        payment_mode = donation.payment_mode.name

    data = [

        ["Receipt No", donation.receipt_no],

        ["Date", donation.donation_date.strftime("%d-%m-%Y")],

        ["Donor", donation.donor.full_name],

        ["Donation Type", donation.donation_type],

        ["Purpose", donation.purpose.name],

        ["Amount", f"₹ {donation.amount}"],

        ["Payment Mode", payment_mode],

        ["Remarks", donation.remarks or "-"]

    ]

    table = Table(
        data,
        colWidths=[170, 300]
    )

    table.setStyle(TableStyle([

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

        ("TOPPADDING", (0, 0), (-1, -1), 8)

    ]))

    elements.append(table)

    elements.append(
        Paragraph(
            "<br/><br/>Received By: ____________________",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Authorized Signature: ____________________",
            styles["Normal"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name=f"{donation.receipt_no}.pdf",
        mimetype="application/pdf"
    )