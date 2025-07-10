from flask import Blueprint

instrument_registry = Blueprint(
    "instrument_registry",
    __name__,
    url_prefix="/api/v1/instruments",
)
