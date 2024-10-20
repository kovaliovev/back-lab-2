from .user_routes import init_app as init_user_routes

def init_app(app):
    
    init_user_routes(app)
