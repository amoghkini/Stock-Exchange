from flask.views import MethodView


class InstrumentAPI(MethodView):
    
    def get(self):
        return {"status": "ok"}
    
    def post(self):
        pass