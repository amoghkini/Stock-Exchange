from instrument_registry.config.base_config import BaseConfig


class ProdConfig(BaseConfig):
    """
    Production configuration
    """

    DEBUG = False

    def __str__(self) -> str:
        return "Prod Config"

    def __repr__(self) -> str:
        return "Prod Config"
