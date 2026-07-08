from flask import Blueprint

donors = Blueprint(
    "donors",
    __name__,
    url_prefix="/donors"
)

from app.donors import routes