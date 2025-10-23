from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from Models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from Database.Mongo import db, awsdb
import bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required."
            })

        email = email.lower()
        user_data = awsdb.users.find_one({"email": email})
        if not user_data:
            return jsonify({
                "status": "error",
                "message": "Account does not exist with this email."
            })

        if not bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return jsonify({
                "status": "error",
                "message": "Invalid email or password."
            })

        user_obj = User(
            user_data['registration'],
            user_data['fullname'],
            user_data['email'],
            user_data['awsteam'],
            user_data['coreteam'],
            user_data.get('pfp_link', ''),
            user_data.get('year', ''),
            user_data.get('whatsapp', ''),
            user_data.get('cloudcaptain', False)
        )

        login_user(user_obj)

        return jsonify({
            "status": "success",
            "message": "Logged in successfully."
        })

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        registration = request.form['registration']
        whatsapp = request.form['phone']
        year = request.form['year']
        email = email.lower()
        college = request.form['college'].lower()
        college = college.replace(' ', '-')

        user = awsdb.users.find_one({'email': email})
        if len(whatsapp) != 10 or not whatsapp.isdigit():
            return jsonify(
                {
                    "status": "error",
                    "message": "Invalid phone number. It should be 10 digits."
                }
            )
        if user:
            return jsonify(
                {
                    "status": "error",
                    "message": "Account already exists with this email!"
                }
            )
        regno_check = awsdb.users.find_one({'registration': registration})
        if regno_check:
            return jsonify(
                {
                    "status": "error",
                    "message": "Account already exists with this registration number!"
                }
            )
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({
            'email': email,
            'fullname': name,
            'registration': registration,
            'year': year,
            'whatsapp': whatsapp,
            'password': hashed_password,
            "created_at": datetime.now(),
            "awsteam": False,
            "coreteam": False,
            "pfp_link": 'https://cdn-icons-png.flaticon.com/512/219/219986.png',
            'college': college
        })

        return jsonify({
            "status": "success",
            "message": "Registered successfully. Please log in."
        })

    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)