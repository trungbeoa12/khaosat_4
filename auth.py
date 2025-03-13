from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        print(f"🔍 Đang kiểm tra đăng nhập: {username} - {password}")  # Debug

        user = User.query.filter_by(username=username).first()

        if not user:
            print("❌ Không tìm thấy user!")  # Debug
            flash('Invalid username or password', 'danger')
            return render_template('login.html')

        print(f"✅ Tìm thấy user: {user.username}")
        print(f"📌 Mật khẩu trong database: {repr(user.password)} (Loại: {type(user.password)})")
        print(f"📌 Mật khẩu nhập vào: {repr(password)} (Loại: {type(password)})")

        # Nếu mật khẩu là số (int), chuyển về chuỗi trước khi so sánh
        db_password = str(user.password).strip()

        if db_password == password:
            login_user(user)
            print("🎉 Đăng nhập thành công!")  # Debug
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        print("❌ Sai tài khoản hoặc mật khẩu!")  # Debug
        flash('Invalid username or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')  # Hiển thị thông báo khi đăng xuất
    return redirect(url_for('auth.login'))

