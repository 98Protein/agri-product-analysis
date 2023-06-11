from .admin import bp as admin_bp
from .category import bp as category_bp
from .compare import bp as compare_bp
from .monitor import bp as monitor_bp
from .predict import bp as predict_bp
from .product import bp as product_bp
from .region import bp as region_bp
from .sell import bp as sell_bp


def init_app(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(monitor_bp)
    app.register_blueprint(region_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(sell_bp)
    app.register_blueprint(predict_bp)
