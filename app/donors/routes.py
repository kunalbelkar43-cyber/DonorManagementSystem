from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from flask import request
from sqlalchemy import or_

from app.extensions import db
from app.donors import donors
from app.donors.forms import DonorForm
from app.donors.utils import generate_donor_code
from app.models.donor import Donor
from app.models.donor_type import DonorType
from app.models.donation import Donation


@donors.route("/")
@login_required
def list_donors():

    page = request.args.get("page", 1, type=int)

    search = request.args.get("search", "").strip()

    query = Donor.query

    if search:

        query = query.filter(
            or_(
                Donor.donor_code.like(f"%{search}%"),
                Donor.full_name.like(f"%{search}%"),
                Donor.mobile.like(f"%{search}%")
            )
        )

    donors = query.order_by(
        Donor.id.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "donors/list.html",
        donors=donors,
        search=search
    )


@donors.route("/add", methods=["GET", "POST"])
@login_required
def add_donor():

    form = DonorForm()

    form.donor_type.choices = [
        (d.id, d.name)
        for d in DonorType.query.order_by(DonorType.name).all()
    ]

    if form.validate_on_submit():

        donor = Donor(
            donor_code=generate_donor_code(),
            full_name=form.full_name.data,
            mobile=form.mobile.data,
            email=form.email.data,
            dob=form.dob.data,
            pan_number=form.pan_number.data.upper() if form.pan_number.data else None,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data,
            donor_type_id=form.donor_type.data,
            notes=form.notes.data,
            status=form.status.data
        )

        db.session.add(donor)
        db.session.commit()

        flash("Donor added successfully.", "success")

        return redirect(url_for("donors.list_donors"))

    return render_template(
        "donors/add.html",
        form=form
    )

@donors.route("/edit/<int:donor_id>", methods=["GET", "POST"])
@login_required
def edit_donor(donor_id):

    donor = Donor.query.get_or_404(donor_id)

    form = DonorForm(obj=donor)

    form.donor_type.choices = [
        (d.id, d.name)
        for d in DonorType.query.order_by(DonorType.name).all()
    ]

    if form.validate_on_submit():

        donor.full_name = form.full_name.data
        donor.mobile = form.mobile.data
        donor.email = form.email.data
        donor.dob = form.dob.data
        donor.pan_number = (
            form.pan_number.data.upper()
            if form.pan_number.data
            else None
        )
        donor.address = form.address.data
        donor.city = form.city.data
        donor.state = form.state.data
        donor.pincode = form.pincode.data
        donor.donor_type_id = form.donor_type.data
        donor.notes = form.notes.data
        donor.status = form.status.data

        db.session.commit()

        flash("Donor updated successfully.", "success")

        return redirect(url_for("donors.list_donors"))

    return render_template(
        "donors/edit.html",
        form=form,
        donor=donor
    )

@donors.route("/delete/<int:donor_id>", methods=["POST"])
@login_required
def delete_donor(donor_id):

    donor = Donor.query.get_or_404(donor_id)

    db.session.delete(donor)

    db.session.commit()

    flash("Donor deleted successfully.", "success")

    return redirect(url_for("donors.list_donors"))

@donors.route("/view/<int:donor_id>")
@login_required
def view_donor(donor_id):

    donor = Donor.query.get_or_404(donor_id)

    donor_donations = Donation.query.filter_by(
        donor_id=donor.id
    ).order_by(Donation.donation_date.desc()).all()

    total_donations = len(donor_donations)

    total_amount = sum(d.amount for d in donor_donations)

    last_donation = donor_donations[0] if donor_donations else None

    return render_template(
        "donors/view.html",
        donor=donor,
        total_donations=total_donations,
        total_amount=total_amount,
        last_donation=last_donation
    )