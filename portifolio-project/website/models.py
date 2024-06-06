from . import db, bcrypt
from datetime import datetime
from flask_login import UserMixin

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, str(self.id), self.__dict__)

class Customer(Base, UserMixin):
    __tablename__ = 'customers'
    username = db.Column(db.String(150), unique=True, index=True, nullable=False)
    email = db.Column(db.String(150), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    profile_pic = db.Column(db.String(150), default='default.jpg', nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    cart_items = db.relationship('Cart', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Customer {self.username}>'

class Product(Base):
    __tablename__ = 'products'
    product_name = db.Column(db.String(150), unique=True, nullable=False, index=True)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(150), nullable=True)
    in_stock = db.Column(db.Integer, default=1)
    image = db.Column(db.String(1000), nullable=True)
    flash_sale = db.Column(db.Boolean, default=False)
    cart_items = db.relationship('Cart', backref='product', lazy=True)
    orders = db.relationship('Order', backref='product', lazy=True)
    
    def __str__(self):
        return f'<Product {self.product_name}>'

class Cart(Base):
    __tablename__ = 'carts'
    quantity = db.Column(db.Integer, default=1)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __str__(self):
        return f'<Cart {self.id}>'

class Order(Base):
    __tablename__ = 'orders'
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(150), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __str__(self):
        return f'<Order {self.id}>'



    
    


