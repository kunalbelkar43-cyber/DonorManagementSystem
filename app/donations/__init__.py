from flask import Blueprint

donations = Blueprint(
    "donations",
    __name__,
    url_prefix="/donations"
)

from app.donations import routes