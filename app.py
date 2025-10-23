import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from Database.Mongo import db, awsdb
from Models.User import User
from Routes.Auth import auth_bp
from Routes.Dashboard import dashboard_bp
from Routes.Cashfree import cashfree_bp
from Routes.Ticket import ticket_bp
from Routes.Team import team_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

routes = [
    auth_bp,
    dashboard_bp,
    team_bp
]

for route in routes:
    app.register_blueprint(route)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@app.login_manager.user_loader
def load_user(user_id):
    user_data = awsdb.users.find_one({"registration": user_id})
    if user_data:
        return User(
            user_data['registration'],
            user_data['fullname'],
            user_data['email'],
            user_data['awsteam'],
            user_data['coreteam'],
            user_data.get('pfp_link', ''),
            user_data.get('year', ''),
            user_data.get('whatsapp', ''),
            user_data.get('cloudcaptain', False),
            user_data.get('mentor', False)
        )
    return None

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
