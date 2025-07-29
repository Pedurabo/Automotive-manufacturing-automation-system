# Automotive Manufacturing Execution System (MES)

A comprehensive Manufacturing Execution System designed for automotive manufacturing facilities, featuring role-based access control, real-time production tracking, quality management, and operational dashboards.

## 🚀 Features

### Core Functionality
- **Role-Based Access Control**: 10 different user roles with specific permissions
- **Real-Time Production Tracking**: Monitor production lines and record production data
- **Quality Management**: Defect tracking and quality control workflows
- **Inventory Management**: Track materials, parts, and finished goods
- **Maintenance Scheduling**: Equipment maintenance and repair tracking
- **Reporting & Analytics**: Comprehensive dashboards and reports
- **API Integration**: RESTful APIs for system integration

### User Roles
- **Admin**: System administration and user management
- **Executive**: High-level overview and strategic reporting
- **Manager**: Department management and oversight
- **Supervisor**: Team supervision and operational control
- **Operator**: Production line operations and data entry
- **Shop Floor Operator**: Direct production activities
- **Quality**: Quality control and inspection processes
- **Maintenance**: Equipment maintenance and repairs
- **Logistics**: Supply chain and inventory management
- **Planner**: Production planning and scheduling
- **Engineer**: Technical support and process improvement
- **Auditor**: Compliance and audit functions

## 🛠️ Technology Stack

### Backend
- **Python 3.13**
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (can be configured for PostgreSQL/MySQL)
- **Flask-Login**: Authentication system
- **Flask-WTF**: Form handling and CSRF protection

### Frontend
- **React 18.2.0**: User interface framework
- **Material-UI (MUI)**: Component library
- **React Router**: Navigation and routing
- **Axios**: HTTP client for API calls

### Development Tools
- **Git**: Version control
- **npm**: Package management for frontend
- **pip**: Package management for backend

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.13** or higher
- **Node.js 16** or higher
- **npm** (comes with Node.js)
- **Git**

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Pedurabo/Automotive-manufacturing-automation-system.git
cd Automotive-manufacturing-automation-system
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Initialize the Database
```bash
python init_db.py
```

#### Run the Flask Backend
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Node.js Dependencies
```bash
npm install
```

#### Start the React Development Server
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
Automotive Manufacturing Execution System/
├── app.py                 # Main Flask application
├── auth.py               # Authentication and authorization
├── models.py             # Database models
├── extensions.py         # Flask extensions
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── pages/       # React components
│   │   ├── App.js       # Main App component
│   │   └── index.js     # Entry point
│   ├── package.json     # Node.js dependencies
│   └── public/          # Static assets
├── templates/           # HTML templates (legacy)
├── static/             # Static files (CSS, JS, uploads)
├── views/              # Flask view modules
└── instance/           # Database and configuration files
```

## 🔐 Authentication & Security

The system uses Flask-Login for session management and implements role-based access control. Each user role has specific permissions and access to different parts of the system.

### Default Users (for testing)
The system comes with pre-configured test users for each role. Check the `init_db.py` file for default credentials.

## 📊 API Documentation

### Authentication Endpoints
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /api/user` - Get current user info

### Production Endpoints
- `GET /api/production` - Get production data
- `POST /api/production` - Record production data
- `GET /api/defects` - Get defect reports
- `POST /api/defects` - Record defect data

### User Management Endpoints
- `GET /api/users` - Get all users (Admin only)
- `POST /api/users` - Create new user (Admin only)
- `PUT /api/users/<id>` - Update user (Admin only)
- `DELETE /api/users/<id>` - Delete user (Admin only)

## 🧪 Testing

### Backend Testing
```bash
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Set up a reverse proxy (nginx)
4. Use a production WSGI server (gunicorn)
5. Deploy the React build to a static file server

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/mes_db
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Pedurabo/Automotive-manufacturing-automation-system/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🔄 Version History

- **v1.0.0** - Initial release with basic MES functionality
- Role-based access control
- Production tracking
- Quality management
- React frontend with Material-UI

## 📞 Contact

- **Repository**: [https://github.com/Pedurabo/Automotive-manufacturing-automation-system](https://github.com/Pedurabo/Automotive-manufacturing-automation-system)
- **Issues**: [https://github.com/Pedurabo/Automotive-manufacturing-automation-system/issues](https://github.com/Pedurabo/Automotive-manufacturing-automation-system/issues)

---

**Note**: This is a development version. For production use, ensure proper security configurations and database setup. 