from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DateField
from wtforms.validators import Optional


class DonationReportForm(FlaskForm):

    from_date = DateField(
        "From Date",
        validators=[Optional()]
    )

    to_date = DateField(
        "To Date",
        validators=[Optional()]
    )

    donor = SelectField(
        "Donor",
        coerce=int,
        validators=[Optional()]
    )

    payment_mode = SelectField(
        "Payment Mode",
        coerce=int,
        validators=[Optional()]
    )

    purpose = SelectField(
        "Purpose",
        coerce=int,
        validators=[Optional()]
    )

    submit = SubmitField("Search")