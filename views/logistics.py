from flask import Blueprint, render_template
from flask_login import login_required, current_user

logistics_bp = Blueprint('logistics', __name__, url_prefix='/logistics')

@logistics_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Logistics Handler':
        return 'Access denied', 403
    return render_template('logistics/dashboard.html') 