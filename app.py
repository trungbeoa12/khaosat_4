from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from database import init_db, db
from models import User, SurveyResponse
from auth import auth_bp
from admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        response_text = request.form['response']
        survey_response = SurveyResponse(user_id=current_user.id, response=response_text)
        db.session.add(survey_response)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('survey.html')

# Đăng ký các Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)

