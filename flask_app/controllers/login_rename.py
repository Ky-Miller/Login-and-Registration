from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.login_model import User

from  flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname


# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/')
def home_route():

    return render_template('login_page.html')

# ====================================
# Log In Validations Route
# ====================================
@app.route('/submit', methods= ['POST'])
def submit_user():

    if not User.user_validate(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email"     : request.form['email'],
        "password"  : pw_hash
    }
    session['first_name'] = request.form['first_name']
    user_id = User.add_user(data)
    return redirect('/dashboard/')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard/')
def dashboard():

    signed_in_user = User.get_by_id({'id': session['user_id']})

    return render_template('dashboard.html', signed_in_user = signed_in_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================


# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================
