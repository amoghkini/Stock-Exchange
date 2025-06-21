from flask.views import MethodView



class HomeAPI(MethodView):
    """
    The home API endpoint.
    """
    def get(self):
        return {"status": "ok"}


class HealthCheckAPI(MethodView):
    """
    The health check API endpoint.
    """
    def get(self):
        return {"status": "ok"}
