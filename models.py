from flask_login import UserMixin
from extensions import db
from datetime import datetime

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='pending')
    production_data = db.relationship('ProductionData', backref='work_order', lazy=True)
    defects = db.relationship('Defect', backref='work_order', lazy=True)

class ProductionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'), nullable=False)
    vin_or_barcode = db.Column(db.String(100))
    torque = db.Column(db.Float)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class Defect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'), nullable=False)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class WorkOrderNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    file_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    work_order = db.relationship('WorkOrder', backref=db.backref('notes', lazy=True))
    user = db.relationship('User', backref=db.backref('work_order_notes', lazy=True)) 