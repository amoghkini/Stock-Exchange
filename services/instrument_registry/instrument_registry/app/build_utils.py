from typing import Any, Tuple
from werkzeug.utils import import_string

from flask import Flask, Blueprint

class BuildUtils:
    
    @staticmethod
    def get_imported_stuff_by_path(
        path: str
    ) -> Tuple[Any, str]:
        """
        Import module and get object by its path.

        Args:
            path (str): Path to the module and object.

        Returns:
            Tuple[Any, str]: A tuple containing the imported module and object name.

        Example:
            >>> main = Main(config)
            >>> module, object_name = BuildUtils.get_imported_stuff_by_path('my_module.my_object_path')
        """
        module_name: str
        object_name: str

        module_name, object_name = path.rsplit(".", 1)
        module: Any = import_string(module_name)
        return module, object_name

    @staticmethod
    def check_for_registered_blueprint(
        app: Flask,
        blueprint: Blueprint
    ) -> bool:
        """
        Check if the given blueprint is already registered in the app.

        Args:
            app (Flask): The Flask app instance.
            blueprint (Blueprint): The blueprint to check.

        Returns:
            bool: True if the blueprint is already registered, False otherwise.
        """
        found: bool = False
        for name in [str(x) for x in app.blueprints]:
            if blueprint.__class__.__name__.split(".")[-1] in name:
                found = True
        return found