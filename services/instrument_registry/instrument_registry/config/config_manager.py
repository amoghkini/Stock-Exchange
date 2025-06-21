import os
from typing import Optional, Type

from dotenv import load_dotenv

from instrument_registry.config.base_config import BaseConfig
from instrument_registry.config.dev_config import DevConfig
from instrument_registry.config.prod_config import ProdConfig
from instrument_registry.config.test_config import TestConfig


DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


CONFIG_MAPPING: dict[str, Type[BaseConfig]] = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig,
}

if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)
    

class ConfigManager:
    """
    A utility class to manage application configuration based on the environment.
    """

    @staticmethod
    def get_config(env: Optional[str] = None) -> BaseConfig:
        """
        Retrieve the configuration instance for the given environment.

        Args:
            env (Optional[str]): The environment name (e.g., 'dev', 'prod', 'test').
                                 If None, reads from the ENV environment variable.

        Returns:
            BaseConfig: An instance of the configuration class corresponding to the environment.

        Raises:
            KeyError: If the environment is not in CONFIG_MAPPING.
        """
        if not env:
            env = ConfigManager.get_env()
        if env not in CONFIG_MAPPING:
            raise KeyError(
                f"Invalid environment '{env}'. Expected one of: {list(CONFIG_MAPPING.keys())}"
            )
        return CONFIG_MAPPING[env]()

    @staticmethod
    def get_env() -> str:
        """
        Fetch the environment name from the 'ENV' environment variable.
        Defaults to 'dev' if not set.

        Returns:
            str: The environment name.
        """
        return os.environ.get("ENV", "dev")
