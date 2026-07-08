from flask import render_template
from flask_login import login_required

from app.donations import donations

@donations.route("/")
@login_required
def list_donations():
    return render_template("donations/list.html")