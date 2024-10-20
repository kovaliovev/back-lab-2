from .user_routes import init_app as init_user_routes
from .category_routes import init_app as init_category_routes
from .record_routes import init_app as init_record_routes

def init_app(app):
    
    init_user_routes(app)
    init_category_routes(app)
    init_record_routes(app)
