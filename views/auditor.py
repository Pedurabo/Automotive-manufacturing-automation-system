from flask import Blueprint, render_template
from flask_login import login_required, current_user

auditor_bp = Blueprint('auditor', __name__, url_prefix='/auditor')

@auditor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'External Auditor':
        return 'Access denied', 403
    return render_template('auditor/dashboard.html') 