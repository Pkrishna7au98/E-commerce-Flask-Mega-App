from flask import redirect, render_template , url_for ,flash , request, session, current_app, make_response
from shop import db, myapp, photos, search, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm , CustomerLoginForm
from .model import Register, CustomerOrder
import os, secrets
import pdfkit
import stripe

publishable_key = "pk_test_51KBwqGSJIvndp4WyZfaHxqt9lVxqjVGBXyqYldk4OFUwHXsVddBqRSEiXIMWWbYHLWDWOuYwOPm0CPkoYD00Aoio00TvI9m5Gt"

stripe.api_key = "sk_test_51KBwqGSJIvndp4WyWKRtLPrfLGJ5GM872hZ6EV4HtANf1lU8S2UqzjawQ3ZEP8CW1tjqlNLePXI4bbfE9hKqMZOU00UsECdnHJ"

@myapp.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
        )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='My Cart',
        amount=amount,
        currency='inr',
        )

    orders = CustomerOrder.query.filter_by(customer_id = current_user.id).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@myapp.route('/thanks')
def thanks():
    return render_template('customer/thanks.html')

@myapp.route('/customer/register', methods = ['GET', 'POST'])
def customer_register():

    form = CustomerRegisterForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name = form.name.data, username=form.username.data, email=form.email.data, password = hash_password, country = form.country.data, state = form.state.data, city= form.city.data, address = form.address.data, contact = form.contact.data, zipcode = form.zipcode.data)

        db.session.add(register)
        flash(f'welcome {form.username.data} | Thanks for registration ', 'success')
        db.session.commit()
        return redirect(url_for('CustomerLogin'))

    return render_template('customer/register.html', form=form)

@myapp.route('/customer/login', methods=['GET', 'POST'])
def CustomerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        
        flash('Incorrect Email or Password')
        return redirect(url_for('CustomerLogin'))
    return render_template('customer/login.html', form=form  )

@myapp.route('/customer/logout')
def CustomerLogout():
    logout_user()
    return redirect(url_for('CustomerLogin'))

def updateshoppingcart():
    for _key , product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
        del product['colors']

    return updateshoppingcart

@myapp.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders = session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been been sent', 'success')
            return redirect(url_for('orders', invoice=invoice))
            
        except Exception as e:
            print(e)
            flash("Something went wrong while getting order", 'danger')
            return redirect(url_for('getCart'))

@myapp.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0 
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id = customer_id).order_by(CustomerOrder.id.desc()).first()
        
        for _key, product in orders.orders.items():
            discount = (product['discount'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * subTotal))

    else:
        return redirect(url_for('CustomerLogin'))
    return render_template('customer/order.html', invoice= invoice, tax = tax,subTotal=subTotal, grandTotal=grandTotal , customer = customer, orders = orders)


@myapp.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0 
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id = customer_id).order_by(CustomerOrder.id.desc()).first()
        
            for _key, product in orders.orders.items():
                discount = (product['discount'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = ("%.2f" % (1.06 * float(subTotal)))

            rendered = render_template('customer/pdf.html', invoice= invoice, tax = tax, grandTotal=grandTotal , customer = customer, orders = orders)

            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            pdf = pdfkit.from_string(rendered, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inilne: filename='+ invoice + '.pdf'
            return response
    
    return redirect(url_for('orders'))


