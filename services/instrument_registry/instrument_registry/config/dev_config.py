from instrument_registry.config.base_config import BaseConfig


class DevConfig(BaseConfig):
    """
    Development configuration
    """
    
    DEBUG = True
    
    def __str__(self) -> str:
        return "Dev Config"

    def __repr__(self) -> str:
        return "Dev Config"