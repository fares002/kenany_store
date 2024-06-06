from flask import Flask , url_for,  render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_database():
    db.create_all()
    print('Created Database!')
 

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kenany_user:yourpassword@localhost/kenany_store_test'
    db.init_app(app)
    
    
    @app.errorhandler(404)
    def page_not_found(erorr):
        return render_template('404.html'), 404
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))
    

    
    from .views import views
    from .admin import admin
    from .auth import auth
    from .models import Customer, Product, Order,  Cart
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        create_database()
    
    return app