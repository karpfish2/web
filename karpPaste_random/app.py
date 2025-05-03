from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random
import sqlite3
import os
import secrets

# Get the absolute path to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'pastes.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline';"
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

# Database setup
def get_db():
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    try:
        db.execute('''
            CREATE TABLE IF NOT EXISTS pastes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
    finally:
        db.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pastes', methods=['GET', 'POST'])
def handle_pastes():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        
        if not text:
            return render_template('index.html', message='Текст не может быть пустым')
        
        if len(text) > 1000000:  # 1 million characters
            return render_template('index.html', message='Текст слишком длинный (максимум 1 000 000 символов)')
        
        db = get_db()
        try:
            db.execute('INSERT INTO pastes (text) VALUES (?)', (text,))
            db.commit()
        finally:
            db.close()
        
        return render_template('index.html', message='Паста успешно сохранена!')
    
    return redirect(url_for('index'))

@app.route('/api/pastes/random', methods=['GET'])
def get_random_paste():
    db = get_db()
    try:
        cursor = db.execute('SELECT COUNT(*) as count FROM pastes')
        count = cursor.fetchone()['count']
        
        if count == 0:
            return render_template('index.html', message='Нет доступных паст')
        
        # Get random offset
        offset = random.randint(0, count - 1)
        cursor = db.execute('SELECT text FROM pastes LIMIT 1 OFFSET ?', (offset,))
        random_paste = cursor.fetchone()
        
        return render_template('index.html', random_paste={'text': random_paste['text']})
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000) 