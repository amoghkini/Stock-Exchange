from typing import Any
from flask import Flask

from instrument_registry.app.error_handlers import ErrorHandler
from instrument_registry.app.lifecycle import AppLifeCycle


class AppBuilder:
    
    def __init__(
        self, 
        config_path="instrument_registry.config.dev.DevConfig"
    ) -> None:
        self.config_path = config_path
    
    def build(
        self, 
        app_module_name: str,
        **kwargs: Any
    ) -> Flask:
        """
        The main method to build the Flask application.
        """
        self.app = Flask(__name__)
        
        # self.app.config.from_object(self.app_config)
        # self.app.config["VERBOSE"] = is_verbose()

        # self.__server_bootup_operations()

        # self.__set_path()
        # self.__bind_extensions()
        # self.__register_routes()
        # self.__load_models()
        # self.__load_views()
        # self.__register_context_processors()
        # self.__register_templalte_filters()
        # self.__register_middlewares()

        # Instantiate AppLifecycle with the app instance
        lifecycle_manager = AppLifeCycle(self.app)
        lifecycle_manager.register_before_request()
        lifecycle_manager.register_after_request()
        lifecycle_manager.register_teardown_appcontext()

        # Instantiate ErrorHandler with the app instance
        error_handler_manager = ErrorHandler(self.app)
        error_handler_manager.register_400_error()
        error_handler_manager.register_403_error()
        error_handler_manager.register_404_error()
        error_handler_manager.register_405_error()
        error_handler_manager.register_500_error()
        return self.app