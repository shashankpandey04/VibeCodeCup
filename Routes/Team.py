from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from Database.Mongo import db
from datetime import datetime
import secrets, string

team_bp = Blueprint('team', __name__, url_prefix='/team')

def generate_team_code(length=6):
    import string, secrets
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# ------------------------------
# View Team
# ------------------------------
@team_bp.route('/<team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = db.teams.find_one({
        "team_code": team_id,
        "$or": [
            {"members": current_user.email},
            {"owner_mail": current_user.email}
        ]
    })
    if not team:
        flash('Team not found or access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('team/view.html', team=team)

# ------------------------------
# Create Team
# ------------------------------
@team_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_team():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        if not team_name:
            flash('Team name is required!', 'danger')
            return redirect(url_for('team.create_team'))

        existing_team = db.teams.find_one({
            "$or": [
                {"members": current_user.email},
                {"owner_mail": current_user.email}
            ]
        })
        if existing_team:
            flash('You are already part of a team.', 'warning')
            return redirect(url_for('team.view_team', team_id=existing_team["team_code"]))

        team_code = generate_team_code()
        db.teams.insert_one({
            "name": team_name,
            "owner_mail": current_user.email,
            "members": [current_user.email],
            "pending_requests": [],
            "created_at": datetime.now(),
            "team_code": team_code
        })
        flash('Team created successfully!', 'success')
        return redirect(url_for('team.view_team', team_id=team_code))

    my_team = db.teams.find_one({
        "$or": [
            {"members": current_user.email},
            {"owner_mail": current_user.email}
        ]
    })
    return render_template('team/join.html', my_team=my_team)

# ------------------------------
# Join Team (Request Mode)
# ------------------------------
@team_bp.route('/join', methods=['POST'])
@login_required
def join_team():
    team_code = request.form.get('team_code')
    team = db.teams.find_one({"team_code": team_code})

    if not team:
        flash('Invalid team code.', 'danger')
        return redirect(url_for('team.create_team'))

    # Prevent joining multiple teams
    existing_team = db.teams.find_one({
        "$or": [
            {"members": current_user.email},
            {"owner_mail": current_user.email}
        ]
    })
    if existing_team:
        flash('You are already part of a team.', 'warning')
        return redirect(url_for('team.view_team', team_id=existing_team["team_code"]))

    # Prevent duplicate requests
    if current_user.email in team.get("pending_requests", []):
        flash('You already requested to join this team.', 'info')
        return redirect(url_for('team.create_team'))

    db.teams.update_one(
        {"team_code": team_code},
        {"$push": {"pending_requests": current_user.email}}
    )
    flash('Join request sent successfully. Await team approval.', 'success')
    return redirect(url_for('team.create_team'))


# ------------------------------
# Approve or Reject Request
# ------------------------------
@team_bp.route('/<team_id>/approve', methods=['POST'])
@login_required
def approve_request(team_id):
    email = request.form.get('email')
    action = request.form.get('action')  # approve / reject
    team = db.teams.find_one({"team_code": team_id, "owner_mail": current_user.email})

    if not team:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    if action == 'approve':
        if len(team['members']) >= 4:
            flash('Team limit reached (4 members max).', 'warning')
        else:
            db.teams.update_one(
                {"team_code": team_id},
                {
                    "$push": {"members": email},
                    "$pull": {"pending_requests": email}
                }
            )
            flash(f'{email} added to your team!', 'success')
    elif action == 'reject':
        db.teams.update_one(
            {"team_code": team_id},
            {"$pull": {"pending_requests": email}}
        )
        flash(f'{email} request rejected.', 'info')

    return redirect(url_for('team.view_team', team_id=team_id))


# ------------------------------
# Leave Team
# ------------------------------
@team_bp.route('/<team_id>/leave', methods=['POST'])
@login_required
def leave_team(team_id):
    team = db.teams.find_one({"team_code": team_id})
    if not team:
        flash('Team not found.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    if team['owner_mail'] == current_user.email:
        flash('Owner cannot leave the team.', 'warning')
        return redirect(url_for('team.view_team', team_id=team_id))

    db.teams.update_one(
        {"team_code": team_id},
        {"$pull": {"members": current_user.email}}
    )
    flash('You have left the team.', 'info')
    return redirect(url_for('team.create_team'))
