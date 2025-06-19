
import logging
import time
import uuid
from typing import Any

from flask import Flask, request, g


class AppLifeCycle:
    """ Flask application lifecycle class """
    
    def __init__(
        self, 
        app: Flask
    ) -> None:
        self.app = app
        
    def __before_request(self) -> None:
        
        g.start_time = time.perf_counter()
        g.request_id = str(uuid.uuid4())

        request_id = g.request_id
        method = request.method
        path = request.path
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "unknown")

        if path.startswith("/static") or path in ["/health", "/ping"]:
            g.skip_logging = True
            return

        g.skip_logging = False

        logging.info(
            "Started %s %s from %s - UA: %s",
            method,
            path,
            ip,
            user_agent,
            extra={"request_id": request_id},
        )

    def __after_request(self, response: Any) -> Any:
        if getattr(g, "skip_logging", False):
            return response

        duration = time.perf_counter() - g.start_time
        response_size = len(response.get_data(as_text=False))

        logging.info(
            "Completed %s %s with status %s in %.3fs, size: %d bytes",
            request.method,
            request.path,
            response.status_code,
            duration,
            response_size,
            extra={"request_id": g.request_id},
        )

        response.headers["X-Request-ID"] = g.request_id
        return response

    def __teardown_appcontext(self, exception: Any) -> None:
        if exception and not getattr(g, "skip_logging", False):
            logging.error(
                "Exception during request: %s",
                str(exception),
                extra={"request_id": getattr(g, "request_id", "-")},
            )

    def register_before_request(self) -> None:
        """ Register before request hook """
        self.app.before_request(self.__before_request)

    def register_after_request(self) -> None:
        """ Register after request hook """
        self.app.after_request(self.__after_request)

    def register_teardown_appcontext(self) -> None:
        """ Register teardown appcontext hook """
        self.app.teardown_appcontext(self.__teardown_appcontext)

    def register_all(self) -> None:
        """ Register all hooks """
        self.register_before_request()
        self.register_after_request()
        self.register_teardown_appcontext()
