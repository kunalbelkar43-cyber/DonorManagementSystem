from datetime import date
from sqlalchemy import func
from sqlalchemy import extract

from flask import render_template
from flask_login import login_required


from app import donors
from app.dashboard import dashboard

from app.models.donor import Donor
from app.models.donation import Donation
from app.extensions import db


@dashboard.route("/dashboard")
@login_required
def index():

    total_donors = Donor.query.count()

    total_donations = Donation.query.count()

    total_amount = (
        db.session.query(func.sum(Donation.amount))
        .scalar() or 0
    )

    today_donations = Donation.query.filter(
        Donation.donation_date == date.today()
    ).count()

    recent_donations = (
        Donation.query
        .order_by(Donation.id.desc())
        .limit(10)
        .all()
    )

        # Monetary Donations
    total_monetary = Donation.query.filter(
        Donation.donation_type == "MONETARY"
    ).count()

    # In-Kind Donations
    total_inkind = Donation.query.filter(
        Donation.donation_type == "IN_KIND"
    ).count()

    # This Month Donations
    today = date.today()

    this_month_donations = Donation.query.filter(
        func.month(Donation.donation_date) == today.month,
        func.year(Donation.donation_date) == today.year
    ).count()

    # Average Donation
    average_amount = db.session.query(
        func.avg(Donation.amount)
    ).filter(
        Donation.donation_type == "MONETARY"
    ).scalar() or 0

    today = date.today()

    birthday_donors = Donor.query.filter(
        extract("month", Donor.dob) == today.month,
        extract("day", Donor.dob) == today.day
    ).all()

    recent_activity = Donation.query.order_by(
    Donation.created_at.desc()
    ).limit(10).all()

    return render_template(
    "dashboard/index.html",

    total_donors=total_donors,
    total_donations=total_donations,
    total_amount=total_amount,
    today_donations=today_donations,

    total_monetary=total_monetary,
    total_inkind=total_inkind,
    this_month_donations=this_month_donations,
    average_amount=average_amount,

    recent_donations=recent_donations,

    birthday_donors=birthday_donors
)

