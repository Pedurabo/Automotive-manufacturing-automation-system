from flask import Blueprint, render_template
from flask_login import login_required, current_user

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')

@planner_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Production Planner':
        return 'Access denied', 403
    return render_template('planner/dashboard.html') 