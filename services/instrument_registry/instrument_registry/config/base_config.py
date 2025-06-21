class BaseConfig:
    
    ROUTES = [
        "instrument_registry.api.v1.core.routes.routes",
    ]
    
    BLUEPRINTS = [
        'core.views',
    ]