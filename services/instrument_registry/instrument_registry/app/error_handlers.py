from flask import Flask, jsonify
from http import HTTPStatus
from typing import Any, Tuple


class ErrorHandler:
    """ Flask error handler class """
    
    def __init__(self, app: Flask) -> None:
        self.app = app

    def __handle_400(self, e: Exception) -> Tuple[Any, int]:
        return jsonify(
            {"error": "Bad Request", "message": str(e)}
        ), HTTPStatus.BAD_REQUEST

    def __handle_403(self, e: Exception) -> Tuple[Any, int]:
        return jsonify({"error": "Forbidden", "message": str(e)}), HTTPStatus.FORBIDDEN

    def __handle_404(self, e: Exception) -> Tuple[Any, int]:
        return jsonify({"error": "Not Found", "message": str(e)}), HTTPStatus.NOT_FOUND

    def __handle_405(self, e: Exception) -> Tuple[Any, int]:
        return jsonify(
            {"error": "Method Not Allowed", "message": str(e)}
        ), HTTPStatus.METHOD_NOT_ALLOWED

    def __handle_500(self, e: Exception) -> Tuple[Any, int]:
        return jsonify(
            {"error": "Internal Server Error", "message": str(e)}
        ), HTTPStatus.INTERNAL_SERVER_ERROR

    def register_400_error(self) -> None:
        self.app.register_error_handler(HTTPStatus.BAD_REQUEST, self.__handle_400)

    def register_403_error(self) -> None:
        self.app.register_error_handler(HTTPStatus.FORBIDDEN, self.__handle_403)

    def register_404_error(self) -> None:
        self.app.register_error_handler(HTTPStatus.NOT_FOUND, self.__handle_404)

    def register_405_error(self) -> None:
        self.app.register_error_handler(HTTPStatus.METHOD_NOT_ALLOWED, self.__handle_405)

    def register_500_error(self) -> None:
        self.app.register_error_handler(
            HTTPStatus.INTERNAL_SERVER_ERROR, self.__handle_500
        )

    def register_all(self) -> None:
        self.register_400_error()
        self.register_403_error()
        self.register_404_error()
        self.register_405_error()
        self.register_500_error()
