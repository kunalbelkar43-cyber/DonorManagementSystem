from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import date
from app.extensions import db

from app.dashboard import dashboard
from app.models.donor import Donor
from app.models.donation import Donation

@dashboard.route("/dashboard")
@login_required
def index():

    total_donors = Donor.query.count()

    total_donations = Donation.query.count()

    total_amount = db.session.query(
        func.sum(Donation.amount)
    ).scalar()

    if total_amount is None:
        total_amount = 0

    today_donations = Donation.query.filter(
        Donation.donation_date == date.today()
    ).count()

    recent_donations = Donation.query.order_by(
        Donation.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/index.html",
        total_donors=total_donors,
        total_donations=total_donations,
        total_amount=total_amount,
        today_donations=today_donations,
        recent_donations=recent_donations,
        user=current_user
    )