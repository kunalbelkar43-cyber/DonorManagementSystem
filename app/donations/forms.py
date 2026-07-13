from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    StringField,
    DecimalField,
    DateField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional
)


class DonationForm(FlaskForm):

    # ==================================================
    # Common Information
    # ==================================================

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

    purpose = SelectField(
        "Donation Purpose",
        coerce=int,
        validators=[DataRequired()]
    )

    donation_type = SelectField(
        "Donation Type",
        choices=[
            ("MONETARY", "Monetary Donation"),
            ("IN_KIND", "In-Kind Donation")
        ],
        validators=[DataRequired()]
    )

    # ==================================================
    # Monetary Donation
    # ==================================================

    amount = DecimalField(
        "Amount",
        places=2,
        validators=[Optional()],
        render_kw={"placeholder": "Enter Donation Amount"}
    )

    payment_mode = SelectField(
        "Payment Mode",
        coerce=int,
        validators=[Optional()]
    )

    transaction_reference = StringField(
        "Transaction Reference",
        validators=[Optional()],
        render_kw={"placeholder": "Transaction Reference"}
    )

    bank_name = StringField(
        "Bank Name",
        validators=[Optional()],
        render_kw={"placeholder": "Bank Name"}
    )

    account_number = StringField(
        "Account Number",
        validators=[Optional()],
        render_kw={"placeholder": "Account Number"}
    )

    ifsc_code = StringField(
        "IFSC Code",
        validators=[Optional()],
        render_kw={"placeholder": "IFSC Code"}
    )

    cheque_number = StringField(
        "Cheque Number",
        validators=[Optional()],
        render_kw={"placeholder": "Cheque Number"}
    )

    cheque_date = DateField(
        "Cheque Date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    utr_number = StringField(
        "UPI Transaction Number (UTR)",
        validators=[Optional()],
        render_kw={"placeholder": "UPI UTR Number"}
    )

    # ==================================================
    # In-Kind Donation
    # ==================================================

    item_name = StringField(
        "Item Name",
        validators=[Optional()],
        render_kw={"placeholder": "Item Name"}
    )

    category = StringField(
        "Category",
        validators=[Optional()],
        render_kw={"placeholder": "Category"}
    )

    quantity = DecimalField(
        "Quantity",
        places=2,
        validators=[Optional()],
        render_kw={"placeholder": "Quantity"}
    )

    estimated_value = DecimalField(
        "Estimated Value",
        places=2,
        validators=[Optional()],
        render_kw={"placeholder": "Estimated Value"}
    )

    # ==================================================
    # Common Remarks
    # ==================================================

    remarks = TextAreaField(
        "Remarks",
        validators=[Optional()],
        render_kw={
            "rows": 3,
            "placeholder": "Additional Remarks"
        }
    )

    # ==================================================
    # Submit Button
    # ==================================================

    submit = SubmitField("Save / Update Donation")