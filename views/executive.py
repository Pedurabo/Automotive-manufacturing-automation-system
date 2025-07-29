from flask import Blueprint, render_template
from flask_login import login_required, current_user

executive_bp = Blueprint('executive', __name__, url_prefix='/executive')

@executive_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Executive':
        return 'Access denied', 403
    return render_template('executive/dashboard.html') 