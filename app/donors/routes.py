from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.donors import donors
from app.donors.forms import DonorForm
from app.donors.utils import generate_donor_code
from app.models.donor import Donor
from app.models.donor_type import DonorType


@donors.route("/")
@login_required
def list_donors():

    donor_list = Donor.query.order_by(Donor.id.desc()).all()

    return render_template(
        "donors/list.html",
        donors=donor_list
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