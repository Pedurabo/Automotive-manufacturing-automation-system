import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/login'
WORK_ORDERS_URL = f'{BASE_URL}/api/operator/work_orders'
COMPLETE_URL = lambda wo_id: f'{BASE_URL}/api/operator/work_order/{wo_id}/complete'
PROD_DATA_URL = lambda wo_id: f'{BASE_URL}/api/operator/work_order/{wo_id}/production_data'
DEFECT_URL = lambda wo_id: f'{BASE_URL}/api/operator/work_order/{wo_id}/defect'

USERNAME = 'operator1'
PASSWORD = 'password123'

session = requests.Session()

# Get login page to fetch CSRF token (if using Flask-WTF)
resp = session.get(LOGIN_URL)
soup = BeautifulSoup(resp.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})
csrf_token = csrf_token['value'] if csrf_token else ''

# Log in
login_data = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrf_token': csrf_token,
    'submit': 'Login'
}
resp = session.post(LOGIN_URL, data=login_data)
if 'Invalid username or password' in resp.text:
    print('Login failed!')
    exit(1)
print('Login successful!')

# List work orders
resp = session.get(WORK_ORDERS_URL)
print('Work Orders:', resp.json())

# If there are work orders, mark the first as complete and record data/defect
work_orders = resp.json()
if work_orders:
    wo_id = work_orders[0]['id']
    # Mark as complete
    resp = session.post(COMPLETE_URL(wo_id))
    print(f'Mark work order {wo_id} complete:', resp.json())
    # Record production data
    prod_data = {
        'vin_or_barcode': 'VIN123456789',
        'torque': 120.5,
        'temperature': 75.2
    }
    resp = session.post(PROD_DATA_URL(wo_id), json=prod_data)
    print(f'Record production data for {wo_id}:', resp.json())
    # Record defect
    defect_data = {
        'description': 'Paint scratch',
        'type': 'Cosmetic'
    }
    resp = session.post(DEFECT_URL(wo_id), json=defect_data)
    print(f'Record defect for {wo_id}:', resp.json())
else:
    print('No work orders found.') 