import secrets
import os
from PIL import Image
from flask import render_template, url_for , flash ,redirect ,request , abort
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm ,UpdateAccountForm ,PostForm
from flaskblog import app,db,bcrypt
from flask_login import login_user , current_user , logout_user , login_required


@app.route("/")
def home():
    posts= Post.query.all()
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


#Have to learn this 
#What does the os module can do (theres)
def save_picture(form_picture):
    random_hex  = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/profile_pics' , picture_fn)
    
    
    #Using pillow for image processing  
    
    output_size = (125 , 125) #resizing size 1000x1000 image becomes 125x125
    i = Image.open(form_picture)
    i.thumbnail(output_size) #sizing the image 
    i.save(picture_path) #inserting the lightweight version now
    
    return picture_fn


@app.route("/account" , methods=['GET' , 'POST'])
@login_required
#login_required checks if the person is logged in or not
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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

@app.route("/post/new" , methods = ['GET','POST'])
@login_required
def new_post():
    form= PostForm()
    if form.validate_on_submit():
        post= Post(title=form.title.data , content= form.content.data , author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created! ' , 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html' , title='New Post' , form=form ,legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #this basically means give me the post with this postID or else just return error 404
    return render_template('post.html', title= post.title , post=post)

@app.route("/post/<int:post_id>/update" , methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #http response for a false route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content= form.content.data
        db.session.commit()
        flash('Your post has been updated!' , 'success')
        return redirect(url_for('post' , post_id=post.id))
    elif request.method=='GET':
        form.title.data = post.title 
        form.content.data = post.content
    form.title.data=post.title
    form.content.data=post.content
    return render_template('create_post.html' , title='Update Post' , form=form ,legend='Update Post')


@app.route("/post/<int:post_id>/delete" , methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!' , 'success')
    return redirect(url_for('home'))