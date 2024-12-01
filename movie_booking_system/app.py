from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Movie, Ticket, Admin, Review
from datetime import datetime
import random
import string
import os
import datetime 


app = Flask(__name__)

# Explicitly set the path to the database in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'movie_booking.db')}"
app.config['SECRET_KEY'] = 'your_secret_key'

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)



#db.init_app(app)
migrate = Migrate(app, db)

# Default Route - Redirects to Login
@app.route('/')
def default():
    return redirect(url_for('login'))




@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in to access the home page.', 'warning')
        return redirect(url_for('login'))
    
    # Check if the user is an admin
    is_admin = Admin.query.get(session.get('user_id'))
    
    return render_template('home.html', is_admin=is_admin)

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone')  # Optional field
        address = request.form.get('address')  # Optional field

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'error')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(name=name, email=email, password=password, phone=phone, address=address)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Check if username already exists
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists. Please log in.', 'danger')
#             return redirect(url_for('login'))

#         # Add user to database
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('Registration successful! Please log in.', 'success')
#         return redirect(url_for('login'))

#     return render_template('register.html')

# User Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Check if the user exists and the password matches
#         user = User.query.filter_by(email=email).first()
#         if user and user.password == password:  # Ensure to hash and verify passwords in production
#             flash('Login successful!', 'success')
#             # Perform session management (e.g., store user ID in the session)
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid email or password.', 'error')

#     return render_template('login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user is an admin
        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            session['user_id'] = admin.id
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))

        # If neither admin nor user, flash an error message
        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('admin_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user is an admin
        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            session['user_id'] = admin.id
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Check if the user is a regular user
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = False  # Explicitly set this to False for regular users
            flash('Login successful!', 'success')
            return redirect(url_for('browse_movies'))

        # If neither admin nor user, flash an error message
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
        # for _ in range(num_tickets):
        #     new_ticket = Ticket(movie_id=movie.id, user_id=session['user_id'])
        #     db.session.add(new_ticket)

        # db.session.commit()
        for _ in range(num_tickets):
            ticket = Ticket(movie_id=movie_id, user_id=session['user_id'], price=movie.price, showtime=screen_time)
            db.session.add(ticket)

        db.session.commit()

        flash(f'{num_tickets} ticket(s) purchased successfully for {movie.title}!', 'success')
        return redirect(url_for('browse_movies'))

    return render_template('purchase_ticket.html', movie=movie)

# Search Movies Route
@app.route('/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('query', '').strip()
    results = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    return render_template('search_results.html', results=results)

# Process Purchase Route
@app.route('/process_purchase', methods=['POST'])
def process_purchase():
    movie_id = request.form.get('movie_id')
    screen_time = request.form.get('screen_time')
    num_tickets = int(request.form.get('num_tickets'))
    theater = request.form.get('theater')

    # Fetch the movie details
    movie = Movie.query.get(movie_id)
    if not movie:
        flash("Movie not found. Please try again.", "danger")
        return redirect(url_for('browse_movies'))

    # Check if the movie price is set
    if movie.price is None:
        flash("Movie price is not set. Please contact support.", "danger")
        return redirect(url_for('browse_movies'))

    # Total cost of tickets
    total_cost = movie.price * num_tickets

    # Create tickets and save to the database
    for _ in range(num_tickets):
        barcode = ''.join(random.choices(string.ascii_letters + string.digits, k=12))  # Generate unique barcode
        ticket = Ticket(
            showtime=screen_time,
            price=movie.price,
            barcode=barcode,
            user_id=session.get('user_id'),
            movie_id=movie.id
        )
        db.session.add(ticket)

    db.session.commit()

    return render_template('payment_confirmation.html',
                           movie=movie,
                           screen_time=screen_time,
                           num_tickets=num_tickets,
                           theater=theater,
                           total_cost=total_cost,
                           barcode=barcode)  # Return the last generated barcode

# @app.route('/process_purchase', methods=['POST'])
# def process_purchase():
#     movie_id = request.form.get('movie_id')
#     screen_time = request.form.get('screen_time')
#     num_tickets = int(request.form.get('num_tickets'))
#     theater = request.form.get('theater')

#     # Fetch the movie details
#     movie = Movie.query.get(movie_id)
#     if not movie:
#         flash("Movie not found. Please try again.", "danger")
#         return redirect(url_for('browse_movies'))

#     # Check if the movie price is set
#     if movie.price is None:
#         flash("Movie price is not set. Please contact support.", "danger")
#         return redirect(url_for('browse_movies'))

#     # Generate a unique barcode
#     barcode = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

#     # Create tickets and save to the database
#     for _ in range(num_tickets):
#         ticket = Ticket(
#             showtime=screen_time,
#             price=movie.price,
#             barcode=barcode,
#             user_id=session.get('user_id'),
#             movie_id=movie.id
#         )
#         db.session.add(ticket)
#     db.session.commit()

#     total_cost = movie.price * num_tickets
#     return render_template('payment_confirmation.html',
#                            movie=movie,
#                            screen_time=screen_time,
#                            num_tickets=num_tickets,
#                            theater=theater,
#                            total_cost=total_cost,
#                            barcode=barcode)



# Admin Dashboard Route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not Admin.query.get(session['user_id']):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('browse_movies'))
    #return render_template('admin_dashboard.html')
    return render_template('admin_dashboard.html', admin=Admin.query.get(session['user_id']))


@app.route('/generate_status_report')
def generate_status_report():
    if 'user_id' not in session or not Admin.query.get(session['user_id']):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('browse_movies'))
    
    now_showing_movies = Movie.query.filter_by(status="Now Showing").all()
    print(f"Now Showing Movies: {now_showing_movies}")  # Debugging line
    
    upcoming_movies = Movie.query.filter_by(status="Upcoming").all()
    #total_tickets = Ticket.query.count()
    total_tickets = db.session.query(Ticket).count()
    total_revenue = db.session.query(db.func.sum(Ticket.price)).scalar() or 0

    return render_template('status_report.html', 
                           now_showing_movies=now_showing_movies,
                           upcoming_movies=upcoming_movies,
                           total_tickets=total_tickets,
                           total_revenue=total_revenue)


# Manage Movies Route
@app.route('/manage_movies', methods=['GET', 'POST'])
def manage_movies():
    # Ensure the user is logged in as an admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('browse_movies'))
    
    movies = Movie.query.all()

    # Adding a new movie
    if request.method == 'POST':
        title = request.form['title']
        synopsis = request.form['synopsis']
        cast = request.form['cast']
        runtime = int(request.form['runtime'])
        status = request.form['status']
        price = float(request.form['price'])
        showtime = request.form['showtime']
        
        # Create and add the new movie
        new_movie = Movie(title=title, synopsis=synopsis, cast=cast, runtime=runtime,
                          status=status, price=price, showtime=showtime)
        db.session.add(new_movie)
        db.session.commit()
        flash(f"Movie '{title}' added successfully!", "success")
        return redirect(url_for('manage_movies'))

    return render_template('manage_movies.html', movies=movies)

# Route to Delete a Movie
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    # Ensure the user is logged in as an admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('browse_movies'))

    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash(f"Movie '{movie.title}' has been deleted.", "success")
    else:
        flash("Movie not found.", "danger")
    return redirect(url_for('manage_movies'))

@app.route('/status_report', methods=['GET'])
def status_report():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('browse_movies'))

    # Retrieve the status data
    total_tickets_sold = Ticket.query.count()
    movies_playing = Movie.query.filter_by(status="Now Showing").all()
    upcoming_movies = Movie.query.filter_by(status="Upcoming").all()
    
    return render_template(
        'status_report.html',
        total_tickets_sold=total_tickets_sold,
        movies_playing=movies_playing,
        upcoming_movies=upcoming_movies
    )


@app.route('/add_review/<int:movie_id>', methods=['POST'])
def add_review(movie_id):
    content = request.form['review_content']  # Make sure the name in the form matches this key
    review = Review(content=content, user_id=session['user_id'], movie_id=movie_id)
    db.session.add(review)
    db.session.commit()
    flash("Review added successfully!", "success")
    return redirect(url_for('movie_details', movie_id=movie_id))


# @app.route('/add_review/<int:movie_id>', methods=['POST'])
# def add_review(movie_id):
#     if 'user_id' not in session:
#         flash('You need to be logged in to write a review.', 'warning')
#         return redirect(url_for('login'))

#     content = request.form['review_content']
#     if not content.strip():
#         flash('Review content cannot be empty.', 'danger')
#         return redirect(url_for('movie_details', movie_id=movie_id))

#     # Save the review to the database
#     review = Review(
#         user_id=session['user_id'],
#         movie_id=movie_id,
#         content=content.strip()
#     )
#     db.session.add(review)
#     db.session.commit()
#     flash('Review added successfully!', 'success')
#     return redirect(url_for('movie_details', movie_id=movie_id))


@app.route('/movie_details/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).all()  # Fetch reviews for the movie
    print("Fetched Reviews:", reviews)  # Debugging
    return render_template('movie_details.html', movie=movie, reviews=reviews)

@app.route('/movie_reviews/<int:movie_id>')
def movie_reviews(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return render_template('movie_reviews.html', movie=movie, reviews=reviews)


# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
