cd /home/trungdt2/Desktop/khaosat_4/

source venv/bin/activate  # Trên Ubuntu/Linux

pip install flask flask_sqlalchemy flask_login flask_wtf pandas gunicorn

mkdir templates static
touch app.py database.py models.py auth.py admin.py forms.py
touch templates/index.html templates/survey.html templates/admin.html
touch static/style.css

