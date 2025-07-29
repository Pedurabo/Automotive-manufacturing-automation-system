from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name != 'MES Admin':
        return 'Access denied', 403
    return render_template('admin/dashboard.html') 