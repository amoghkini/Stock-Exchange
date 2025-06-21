from instrument_registry.api.v1.core import instrument_registry_home
from instrument_registry.api.v1.core.views import HomeAPI, HealthCheckAPI


routes = [
    (
        (instrument_registry_home),
        ("/home", "home_api", HomeAPI),
        ("/health-check", "health_check_api", HealthCheckAPI),
    )
]
