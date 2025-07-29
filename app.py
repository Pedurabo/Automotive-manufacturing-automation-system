from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager
from extensions import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended.exceptions import JWTExtendedException
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mes.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
jwt = JWTManager(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User
from auth import auth_bp
from views.shop_floor_operator import shop_floor_operator_bp
from views.api_operator import api_operator_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(shop_floor_operator_bp)
app.register_blueprint(api_operator_bp)

@app.route('/')
def index():
    return 'MES Flask API is running. Go to /login to sign in.'

# Example: emit a test notification to all clients
@app.route('/api/notify_test')
def notify_test():
    socketio.emit('notification', {'title': 'Test Notification', 'message': 'This is a test notification from the backend.'})
    return {'success': True}

# SocketIO event for client connection
default_namespace = '/'
@socketio.on('connect', namespace=default_namespace)
def handle_connect():
    print('Client connected')
    emit('notification', {'title': 'Welcome', 'message': 'Connected to MES notifications.'})

@socketio.on('disconnect', namespace=default_namespace)
def handle_disconnect():
    print('Client disconnected')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role.name}
        )
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Invalid username or password'}), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(JWTExtendedException)
def handle_jwt_errors(e):
    return jsonify({'msg': str(e)}), 422

if __name__ == '__main__':
    socketio.run(app, debug=True) 