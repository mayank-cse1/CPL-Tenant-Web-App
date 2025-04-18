from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Routes
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/reg')
def reg():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({"message": "User created successfully", "user_id": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login')
def login():
    return render_template('index.html')
@app.route('/tenantRegistration')
def tenantRegistration():
    return render_template('tenantRegistration.html')
@app.route('/tenant-data', methods=['GET'])
def tenant_data():
    id_token = request.headers['Authorization'].split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        tenant_data = db.collection('tenants').document(uid).get().to_dict()
        return jsonify(tenant_data), 200
    except Exception as e:
        return jsonify({"error": "Unauthorized"}), 401
@app.route('/admin')
def admin_portal():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    blocks = db.collection('blocks').stream()
    block_data = {block.id: block.to_dict() for block in blocks}
    return render_template('admin.html', blocks=block_data)
@app.route('/tenant')
def tenant_portal():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # blocks = db.collection('blocks').stream()
    # block_data = {block.id: block.to_dict() for block in blocks}
    return render_template('tenant.html')

@app.route('/block/<block_id>')
def block_details(block_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    flats = db.collection('blocks').document(block_id).collection('flats').stream()
    flat_data = {flat.id: flat.to_dict() for flat in flats}
    return render_template('block_details.html', block_id=block_id, flats=flat_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
