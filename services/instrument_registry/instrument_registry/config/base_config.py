import os


class BaseConfig:
    """
    Base configuration class.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///"
        + os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "..", "data", "dev.db"
        ),
    )
    ROUTES: list[str] = [
        "instrument_registry.api.v1.core.routes.routes",
    ]
    
    BLUEPRINTS: list[str] = [
        "instrument_registry.api.v1.core.instrument_registry_home",
    ]
    
    EXTENSIONS: list[str] = [
        # "instrument_registry.app.extensions.db",
    ]
    
    MIDDLEWARE: list[str] = []
