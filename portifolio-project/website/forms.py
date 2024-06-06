from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField ,PasswordField, SubmitField, BooleanField, EmailField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from flask_wtf.file import FileField

class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email = EmailField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Sign Up')

    
    
class LoginForm(FlaskForm):
    email= EmailField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')
    
    
class PasswordChangeForm(FlaskForm):
    Current_Password=PasswordField(label='Current Password' , validators=[DataRequired(), Length(min=6)])
    New_Password=PasswordField(label='New_Password' , validators=[DataRequired(), Length(min=6)])
    Confirm_New_Password=PasswordField(label='Confirm_New_Password' , validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label='Change Password')
    
    
class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')
    
    
class OrdersForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')])
    submit = SubmitField('Update status')