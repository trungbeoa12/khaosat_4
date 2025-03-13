from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Sử dụng đường dẫn tuyệt đối tới file survey.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

