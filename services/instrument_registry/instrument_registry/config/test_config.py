from instrument_registry.config.base_config import BaseConfig


class TestConfig(BaseConfig):
    """
    Test configuration
    """

    DEBUG = False

    def __str__(self) -> str:
        return "Test Config"

    def __repr__(self) -> str:
        return "Test Config"
