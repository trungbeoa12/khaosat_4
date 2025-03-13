from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import User, db
import pandas as pd

admin_bp = Blueprint('admin', __name__)  # Định nghĩa Blueprint

@admin_bp.route('/import_users')
def import_users():
    try:
        print("Đang chạy import_users...")  # Debug
        file_path = "/home/trungdt2/Desktop/khaosat_4/User_Data_with_Passwords.csv"
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            username = row['username']
            password = row['password']
            print(f"Đang nhập: {username} - {password}")  # Debug

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                hashed_password = generate_password_hash(str(password), method='pbkdf2:sha256')
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)

        db.session.commit()
        print("Import hoàn tất!")  # Debug
        flash("User data imported successfully!", "success")
    except Exception as e:
        print(f"Lỗi import: {e}")  # Debug
        flash(f"Error importing user data: {str(e)}", "danger")

    return redirect(url_for('home'))

