from flask import Blueprint, render_template
from flask_login import login_required, current_user

maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@maintenance_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Maintenance Technician':
        return 'Access denied', 403
    return render_template('maintenance/dashboard.html') 