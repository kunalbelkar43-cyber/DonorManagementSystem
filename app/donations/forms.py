from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateField,
    DecimalField,
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    NumberRange,
    Optional,
    Length
)


class DonationForm(FlaskForm):

    donor = SelectField(
        "Donor",
        coerce=int,
        validators=[DataRequired()]
    )

    donation_date = DateField(
        "Donation Date",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    amount = DecimalField(
        "Amount",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    payment_mode = SelectField(
        "Payment Mode",
        coerce=int,
        validators=[DataRequired()]
    )

    purpose = SelectField(
        "Donation Purpose",
        coerce=int,
        validators=[DataRequired()]
    )

    transaction_reference = StringField(
        "Transaction Reference",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    remarks = TextAreaField("Remarks")

    submit = SubmitField("Save Donation")