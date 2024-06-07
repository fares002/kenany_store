from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrdersForm
from werkzeug.utils import secure_filename
from .models import Product , Order , Customer
from . import db


admin = Blueprint('admin', __name__)


@admin.route('/media/<filename>')
def get_media(filename):
    return send_from_directory('../media', filename)


@admin.route('/add_shop_items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()
        
        
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale

            new_shop_item.image = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfully', 'success')
                print('Product Added Successfully!!')
                return redirect(url_for('admin.add_shop_items'))
            except Exception as e:
                print(e)
                flash('Product Not Added!!')
        
        print(form.errors)
        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')


@admin.route('/shop_items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.created_at).all()
        return render_template('shop_items.html', items=items)
    
    
    return render_template('404.html')


@admin.route('update_item/<int:id>', methods=['GET', 'POST'])
@login_required
def update_shop_item(id):
    if current_user.id == 1:
        form= ShopItemsForm()
        item_to_update = Product.query.get(id)
        form.product_name.render_kw = {'value': item_to_update.product_name}
        form.current_price.render_kw = {'value': item_to_update.current_price}
        form.previous_price.render_kw = {'value': item_to_update.previous_price}
        form.in_stock.render_kw = {'value': item_to_update.in_stock}
        form.flash_sale.render_kw = {'checked': item_to_update.flash_sale}
        
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            
            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
            
            try:
                Product.query.filter_by(id=id).update(dict(
                                                            product_name=product_name,
                                                            current_price=current_price,
                                                            previous_price=previous_price,
                                                            in_stock=in_stock,
                                                            flash_sale=flash_sale,
                                                            image=file_path
                                                        ))
                
                db.session.commit()
                flash('Item Updated Successfully', 'success')
                return redirect(url_for('admin.shop_items'))
                
            except Exception as e:
                print(e)
                flash('Item Not Updated!!', 'danger')
                # return redirect(url_for('admin.update_shop_item', id=id))
        return render_template('update_item.html', form=form)
    
    return render_template('404.html')


@admin.route('/delete_item/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item Deleted Successfully', 'success')
            return redirect(url_for('admin.shop_items'))
        except Exception as e:
            print(e)
            flash('Item Not Deleted!!', 'danger')
        return redirect(url_for('admin.shop_items'))
        
        
    return render_template('404.html')



@admin.route('/view_orders', methods=['GET', 'POST'])
@login_required
def view_orders():
    if current_user.id == 1:
        orders = Order.query.order_by(Order.created_at).all()
        return render_template('view_orders.html', orders=orders)
    
    return render_template('404.html')



@admin.route('/update_order/<int:id>', methods=['GET', 'POST'])
@login_required
def update_order(id):
    if current_user.id == 1:
        form = OrdersForm()
        if form.validate_on_submit():
            order = Order.query.get(id)
            order_status = form.order_status.data
            try:
                order.status = order_status
                db.session.commit()
                flash('Order Status Updated Successfully', 'success')
                return redirect(url_for('admin.view_orders'))
            except Exception as e:
                print(e)
                flash('Order Status Not Updated!!', 'danger')
                return redirect(url_for('admin.update_order', id=id))
        
        return render_template('update_order.html', form=form)
    return render_template('404.html')

@admin.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    if current_user.id == 1:
        customers = Customer.query.order_by(Customer.created_at).all()
        return render_template('customers.html', customers=customers)
    
    return render_template('404.html')

