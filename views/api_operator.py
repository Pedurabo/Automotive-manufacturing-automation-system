from flask import Blueprint, jsonify, request, current_app, send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import WorkOrder, ProductionData, Defect, WorkOrderNote, User
from extensions import db

api_operator_bp = Blueprint('api_operator', __name__, url_prefix='/api/operator')

# In-memory bid store (reset on server restart)
bid_store = []

# Unique bid ID counter
def next_bid_id():
    if not hasattr(next_bid_id, 'counter'):
        next_bid_id.counter = 1
    val = next_bid_id.counter
    next_bid_id.counter += 1
    return val

# In-memory store for work order notes/photos
work_order_notes = {}

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_operator_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        # Ensure unique filename
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(save_path):
            filename = f"{base}_{counter}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1
        file.save(save_path)
        file_url = f"/static/uploads/{filename}"
        return jsonify({'success': True, 'file_url': file_url}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# Serve uploaded files (optional, for direct access)
@api_operator_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@api_operator_bp.route('/work_orders', methods=['GET'])
@jwt_required()
def list_work_orders():
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    if role != 'Shop Floor Operator':
        return jsonify({'error': 'Forbidden'}), 403
    work_orders = WorkOrder.query.filter_by(assigned_to=int(user_id)).all()
    return jsonify([
        {'id': wo.id, 'description': wo.description, 'status': wo.status} for wo in work_orders
    ])

@api_operator_bp.route('/work_order/<int:wo_id>/complete', methods=['POST'])
@jwt_required()
def mark_work_order_complete(wo_id):
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    if role != 'Shop Floor Operator':
        return jsonify({'error': 'Forbidden'}), 403
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    wo.status = 'complete'
    db.session.commit()
    return jsonify({'success': True})

@api_operator_bp.route('/work_order/<int:wo_id>/start', methods=['POST'])
@jwt_required()
def start_work_order(wo_id):
    user_id = get_jwt_identity()
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    wo.status = 'in_progress'
    db.session.commit()
    return jsonify({'success': True, 'status': wo.status})

@api_operator_bp.route('/work_order/<int:wo_id>/pause', methods=['POST'])
@jwt_required()
def pause_work_order(wo_id):
    user_id = get_jwt_identity()
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    wo.status = 'paused'
    db.session.commit()
    return jsonify({'success': True, 'status': wo.status})

@api_operator_bp.route('/work_order/<int:wo_id>/resume', methods=['POST'])
@jwt_required()
def resume_work_order(wo_id):
    user_id = get_jwt_identity()
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    wo.status = 'in_progress'
    db.session.commit()
    return jsonify({'success': True, 'status': wo.status})

@api_operator_bp.route('/work_order/<int:wo_id>/note', methods=['POST'])
@jwt_required()
def add_work_order_note(wo_id):
    user_id = get_jwt_identity()
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json()
    note = data.get('note')
    photo_url = data.get('photo_url')
    if not note:
        return jsonify({'error': 'Note text required'}), 400
    note_obj = WorkOrderNote(
        work_order_id=wo_id,
        user_id=user_id,
        note=note,
        file_url=photo_url
    )
    db.session.add(note_obj)
    db.session.commit()
    # Return all notes for this work order
    notes = WorkOrderNote.query.filter_by(work_order_id=wo_id).order_by(WorkOrderNote.timestamp.desc()).all()
    notes_data = [
        {
            'id': n.id,
            'note': n.note,
            'photo_url': n.file_url,
            'user_id': n.user_id,
            'username': User.query.get(n.user_id).username if User.query.get(n.user_id) else '',
            'timestamp': n.timestamp.isoformat() if n.timestamp else ''
        }
        for n in notes
    ]
    return jsonify({'success': True, 'notes': notes_data})

@api_operator_bp.route('/work_order/<int:wo_id>/notes', methods=['GET'])
@jwt_required()
def get_work_order_notes(wo_id):
    notes = WorkOrderNote.query.filter_by(work_order_id=wo_id).order_by(WorkOrderNote.timestamp.desc()).all()
    notes_data = [
        {
            'id': n.id,
            'note': n.note,
            'photo_url': n.file_url,
            'user_id': n.user_id,
            'username': User.query.get(n.user_id).username if User.query.get(n.user_id) else '',
            'timestamp': n.timestamp.isoformat() if n.timestamp else ''
        }
        for n in notes
    ]
    return jsonify({'notes': notes_data})

@api_operator_bp.route('/work_order/<int:wo_id>/production_data', methods=['POST'])
@jwt_required()
def record_production_data(wo_id):
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    if role != 'Shop Floor Operator':
        return jsonify({'error': 'Forbidden'}), 403
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json()
    vin = data.get('vin_or_barcode')
    torque = data.get('torque')
    temperature = data.get('temperature')
    errors = []
    if not vin or not isinstance(vin, str) or len(vin.strip()) < 3:
        errors.append('VIN or barcode is required and must be at least 3 characters.')
    try:
        torque = float(torque)
        if not (0 <= torque <= 1000):
            errors.append('Torque must be between 0 and 1000.')
    except (TypeError, ValueError):
        errors.append('Torque must be a number.')
    try:
        temperature = float(temperature)
        if not (-50 <= temperature <= 200):
            errors.append('Temperature must be between -50 and 200.')
    except (TypeError, ValueError):
        errors.append('Temperature must be a number.')
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    prod_data = ProductionData(
        work_order_id=wo_id,
        vin_or_barcode=vin,
        torque=torque,
        temperature=temperature
    )
    db.session.add(prod_data)
    db.session.commit()
    return jsonify({'success': True})

@api_operator_bp.route('/work_order/<int:wo_id>/defect', methods=['POST'])
@jwt_required()
def record_defect(wo_id):
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    if role != 'Shop Floor Operator':
        return jsonify({'error': 'Forbidden'}), 403
    wo = WorkOrder.query.get_or_404(wo_id)
    if wo.assigned_to != int(user_id):
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json()
    description = data.get('description')
    defect_type = data.get('type')
    errors = []
    if not description or not isinstance(description, str) or len(description.strip()) < 3:
        errors.append('Description is required and must be at least 3 characters.')
    if not defect_type or not isinstance(defect_type, str) or len(defect_type.strip()) < 3:
        errors.append('Defect type is required and must be at least 3 characters.')
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    defect = Defect(
        work_order_id=wo_id,
        description=description,
        type=defect_type
    )
    db.session.add(defect)
    db.session.commit()
    return jsonify({'success': True})

@api_operator_bp.route('/bids', methods=['POST'])
@jwt_required()
def submit_bid():
    data = request.get_json()
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    bid = {
        'id': next_bid_id(),
        'user_id': user_id,
        'role': role,
        'type': data.get('type'),
        'price': float(data.get('price', 0)),
        'quantity': float(data.get('quantity', 0))
    }
    bid_store.append(bid)
    return jsonify({'success': True, 'message': 'Bid submitted!', 'bid': bid})

@api_operator_bp.route('/bids/<int:bid_id>', methods=['PUT'])
@jwt_required()
def update_bid(bid_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    for bid in bid_store:
        if bid['id'] == bid_id and bid['user_id'] == user_id:
            bid['price'] = float(data.get('price', bid['price']))
            bid['quantity'] = float(data.get('quantity', bid['quantity']))
            bid['type'] = data.get('type', bid['type'])
            return jsonify({'success': True, 'bid': bid})
    return jsonify({'success': False, 'message': 'Bid not found or not yours'}), 404

@api_operator_bp.route('/bids/<int:bid_id>', methods=['DELETE'])
@jwt_required()
def delete_bid(bid_id):
    user_id = get_jwt_identity()
    for i, bid in enumerate(bid_store):
        if bid['id'] == bid_id and bid['user_id'] == user_id:
            del bid_store[i]
            return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Bid not found or not yours'}), 404

@api_operator_bp.route('/bids', methods=['GET'])
@jwt_required()
def get_bids():
    # Return all bids for display
    return jsonify(bid_store)

@api_operator_bp.route('/market/clear', methods=['POST'])
@jwt_required()
def clear_market():
    # Simple market clearing: sort supply ascending by price, demand descending by price
    supply_bids = [b for b in bid_store if b['type'] == 'supply']
    demand_bids = [b for b in bid_store if b['type'] == 'demand']
    supply_bids.sort(key=lambda b: b['price'])
    demand_bids.sort(key=lambda b: -b['price'])
    cleared = []
    supply_idx, demand_idx = 0, 0
    total_cleared = 0
    lmp = 0
    # Match supply and demand
    while supply_idx < len(supply_bids) and demand_idx < len(demand_bids):
        s = supply_bids[supply_idx]
        d = demand_bids[demand_idx]
        qty = min(s['quantity'], d['quantity'])
        if s['price'] <= d['price'] and qty > 0:
            cleared.append({'supply': s, 'demand': d, 'quantity': qty, 'price': d['price']})
            lmp = d['price']  # Last matched price
            s['quantity'] -= qty
            d['quantity'] -= qty
            total_cleared += qty
            if s['quantity'] == 0:
                supply_idx += 1
            if d['quantity'] == 0:
                demand_idx += 1
        else:
            break
    # LMP per node (simulate 1 node for now)
    lmp_result = {'Node1': lmp} if lmp else {'Node1': 0}
    # Dispatch: how much each GenCo supplies
    dispatch = {}
    for c in cleared:
        uid = c['supply']['user_id']
        dispatch[uid] = dispatch.get(uid, 0) + c['quantity']
    dispatch_result = [{'unit': f'GenCo{uid}', 'output': qty} for uid, qty in dispatch.items()]
    # Settlement: revenue for GenCos, cost for LSEs
    settlement = []
    for c in cleared:
        gen = c['supply']
        lse = c['demand']
        revenue = c['quantity'] * c['price']
        settlement.append({'participant': f'GenCo{gen["user_id"]}', 'revenue': revenue})
        settlement.append({'participant': f'LSE{lse["user_id"]}', 'cost': revenue})
    settlement_history.extend(settlement)
    return jsonify({
        'lmp': lmp_result,
        'dispatch': dispatch_result,
        'settlement': settlement,
        'message': f'Market cleared: {total_cleared} MW at LMP {lmp}'
    })

@api_operator_bp.route('/profit', methods=['GET'])
@jwt_required()
def get_profit():
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    # Only for GenCo (supply) users
    if role not in ['GenCo', 'Shop Floor Operator', 'Supply', 'supply']:
        return jsonify({'profit': 0, 'message': 'Not a GenCo/supply user'}), 403
    # Find all settlements for this user as GenCo
    profit = 0
    for s in settlement_history:
        if s.get('participant') == f'GenCo{user_id}':
            profit += s.get('revenue', 0)
    return jsonify({'profit': profit})

@api_operator_bp.route('/report', methods=['GET'])
@jwt_required()
def get_report():
    user_id = get_jwt_identity()
    role = get_jwt().get('role')
    user_bids = [b for b in bid_store if b['user_id'] == user_id]
    user_settlements = [s for s in settlement_history if f'{role}{user_id}' in s.get('participant', '')]
    profit = sum(s.get('revenue', 0) for s in user_settlements if 'revenue' in s)
    cost = sum(s.get('cost', 0) for s in user_settlements if 'cost' in s)
    return jsonify({
        'bids': user_bids,
        'settlements': user_settlements,
        'profit': profit,
        'cost': cost
    })

# Track settlement history globally
settlement_history = [] 