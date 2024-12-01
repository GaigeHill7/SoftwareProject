from app import app, db
from models import Admin

# Create an admin user
new_admin = Admin(
    id=1,  # Replace with a valid ID if necessary
    name="Admin User",
    email="admin@example.com",
    password="adminpassword"
)

# Use the application context
with app.app_context():
    db.session.add(new_admin)
    db.session.commit()
    print("Admin user created successfully!")

