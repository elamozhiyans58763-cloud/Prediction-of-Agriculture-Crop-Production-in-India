import os
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session
from app.prediction import crop_predictor
from app.utils import get_unique_values, load_dataset_preview, get_dataset_info

VALID_USERNAME = os.environ.get('APP_USERNAME', 'admin')
VALID_PASSWORD = os.environ.get('APP_PASSWORD', 'password123')

USERS_FILE = Path(__file__).parent.parent / 'users.json'


def load_users():
    """Load registered users from JSON file."""
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_users(users):
    """Save registered users to JSON file."""
    USERS_FILE.write_text(json.dumps(users, indent=2))


def create_app():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(root_dir, 'templates')
    static_dir = os.path.join(root_dir, 'static')

    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'crop-production-secret')

    def require_login():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return None

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))

        error = None
        username = ''

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            # Check against default credentials
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))

            # Check against registered users
            users = load_users()
            if username in users and users[username]['password'] == password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))

            error = 'Invalid username or password. Please try again.'

        return render_template('login.html', error=error, username=username)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))

        error = None
        success = None
        username = ''
        email = ''

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()

            # Validation
            if len(username) < 3:
                error = 'Username must be at least 3 characters long.'
            elif password != confirm_password:
                error = 'Passwords do not match.'
            elif len(password) < 6:
                error = 'Password must be at least 6 characters long.'
            else:
                users = load_users()
                if username in users:
                    error = 'Username already exists. Please choose a different one.'
                else:
                    # Register new user
                    users[username] = {'email': email, 'password': password}
                    save_users(users)
                    success = 'Account created successfully! You can now sign in.'
                    username = ''
                    email = ''

        return render_template('signup.html', error=error, success=success, username=username, email=email)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        login_redirect = require_login()
        if login_redirect:
            return login_redirect

        states = get_unique_values('State_Name')
        seasons = get_unique_values('Season')
        crops = get_unique_values('Crop')
        districts = get_unique_values('District_Name')

        context = {
            'states': states or ['Maharashtra', 'Karnataka', 'Punjab'],
            'seasons': seasons or ['Kharif', 'Rabi', 'Whole Year'],
            'crops': crops or ['Rice', 'Wheat', 'Maize'],
            'districts': districts or ['Pune', 'Bangalore', 'Amritsar'],
            'prediction': None,
            'input_data': {},
            'fertilizer_rec': None,
            'recommendations': None,
            'message': None,
            'info': get_dataset_info(),
            'preview': load_dataset_preview().to_dict(orient='records'),
            'username': session.get('username')
        }

        if request.method == 'POST':
            try:
                input_data = {
                    'State_Name': request.form.get('state', ''),
                    'District_Name': request.form.get('district', ''),
                    'Crop_Year': int(request.form.get('crop_year', 2023)),
                    'Season': request.form.get('season', ''),
                    'Crop': request.form.get('crop', ''),
                    'Area': float(request.form.get('area', 0.0)),
                    'Annual_Rainfall': float(request.form.get('rainfall', 0.0)),
                    'Fertilizer': float(request.form.get('fertilizer', 0.0)),
                    'Pesticide': float(request.form.get('pesticide', 0.0)),
                    'Temperature': float(request.form.get('temperature', 0.0))
                }

                prediction = crop_predictor.predict(input_data)
                if prediction is not None:
                    fertilizer_rec = crop_predictor.get_fertilizer_recommendation(input_data['Crop'], input_data['Area'])
                    recommendations = crop_predictor.get_crop_recommendations(
                        input_data['State_Name'], input_data['Season'], input_data['Annual_Rainfall'], input_data['Temperature']
                    )

                    context.update({
                        'prediction': round(prediction, 2),
                        'input_data': input_data,
                        'fertilizer_rec': fertilizer_rec,
                        'recommendations': recommendations,
                        'message': 'Prediction generated successfully.'
                    })
                else:
                    context['message'] = 'Prediction failed. Please verify the input values and model availability.'

            except Exception as exc:
                context['message'] = f'Error processing the form: {exc}'
                context['input_data'] = request.form.to_dict()

        return render_template('new_index.html', **context)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
