from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import SignUpForm
from .models import Product, Cart, Order
from . import db
from flask_login import login_required, current_user
from intasend import APIService

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = "ISPubKey_test_8ff503c9-81b7-4144-88df-4ce1d65a3cdb"
API_TOKEN = "ISSecretKey_test_2d424435-3893-4eb4-ae0f-e0a7e8736288"

@views.route('/home')
def home():
    items = Product.query.all()
    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_id=current_user.id).all()
                           if current_user.is_authenticated else [])



@views.route('/')
def base():
    items = Product.query.filter_by(flash_sale=True).all()
    return render_template('landing_page.html', items=items, cart=Cart.query.filter_by(customer_id=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/add_to_cart/<int:id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(id):
    item_to_add = Product.query.get(id) #get item to add to cart
    item_exists = Cart.query.filter_by(product_id=id, customer_id=current_user.id).first() #check if item already exists in cart for user
    if item_exists:
        try:
            item_exists.quantity += 1
            db.session.commit()
            flash('item added to cart successfully!', 'success')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash(f'An error occurred while adding item to cart', 'danger')
            return redirect(request.referrer)
    
    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_id = item_to_add.id
    new_cart_item.customer_id = current_user.id
    
    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'added to cart successfully!', 'success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        flash(f'An error occurred while adding item to cart', 'danger')
        return redirect(request.referrer)



@views.route('/cart', methods=['POST', 'GET'])
@login_required
def cart():
    cart_items = []
    amount = 0
    total = 0
    if current_user.is_authenticated:
        id = current_user.id
        cart_items = Cart.query.filter_by(customer_id=id).all()
        for item in cart_items:
            amount += item.product.current_price * item.quantity
            total = amount + 1000
        print(current_user.id, cart_items, amount, total)
    return render_template('cart.html', cart_items=cart_items , amount=amount, total=total)



@views.route('/delete_cart_item/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_cart_item(id):
    item_to_delete = Cart.query.get(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        # flash('item deleted successfully!', 'success')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        flash('An error occurred while deleting item', 'danger')
        return redirect(request.referrer)

    
@views.route('/pluscart')
def pluscart():
    if request.method == 'GET':
        prod_id = request.args.get('prod_id')
        cart_item = Cart.query.get(prod_id)
        cart_item.quantity += 1
        db.session.commit()
        cart = Cart.query.filter_by(customer_id=current_user.id).all()
        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity
            total = amount + 1000
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': total
        }
        return jsonify(data)
    
    
    
@views.route('/minuscart')
def minuscart():
    if request.method == 'GET':
        prod_id = request.args.get('prod_id')
        cart_item = Cart.query.get(prod_id)
        if cart_item.quantity :
            cart_item.quantity -= 1
            db.session.commit()
            cart = Cart.query.filter_by(customer_id=current_user.id).all()
            amount = 0
            for item in cart:
                amount += item.product.current_price * item.quantity
                total = amount + 1000
                print(amount, total)
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': total
        }
        return jsonify(data)
    
    
# @views.route('/remove_cart_item', methods=['POST', 'GET'])
# @login_required
# def remove_cart_item():
#     if request.method == 'GET':
#         prod_id = request.args.get('prod_id')
        
#         # Check if prod_id is provided
#         if not prod_id:
#             return jsonify({'error': 'Product ID not provided'}), 400
        
#         # Check if prod_id is valid and corresponding cart_item exists
#         cart_item = Cart.query.get(prod_id)
#         if not cart_item:
#             return jsonify({'error': 'Cart item not found'}), 404
        
#         # Ensure the cart item belongs to the current user
#         if cart_item.customer_id != current_user.id:
#             return jsonify({'error': 'Unauthorized action'}), 403

#         db.session.delete(cart_item)
#         db.session.commit()
#         cart = Cart.query.filter_by(customer_id=current_user.id).all()
#         amount = sum(item.product.current_price * item.quantity for item in cart)
#         total = amount + 1000

#         data = {
#             'quantity': 3,
#             'amount': amount,
#             'total': total
#         }
#         return jsonify(data)




@views.route('/About_us')
def about():
    return render_template('about_us.html')


@views.route('/place_order', methods=['POST', 'GET'])
@login_required
def place_order():
    customer_cart= Cart.query.filter_by(customer_id=current_user.id).all()
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity
            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number="2541557636517", email=current_user.email, amount=total, currency="USD", narrative="Purchase of goods")
            
            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']
                
                new_order.product_id = item.product_id
                new_order.customer_id = current_user.id
                db.session.add(new_order)
                
                product = Product.query.get(item.product_id)
                product.in_stock -= item.quantity
                db.session.delete(item)
                db.session.commit()
                
            flash('Order placed successfully!', 'success')
            return redirect('/orders')
        except Exception as e:
            print(e)
            flash('An error occurred while placing order', 'danger')
            return redirect(request.referrer)
    
    flash('Your cart is empty!', 'danger')
    return redirect('/')



@views.route('/orders' , methods=['POST', 'GET'])
@login_required
def orders():
    orders = Order.query.filter_by(customer_id=current_user.id).all()
    for item in orders:
        print(item.product.product_name)
    return render_template('orders.html', orders=orders)
    
    
    

@views.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search}%')).all()
        print(items)
        return render_template('search.html', items_new=items, cart=Cart.query.filter_by(customer_id=current_user.id).all()
                           if current_user.is_authenticated else [] )
    return render_template('search.html')