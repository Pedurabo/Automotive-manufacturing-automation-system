from app import app
from extensions import db
from models import User, Role, WorkOrder
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create roles
    roles = [
        'Shop Floor Operator',
        'Line Supervisor',
        'Production Planner',
        'Quality Inspector',
        'Maintenance Technician',
        'Process Engineer',
        'Logistics Handler',
        'MES Admin',
        'Plant Manager',
        'Executive',
        'External Auditor'
    ]
    role_objs = {}
    for role_name in roles:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()
        role_objs[role_name] = role

    # Create example users for each role
    users = [
        ('operator1', 'password123', 'Shop Floor Operator'),
        ('supervisor1', 'password123', 'Line Supervisor'),
        ('planner1', 'password123', 'Production Planner'),
        ('quality1', 'password123', 'Quality Inspector'),
        ('maintenance1', 'password123', 'Maintenance Technician'),
        ('engineer1', 'password123', 'Process Engineer'),
        ('logistics1', 'password123', 'Logistics Handler'),
        ('admin1', 'password123', 'MES Admin'),
        ('manager1', 'password123', 'Plant Manager'),
        ('exec1', 'password123', 'Executive'),
        ('auditor1', 'password123', 'External Auditor'),
    ]
    user_objs = {}
    for username, password, role_name in users:
        user = User(
            username=username,
            password=generate_password_hash(password),
            role_id=role_objs[role_name].id
        )
        db.session.add(user)
        db.session.commit()
        user_objs[username] = user

    # Create sample work orders assigned to the operator
    wo1 = WorkOrder(description='Assemble engine block', assigned_to=user_objs['operator1'].id)
    wo2 = WorkOrder(description='Install transmission', assigned_to=user_objs['operator1'].id)
    db.session.add_all([wo1, wo2])
    db.session.commit()

    print('Database initialized with sample roles and users.') 