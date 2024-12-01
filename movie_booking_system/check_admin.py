from models import db, Admin
from app import app

with app.app_context():
    admin = Admin.query.filter_by(email="admin@example.com").first()
    if admin:
        print(f"Admin Found: {admin.email}")
    else:
        print("Admin not found.")
