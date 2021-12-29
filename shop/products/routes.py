from operator import methodcaller
from types import prepare_class
from flask import redirect, render_template , url_for ,flash , request, session, current_app
from flask_uploads import IMAGES
from shop import db, myapp, photos, search
from shop.admin.routes import categories
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import os , secrets

@myapp.route('/')
def home():
    page = request.args.get('page,1,type=int')
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=6)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('/products/index.html', products = products, brands=brands, categories= categories)

@myapp.route('/result')
def result():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword , fields=['name', 'desc'], limit=3)
    return render_template('products/result.html', products = products, brands=brands , categories= categories)

@myapp.route("/brand/<int:id>")
def get_brand(id):
    page = request.args.get('page,1,type=int')
    get_bd = Brand.query.filter_by(id=id).first_or_404() 
    brand = Addproduct.query.filter_by(brand = get_bd).paginate(page=page, per_page= 1)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()

    return render_template("products/index.html", brand = brand, brands=brands, categories= categories, get_bd = get_bd)

@myapp.route("/product/<int:id>")
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html', product=product, brands=brands, categories= categories)


@myapp.route("/category/<int:id>")
def get_category(id):
    page = request.args.get('page,1,type=int')
    get_Cat = Category.query.filter_by(id=id).first_or_404()
    category = Addproduct.query.filter_by(category= get_Cat).paginate(page=page, per_page = 1)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()

    categories =  Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template("products/index.html", category = category, brands=brands, categories=categories, get_cat = get_Cat)

@myapp.route('/addbrand', methods = ['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name = getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template("products/addbrand.html", title = "Add Brand", brands= 'brands')

@myapp.route("/updatebrand/<int:id>", methods= ['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    if request.method == 'POST':
        updatebrand.name = brand
        flash("Your brand has been updated" , 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand', updatebrand = updatebrand)

@myapp.route('/deletebrand/<int:id>', methods = ['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(brand)
        flash(f'The {brand.name} was successfully deleted', 'danger')
        db.session.commit()
        return redirect(url_for('brands'))

    flash(f"The {brand.name} can't be deleted", 'warning')
    return render_template(url_for('admin'), brand = brand)


@myapp.route('/addcat', methods = ['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name = getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return render_template("products/addbrand.html", title = "Add Category")

@myapp.route('/updatecat/<int:id>', methods = ['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash("Please Login first", 'danger')
        return redirect(url_for("login"))

    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == 'POST':
        updatecat.name = category
        flash('Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))

    return render_template('products/updatebrand.html', title="Update Category", updatecat = updatecat)

@myapp.route('/deletecat/<int:id>', methods = ['POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(category)
        flash(f'The {category.name} was successfully deleted', 'danger')
        db.session.commit()
        return redirect(url_for('categories'))

    flash(f"The {category.name} can't be deleted", 'warning')
    return render_template(url_for('admin'), category = category)

@myapp.route('/addproduct',methods = ['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)

    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        discount = form.discount. data 
        desc = form.description.data
        color = form.color.data

        brand = request.form.get('brand')
        categ = request.form.get('category')

        image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")

        new_prod = Addproduct(name= name, price=price, stock = stock, discount = discount, desc = desc, color = color, brand_id = brand, category_id = categ, image_1=image_1, image_2=image_2, image_3=image_3)
  
        db.session.add(new_prod)
        db.session.commit()
        flash("The product was successully added", 'success')

        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title="Add product page", brands=brands, categories=categories, form = form)

@myapp.route('/updateproduct/<int:id>', methods = ['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash("Please Login first", 'danger')
        return redirect(url_for("login"))
 
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)

    brand = request.form.get('brand')
    category = request.form.get('category')

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand
        product.category_id = category
        product.color = form.color.data
        product.desc = form.description.data

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name = secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images" + product.image_))
                product.image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name = secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name = secrets.token_hex(10) + ".")


        flash("Your product has been updated", 'success')
        db.session.commit()
        return redirect('/')

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.desc

    return render_template('products/updateproduct.html',title = 'Update Prouduct', brands=brands, categories=categories, product=product, form=form)

    
@myapp.route('/deleteproduct/<int:id>', methods = ['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)

    if request.method == 'POST':

        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            
        except Exception as e:
            print(e)


        db.session.delete(product)
        db.session.commit()
        flash(f"Your product {product.name} has been deleted", 'success')
        return redirect(url_for('admin'))

    flash(f"This product can't be deleted" , 'warning')
    return render_template('admin', product=product)