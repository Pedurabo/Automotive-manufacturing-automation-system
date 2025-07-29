from flask import Blueprint, render_template
from flask_login import login_required, current_user

manager_bp = Blueprint('manager', __name__, url_prefix='/manager')

@manager_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'Plant Manager':
        return 'Access denied', 403
    return render_template('manager/dashboard.html') 