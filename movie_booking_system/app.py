from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Movie, Ticket, Admin  # Ensure these models exist and are properly defined
from datetime import datetime




# with app.app_context():
#     db.create_all()




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_booking.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)


migrate = Migrate(app, db)

# Default Route - Redirects to Login
@app.route('/')
def default():
    return redirect(url_for('login'))

# Home Route
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in to access the home page.', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html')  # Home page for logged-in users

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please log in.', 'danger')
            return redirect(url_for('login'))

        # Add user to database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        # Verify user credentials
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('browse_movies'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Browse Movies Route
@app.route('/browse_movies')
def browse_movies():
    now_showing = Movie.query.filter_by(status="Now Showing").all()
    upcoming_movies = Movie.query.filter_by(status="Upcoming").all()
    return render_template('browse_movies.html', now_showing=now_showing, upcoming_movies=upcoming_movies)


# Purchase Ticket Route
@app.route('/purchase_ticket/<int:movie_id>', methods=['GET', 'POST'])
def purchase_ticket(movie_id):
    if 'user_id' not in session:
        flash('Please log in to purchase a ticket.', 'warning')
        return redirect(url_for('login'))

    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        num_tickets = int(request.form['num_tickets'])

        # Create ticket(s)
        for _ in range(num_tickets):
            new_ticket = Ticket(movie_id=movie.id, user_id=session['user_id'])
            db.session.add(new_ticket)

        db.session.commit()
        flash(f'{num_tickets} ticket(s) purchased successfully for {movie.title}!', 'success')
        return redirect(url_for('browse_movies'))

    return render_template('purchase_ticket.html', movie=movie)

# Search Movies Route
@app.route('/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    results = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    return render_template('search_results.html', results=results, query=query)

# Admin Dashboard Route
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session or not Admin.query.get(session['user_id']):
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    movies = Movie.query.all()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        price = float(request.form['price'])
        release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d')

        # Add new movie
        new_movie = Movie(title=title, description=description, status=status, price=price, release_date=release_date)
        db.session.add(new_movie)
        db.session.commit()
        flash(f'Movie "{title}" added successfully!', 'success')

    return render_template('admin_dashboard.html', movies=movies)

# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
