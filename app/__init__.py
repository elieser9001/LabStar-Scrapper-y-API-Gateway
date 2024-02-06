from flask import Flask

def create_app():
    app = Flask(__name__)
        
    from .endpoints import clients_checkin
    app.register_blueprint(clients_checkin.bp)

    return app
