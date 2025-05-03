from app import app
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'pastes.db')

if __name__ == '__main__':
    db = sqlite3.connect(DATABASE_PATH)
    app.run(debug=False, host='127.0.0.1', port=5000) 