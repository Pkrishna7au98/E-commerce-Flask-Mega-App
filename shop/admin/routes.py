from types import MethodDescriptorType
from flask import session , request , url_for , redirect , render_template , flash
from shop import myapp, db , bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category

@myapp.route("/admin")
def admin():
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title="Admin Page" , products = products)

@myapp.route('/brands')
def brands():
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html' , title="Brands Page" , brands = brands)

@myapp.route('/categories')
def categories():
    if 'email' not in session:
        flash("Please Login First", "danger")
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html' , title="Categories Page" , categories = categories)

@myapp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form) 
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        nameofuser = form.name.data
        user = User(name = nameofuser , username = form.username.data, email= form.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()

        flash("Thank you {} for completing the registration process".format(nameofuser), "success")
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration Page")

@myapp.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} you are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash("Wrong password, Please try again", 'danger')
    return render_template('admin/login.html', form = form , title="Login Page")

@myapp.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)  
        return redirect(url_for('home'))  
    else:  
        flash('User not logged in', 'success') 

@myapp.route('/altproduct')
def altproduct():
    return render_template('alt_prod_page.html')