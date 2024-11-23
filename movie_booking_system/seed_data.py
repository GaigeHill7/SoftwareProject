from datetime import datetime
from app import app, db
from models import Movie

# Push the application context
with app.app_context():
    # Seed the database
    movie1 = Movie(
        title="Deadpool 3",
        synopsis="...",
        cast="Ryan Reynolds",
        runtime=120,
        status="Now Showing",
        price=12.5,
        release_date=datetime(2024, 5, 10)
    )
    movie2 = Movie(
        title="Red One",
        synopsis="...",
        cast="Dwayne Johnson",
        runtime=140,
        status="Upcoming",
        price=15.0,
        release_date=datetime(2024, 12, 25)
    )

    db.session.add_all([movie1, movie2])
    db.session.commit()

    print("Movies added successfully!")
