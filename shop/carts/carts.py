from flask import redirect, render_template , url_for ,flash , request, session, current_app
from shop import db, myapp, photos
from shop.products.models import Brand, Category, Addproduct

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2

    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        return False

@myapp.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method == 'POST':
            DictItems = {product_id:{'name':product.name, 'price':product.price, 'discount':product.discount, 'colors':colors , 'quantity':quantity , 'image':product.image_1, 'color': product.color}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])

                if product_id in session['Shoppingcart']:
                    for key,item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True                                                                         
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                    session['Shoppingcart'] = DictItems
                    return redirect(request.referrer)

    except Exception as e:         
        print(e)

    finally:
        return redirect(request.referrer)

@myapp.route('/carts')
def getCart():

    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    if 'Shoppingcart' not in session:
        return redirect(request.referrer)

    subtotal = 0
    grandtotal = 0
    tax = 0
    for key, product in session['Shoppingcart'].items():
        discount = float(product['discount'])
        amount = float(float(product['price']) * float(product['quantity'])) 
        subtotal += (amount -  discount)
        tax = int(0.06 * float(subtotal))
        grandtotal = int(1.06 * subtotal)
    return render_template('products/carts.html',tax = tax, grandtotal=grandtotal, brands=brands, categories= categories)

@myapp.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
 
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Cart Updated Successfully', 'success')
                    return redirect(url_for('getCart'))
                
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))


@myapp.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcar'] <= 0):
        return redirect(url_for('home'))

    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@myapp.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

        