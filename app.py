from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

csrf = CSRFProtect(app)

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True

def validate_email(email):
    if not email or len(email) > 100:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return password and len(password) >= 7

def sanitize_input(text, max_length=1000):
    if not text:
        return ""
    text = text.replace('\x00', '')
    text = text[:max_length]
    text = text.strip()
    return text

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Πρέπει να συνδεθείς πρώτα!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Πρέπει να συνδεθείς πρώτα!', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Δεν έχεις δικαίωμα πρόσβασης!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def set_security_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'self'; form-action 'self'"
    return response

def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        role = 'user'

        if not validate_username(username):
            flash('Username: 3-20 χαρακτήρες, μόνο γράμματα, αριθμοί και underscore!', 'error')
            return render_template('register.html')

        if not validate_email(email):
            flash('Μη έγκυρο email!', 'error')
            return render_template('register.html')

        if not validate_password(password):
            flash('Ο κωδικός πρέπει να έχει τουλάχιστον 7 χαρακτήρες!', 'error')
            return render_template('register.html')

        username = sanitize_input(username, 20)
        email = sanitize_input(email, 100)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                (username, hashed_password, email, role)
            )
            conn.commit()
            flash('Η εγγραφή ολοκληρώθηκε!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Το username υπάρχει ήδη!', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Συμπλήρωσε username και password!', 'error')
            return render_template('login.html')

        username = sanitize_input(username, 20)

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Καλώς ήρθες!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Λάθος username ή password!', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Αποσυνδέθηκες!', 'success')
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    conn = get_db()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template('post.html', post=post)

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or len(title) < 3 or len(title) > 200:
            flash('Ο τίτλος πρέπει να είναι 3-200 χαρακτήρες!', 'error')
            return render_template('new_post.html')

        if not content or len(content) < 10 or len(content) > 10000:
            flash('Το περιεχόμενο πρέπει να είναι 10-10000 χαρακτήρες!', 'error')
            return render_template('new_post.html')

        title = sanitize_input(title, 200)
        content = sanitize_input(content, 10000)

        conn = get_db()
        conn.execute(
            'INSERT INTO posts (title, content, author, user_id) VALUES (?, ?, ?, ?)',
            (title, content, session['username'], session['user_id'])
        )
        conn.commit()
        conn.close()

        flash('Το post δημιουργήθηκε!', 'success')
        return redirect(url_for('index'))

    return render_template('new_post.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    conn = get_db()
    post = conn.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()

    if post and (session.get('role') == 'admin' or post['user_id'] == session['user_id']):
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        flash('Το post διαγράφηκε!', 'success')
    else:
        flash('Δεν μπορείς να διαγράψεις αυτό το post!', 'error')

    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)