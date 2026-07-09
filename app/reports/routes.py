from flask import render_template
from flask_login import login_required

from app.reports import reports


@reports.route("/donations")
@login_required
def donation_report():

    return render_template("reports/donations.html")