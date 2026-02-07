import secrets
from flask import render_template, url_for , flash ,redirect ,request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm ,UpdateAccountForm
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
        'author':' Auvro ',
        'title': 'Muri kha',
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

def save_picture(form_picture):
    random_hex  = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/profile_pics' , picture_fn)



@app.route("/account" , methods=['GET' , 'POST'])
@login_required
#login_required checks if the person is logged in or not
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash (' Your account has been updated !' , 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET' : 
            form.username.data = current_user.username
            form.email.data = current_user.email
    
    image_file= url_for('static' , filename= 'profile_pics/' + current_user.image_file)
    return render_template('account.html' , title='Account',image_file = image_file , form=form )