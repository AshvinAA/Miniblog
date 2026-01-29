from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8e4ef53df82522c718d6d97abd4941b4'

posts=[
    {
        'author':'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted':'April 20,2018'
    },
    {
        'author':'Ashvin Afroz',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted':'April 22,2018'
    }
]


@app.route("/")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",title='about')


if __name__ == "__main__":
    app.run(debug=True)
