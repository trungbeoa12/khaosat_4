from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"  # Cập nhật đúng tên bảng
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    response = db.Column(db.String(500), nullable=False)

