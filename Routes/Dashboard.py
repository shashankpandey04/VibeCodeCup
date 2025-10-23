from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from Models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from Database.Mongo import db, awsdb
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    ticket = db.tickets.find_one({"email": current_user.email})
    # members is an array of emails; match if current user's email is in members or owner_mail equals user's email
    team = db.teams.find_one({
        "$or": [
            {"members": current_user.email},
            {"owner_mail": current_user.email}
        ]
    })
    return render_template('dashboard/index.html', team=team)

@dashboard_bp.route('/notifications', methods=['GET'])
@login_required
def notifications():
    notifications = db.notifications.find({"email": current_user.email}).sort("date", -1)
    return jsonify(
        [
            {
                "title": n['title'],
                "message": n['message'],
                "date": n['date'].strftime("%Y-%m-%d %H:%M:%S")
            } for n in notifications
        ]
    )