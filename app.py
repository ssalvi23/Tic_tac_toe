from flask import Flask, render_template, request, redirect, jsonify ,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, User, Game
from werkzeug.security import generate_password_hash
import secrets
from flask_jwt_extended import create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

db.init_app(app)
jwt = JWTManager(app)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for user login (both GET and POST)
from flask_jwt_extended import create_access_token

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic to authenticate user and generate JWT
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Now you can call check_password
            # Generate JWT token after successful login
            access_token = create_access_token(identity=user.username)
            return jsonify({
                'msg': 'Login successful',
                'access_token': access_token  # Return the token to the client
            }), 200
        else:
            return jsonify({'msg': 'Invalid credentials'}), 400
    return render_template('login.html')

# Route for user registration (GET and POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match", 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists", 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and add to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('register.html')

# Route for the game page (protected by JWT)
@app.route('/game')
@jwt_required()
def game():
    return render_template('game.html')

# Add other routes as needed

if __name__ == '__main__':
    app.run(debug=True)
