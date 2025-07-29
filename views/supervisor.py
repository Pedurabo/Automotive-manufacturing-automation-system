from flask import Blueprint, render_template
from flask_login import login_required, current_user

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')

@supervisor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Line Supervisor':
        return 'Access denied', 403
    return render_template('supervisor/dashboard.html') 