from .user_routes import init_app as init_user_routes
from .category_routes import init_app as init_category_routes

def init_app(app):
    
    init_user_routes(app)
    init_category_routes(app)
