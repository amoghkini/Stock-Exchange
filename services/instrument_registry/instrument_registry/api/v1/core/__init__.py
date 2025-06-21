from flask import Blueprint

instrument_registry_home = Blueprint(
    "instrument_registry_home",
    __name__,
    url_prefix="/api/v1",
)