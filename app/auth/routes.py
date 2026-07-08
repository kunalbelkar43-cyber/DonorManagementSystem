from flask import render_template, redirect, url_for, flash
from app.auth import auth
from app.auth.forms import LoginForm
from app.models.user import User
from flask_login import login_user, logout_user, login_required


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            return redirect(url_for("dashboard.index"))

        flash("Invalid username or password", "danger")

    return render_template(
        "auth/login.html",
        form=form
    )
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("auth.login"))