from flask import Blueprint, render_template, flash, redirect, jsonify, request, session
from flask_login import login_required, current_user
from Database.Mongo import awsdb, db
from dotenv import load_dotenv
import os
import requests

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')

load_dotenv()

AWSURL = os.getenv("AWSURL")
I_API_KEY = os.getenv("INTERNAL_API_KEY")
TICKET_PRICE = 49

@ticket_bp.route('/purchase', methods=['GET'])
@login_required
def purchase_ticket():
    return render_template('ticket/purchase.html')

@ticket_bp.route('/buy', methods=['GET'])
@login_required
def buy_ticket():
    ticket = db.tickets.find_one({"email": current_user.email})
    if ticket:
        flash("You have already purchased a ticket.", "info")
        return redirect('/dashboard')
    if not current_user.is_authenticated:
        flash("Please log in to purchase a ticket.", "warning")
        return redirect('/auth/login')
    
    response = f"{AWSURL}/api/v1/cashfree/order/create"
    headers = {
        "I-API-KEY": I_API_KEY
    }
    order_response = requests.post(response, headers=headers)
    if order_response.status_code == 200:
        data = order_response.json()
        return render_template('ticket/buy.html', order_id=data['order_id'], payment_session_id=data['payment_session_id'], amount=TICKET_PRICE)
    else:
        flash("Failed to create order. Please try again.", "danger")
        return redirect('/ticket/purchase')