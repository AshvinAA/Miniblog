from flaskblog import app, db
from flaskblog.models import User, Post

def check_database():
    with app.app_context():
        print("\n--- USERS ---")
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id} | User: {user.username} | Email: {user.email}")
        
        print("\n--- POSTS ---")
        posts = Post.query.all()
        for post in posts:
            print(f"Title: {post.title} | Author: {post.author.username}")
        
        print("\n----------------\n")

if __name__ == "__main__":
    check_database()