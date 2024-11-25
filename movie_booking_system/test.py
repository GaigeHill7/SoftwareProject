from app import app, db
from models import Movie

with app.app_context():
    now_showing_movies = Movie.query.filter_by(status="Now Showing").all()
    upcoming_movies = Movie.query.filter_by(status="Upcoming").all()
    for movie in now_showing_movies:
        print(f"Now Showing: {movie.title}")
    for movie in upcoming_movies:
        print(f"Upcoming: {movie.title}")
