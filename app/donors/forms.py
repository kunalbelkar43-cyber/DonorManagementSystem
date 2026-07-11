from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField
)
from wtforms.fields import DateField
from wtforms.fields import DateField
from wtforms.validators import Length, Optional

dob = DateField(
    "Date of Birth",
    format="%Y-%m-%d"
)
import re
from wtforms import ValidationError

def validate_pan_number(form, field):
    if field.data:
        pan = field.data.upper()

        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

        if not re.match(pattern, pan):
            raise ValidationError(
                "Enter a valid PAN number (Example: ABCDE1234F)."
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
    dob = DateField(
    "Date of Birth",
    format="%Y-%m-%d",
    validators=[],
)
    pan_number = StringField(
    "PAN Card Number",
    validators=[
        Optional(),
        Length(min=10, max=10)
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