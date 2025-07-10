from instrument_registry.api.v1.instruments import instrument_registry
from instrument_registry.api.v1.instruments.views import InstrumentAPI


routes = [
    (
        (instrument_registry),
        ("/", "instrument_api", InstrumentAPI),
    )
]
