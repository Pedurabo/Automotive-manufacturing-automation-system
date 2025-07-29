from flask import Blueprint, render_template
from flask_login import login_required, current_user

engineer_bp = Blueprint('engineer', __name__, url_prefix='/engineer')

@engineer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Process Engineer':
        return 'Access denied', 403
    return render_template('engineer/dashboard.html') 