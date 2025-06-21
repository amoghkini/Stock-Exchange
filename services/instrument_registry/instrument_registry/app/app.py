import logging
from typing import Any, Tuple, Union, Callable
from flask import Flask, Blueprint
from flask.views import MethodView

from instrument_registry.app.build_utils import BuildUtils
from instrument_registry.app.exceptions import NoRouteModuleFoundException
from instrument_registry.app.error_handlers import ErrorHandler
from instrument_registry.app.lifecycle import AppLifeCycle
from instrument_registry.config.config_manager import ConfigManager


class AppBuilder:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)
        
        self.app_config = ConfigManager.get_config()
        self.app.config.from_object(self.app_config)
        
    def build(
        self, 
        app_module_name: str,
        **kwargs: Any
    ) -> Flask:
        """
        The main method to build the Flask application.
        """
        logging.info("Building %s", app_module_name)

        # self.__server_bootup_operations()

        # self.__set_path()
        # self.__bind_extensions()
        self.__register_routes()
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
    
    def __register_routes(self) -> None:
        """
        Register routes with the Flask application
        
        Raises:
            NoRouteModuleFoundException: If no route module is found
        """
        logging.info("Registering routes")
        
        url_modules: list[str] = self.app.config.get("ROUTES", [])

        for url_module in url_modules:

            logging.info("Importing %s", url_module)

            module, route_name = BuildUtils.get_imported_stuff_by_path(url_module)
            logging.info("Registering module %s", module)
            logging.info("Registering route %s", route_name)

            if hasattr(module, route_name):
                routes = getattr(module, route_name)
                self.__setup_routes(routes)
            else:
                logging.error("No %s url module found", route_name)
                raise NoRouteModuleFoundException(f"No {route_name} url module found")
            
        logging.info("Finished registering blueprints and url routes")

    def __setup_routes(
        self,
        routes: list[
            Tuple[
                Union[Blueprint, Tuple[Blueprint, Any]],
                *Tuple[str, Union[str, None], Any]  # (pattern, [endpoint], view)
            ]
        ],
    ) -> None:
        """
        Set up routes for the given list of blueprints and route definitions.

        Args:
            routes (List[Tuple[Blueprint | Tuple[Blueprint, Any], ...]]): A list where each item
                contains a blueprint followed by one or more route tuples.
                Each route tuple is either:
                - (pattern: str, view: Any)
                - (pattern: str, endpoint: str, view: Any)
        """
        for route in routes:
            blueprint, rules = route[0], route[1:]
            logging.info("Setting up blueprint %s", blueprint)

            for item in rules:
                pattern: str
                endpoint: Union[str, None]
                view: Union[Callable, MethodView]
                
                if len(item) == 3:
                    pattern, endpoint, view = item  # type: ignore
                else:
                    pattern, view = item  # type: ignore
                    endpoint = None

                logging.info(
                    "Plugging URL pattern: %s into view: %s at endpoint: %s",
                    pattern,
                    view.view_class.__name__
                    if hasattr(view, "func_name")  
                    else view.__name__,
                    endpoint or getattr(view, "func_name", "Unknown"),
                )  # type: ignore

                if isinstance(blueprint, tuple):
                    blueprint = blueprint[0]

                blueprint.add_url_rule(
                    pattern,
                    endpoint or view.func_name,
                    view_func=view if hasattr(view, "func_name") else view.as_view(endpoint),
                )

            if not BuildUtils.check_for_registered_blueprint(self.app, blueprint):
                logging.info("Now registering '%s' as blueprint", blueprint.name)
                self.app.register_blueprint(blueprint)
                
    