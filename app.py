from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from database import init_db, db
from models import User, SurveyResponse
from auth import auth_bp
from admin import admin_bp
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
# Sử dụng cấu hình database theo đường dẫn đã được thiết lập trong database.py
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    """
    - Nếu user đã đăng nhập và là admin -> chuyển hướng đến trang Admin Panel
    - Nếu user thường -> hiển thị trang index.html
    - Nếu chưa đăng nhập -> vẫn hiển thị index.html
    """
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_panel'))
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        # Lấy dữ liệu từ form khảo sát
        selected_infra = request.form.getlist('infrastructure[]')
        infra_others = request.form.get('infrastructure_others', '')
        
        policy = request.form.getlist('policy[]')
        policy_others = request.form.get('policy_others', '')
        
        support = request.form.getlist('support[]')
        support_others = request.form.get('support_others', '')
        
        propose_sieupgd = request.form.get('propose_sieupgd', '')
        pgd_code = request.form.get('pgd_code', '')
        pgd_name = request.form.get('pgd_name', '')
        other_banks_info = request.form.get('other_banks_info', '')
        additional_opinions = request.form.get('additional_opinions', '')
        
        # Gộp tất cả dữ liệu vào một dict
        data_dict = {
            "infrastructure": selected_infra,
            "infrastructure_others": infra_others,
            "policy": policy,
            "policy_others": policy_others,
            "support": support,
            "support_others": support_others,
            "propose_sieupgd": propose_sieupgd,
            "pgd_code": pgd_code,
            "pgd_name": pgd_name,
            "other_banks_info": other_banks_info,
            "additional_opinions": additional_opinions
        }
        # Chuyển dict thành chuỗi JSON
        response_text = json.dumps(data_dict, ensure_ascii=False)
        
        # Tạo đối tượng SurveyResponse và lưu vào database
        survey_response = SurveyResponse(user_id=current_user.id, response=response_text)
        db.session.add(survey_response)
        db.session.commit()
        
        flash("Khảo sát của bạn đã được gửi thành công!", "success")
        return redirect(url_for('home'))
    
    # Nếu GET -> hiển thị form survey
    return render_template('survey.html')

# Đăng ký các Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)

