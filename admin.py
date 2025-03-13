from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from models import User, SurveyResponse, db
import pandas as pd

admin_bp = Blueprint('admin', __name__)

# 1. Trang Admin chính
@admin_bp.route('/admin_panel')
def admin_panel():
    return render_template('admin.html')

# 2. Route xuất dữ liệu tổng (Export Overall Report)
@admin_bp.route('/export_overall')
def export_overall():
    # Lấy toàn bộ phản hồi khảo sát
    responses = SurveyResponse.query.all()
    data = []
    for r in responses:
        user = User.query.get(r.user_id)
        data.append({
            "User": user.username if user else "Unknown",
            "Response": r.response
        })
    # Chuyển danh sách thành DataFrame của pandas
    df = pd.DataFrame(data)
    output_file = "overall_report.xlsx"
    df.to_excel(output_file, index=False)
    return send_file(output_file, as_attachment=True)

# 3. Route hiển thị danh sách user chưa làm khảo sát
@admin_bp.route('/not_responded')
def not_responded():
    # Lấy danh sách id của user đã làm khảo sát
    responded_user_ids = {r.user_id for r in SurveyResponse.query.all()}
    # Lấy các user không có trong danh sách trên
    users_not_responded = User.query.filter(~User.id.in_(responded_user_ids)).all()
    return render_template('not_responded.html', users=users_not_responded)

# 4. Route thống kê tổng hợp khảo sát
@admin_bp.route('/statistics')
def statistics():
    total_users = User.query.count()
    total_responses = SurveyResponse.query.count()
    responded_user_ids = {r.user_id for r in SurveyResponse.query.all()}
    not_responded_count = total_users - len(responded_user_ids)
    
    stats = {
        "Total Users": total_users,
        "Total Survey Responses": total_responses,
        "Users Responded": len(responded_user_ids),
        "Users Not Responded": not_responded_count
    }
    return render_template('statistics.html', stats=stats)

