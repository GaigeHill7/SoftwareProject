from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Admin, Movie, Ticket, Payment, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_booking.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)


# Home Route
@app.route('/')
def home():
    return render_template('home.html')  # Home page with navigation


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))
        
        # Add user to database
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from the form
        name = request.form['username']
        password = request.form['password']
        
        # Verify user credentials
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')



# Browse Movies
@app.route('/browse_movies')
def browse_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)


# Movie Details
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('browse_movies'))
    return render_template('movie_details.html', movie=movie)


# Purchase Ticket
@app.route('/purchase_ticket/<int:movie_id>', methods=['GET', 'POST'])
def purchase_ticket(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('browse_movies'))

    if request.method == 'POST':
        showtime = request.form['showtime']
        num_seats = int(request.form['num_seats'])
        price = 10.0 * num_seats  # Assume a fixed price per seat
        
        # Create ticket and add to database
        new_ticket = Ticket(showtime=showtime, num_seats=num_seats, price=price, user_id=session.get('user_id'), barcode='12345678')
        db.session.add(new_ticket)
        db.session.commit()
        
        flash('Ticket purchased successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('purchase_ticket.html', movie=movie)


# Admin Dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_movie':
            title = request.form['title']
            synopsis = request.form['synopsis']
            runtime = request.form['runtime']
            new_movie = Movie(title=title, synopsis=synopsis, runtime=int(runtime))
            db.session.add(new_movie)
            db.session.commit()
            flash('Movie added successfully!', 'success')
        
        elif action == 'remove_movie':
            movie_id = int(request.form['movie_id'])
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                flash('Movie removed successfully!', 'success')
            else:
                flash('Movie not found!', 'danger')
    
    movies = Movie.query.all()
    return render_template('admin_dashboard.html', movies=movies)


# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
