from app import app  # Import the app object from app.py
from models import db, Movie
from datetime import datetime

# Ensure the app context is available for database operations
with app.app_context():
    # Seed data
    movie1 = Movie(
        title="Deadpool 3",
        synopsis="Deadpool's peaceful existence comes crashing down...",
        cast="Ryan Reynolds",
        runtime=120,
        status="Now Showing",
        price=12.5,
        release_date=datetime(2024, 5, 10)
    )
    movie2 = Movie(
        title="Red One",
        synopsis="A thrilling holiday adventure...",
        cast="Dwayne Johnson",
        runtime=140,
        status="Upcoming",
        price=15.0,
        release_date=datetime(2024, 12, 25)
    )

    # Add and commit movies to the database
    db.session.add_all([movie1, movie2])
    db.session.commit()
    print("Seed data successfully added!")
