from flask import Blueprint, render_template
from flask_login import login_required, current_user

quality_bp = Blueprint('quality', __name__, url_prefix='/quality')

@quality_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Quality Inspector':
        return 'Access denied', 403
    return render_template('quality/dashboard.html') 