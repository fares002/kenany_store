from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignUpForm, LoginForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)




@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        phone_number = form.phone_number.data
        address = form.address.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if password == confirm_password:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.phone_number = phone_number
            new_customer.address = address
            new_customer.password = confirm_password
            
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                print(e)
                flash('Account Not created!, Email already exists', 'danger')
            
            form.email.data = ''
            form.username.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            
            
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        customer = Customer.query.filter_by(email=email).first()
        
        if customer:
            if customer.verify_password(password):
                flash('Login Successful!', 'success')
                login_user(customer)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Email or Password', 'danger')
        else:
            flash('Invalid Email or Password', 'danger')
    
    return render_template('login.html', form=form)
     

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    customer = Customer.query.get(id)
    return render_template('profile.html' , customer=customer)



@auth.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    form = PasswordChangeForm()
    customer = Customer.query.get(id)
    if form.validate_on_submit():
        current_password = form.Current_Password.data
        new_password = form.New_Password.data
        confirm_new_password = form.Confirm_New_Password.data
        if new_password == confirm_new_password:
            if customer.verify_password(current_password):
                customer.password = new_password
                db.session.commit()
                flash('Password Changed Successfully!', 'success')
                return redirect(url_for('auth.profile', id=customer.id))
            else:
                flash('Invalid Current Password', 'danger')
        else:
            flash("Passwords don't match!", 'danger')
            
    return render_template('change_password.html', form=form)


    
