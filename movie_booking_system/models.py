from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)

class Admin(User):  # Inherit from User
    admin_id = db.Column(db.Integer, unique=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cast = db.Column(db.Text, nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    reviews = db.relationship('Review', backref='movie', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    showtime = db.Column(db.String(50), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
