from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Email
)


class DonorForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    mobile = StringField(
        "Mobile Number",
        validators=[
            DataRequired(),
            Length(min=10, max=15)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            Optional(),
            Email()
        ]
    )

    address = TextAreaField("Address")

    city = StringField("City")

    state = StringField("State")

    pincode = StringField("PIN Code")

    donor_type = SelectField(
        "Donor Type",
        coerce=int,
        validators=[DataRequired()]
    )

    notes = TextAreaField("Notes")

    status = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField("Save Donor")