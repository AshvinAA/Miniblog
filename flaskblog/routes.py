from flask import render_template, url_for , flash ,redirect ,request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app,db,bcrypt
from flask_login import login_user , current_user , logout_user , login_required

posts=[
    {
        'author':'Saima Alom',
        'title': 'Blog Post 1',
        'content': 'I love potatoes',
        'date_posted':'April 20,2018'
    },
    {
        'author':'Ashvin Afroz',
        'title': 'Blog Post 2',
        'content': 'Hell YEah',
        'date_posted':'April 22,2018'
    }
]




@app.route("/")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",title='about')

@app.route("/register", methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        #Hashing the password
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #Setting the user into the database
        user=User(username=form.username.data , email= form.email.data , password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! ', 'success' ) 
        return redirect(url_for('home'))
    
    return render_template("register.html" , title = 'Register' , form = form )

@app.route("/login" , methods=['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email = form.email.data).first()
        #bcrypt.check_password_hash -> checks the if the password inputted matches with the password in the database        
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            #login -> user parameter takes the person from the database and stores it in the user's browser session 
            #remember = form.remember.data gives the user the option to stay logged in for next sessions
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful . Please recheck your email or password" ,'danger')
    return render_template("login.html" , title = 'Login' , form = form )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
#login_required checks if the person is logged in or not
def account():
    return render_template('account.html' , title='Account')