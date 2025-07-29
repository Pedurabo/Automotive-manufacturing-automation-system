from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import WorkOrder, ProductionData, Defect
from extensions import db

shop_floor_operator_bp = Blueprint('shop_floor_operator', __name__, url_prefix='/operator')

@shop_floor_operator_bp.route('/dashboard')
@login_required
def dashboard():
    work_orders = WorkOrder.query.filter_by(assigned_to=current_user.id).all()
    return render_template('operator/dashboard.html', work_orders=work_orders)

@shop_floor_operator_bp.route('/work_order/<int:wo_id>/record', methods=['GET', 'POST'])
@login_required
def record_production(wo_id):
    work_order = WorkOrder.query.get_or_404(wo_id)
    if request.method == 'POST':
        vin_or_barcode = request.form['vin_or_barcode']
        torque = request.form.get('torque', type=float)
        temperature = request.form.get('temperature', type=float)
        prod_data = ProductionData(work_order_id=wo_id, vin_or_barcode=vin_or_barcode, torque=torque, temperature=temperature)
        db.session.add(prod_data)
        db.session.commit()
        flash('Production data recorded!')
        return redirect(url_for('shop_floor_operator.dashboard'))
    return render_template('operator/record_production.html', work_order=work_order)

@shop_floor_operator_bp.route('/work_order/<int:wo_id>/defect', methods=['GET', 'POST'])
@login_required
def record_defect(wo_id):
    work_order = WorkOrder.query.get_or_404(wo_id)
    if request.method == 'POST':
        description = request.form['description']
        defect_type = request.form['type']
        defect = Defect(work_order_id=wo_id, description=description, type=defect_type)
        db.session.add(defect)
        db.session.commit()
        flash('Defect recorded!')
        return redirect(url_for('shop_floor_operator.dashboard'))
    return render_template('operator/record_defect.html', work_order=work_order) 