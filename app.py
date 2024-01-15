from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect('database.db')
connect.executescript(
"""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS leave (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
    reason TEXT NOT NULL,
    time Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""
    )

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/join', methods=['GET'])
def join():
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute(
"""
INSERT INTO users (username)
VALUES ("justin")
"""
        )
        users.commit()
    return "<p>Done!</p>"

@app.route('/leave', methods=['GET', 'POST'])
def leave():
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute(
"""
INSERT INTO users (username, reason)
VALUES ("justin")
"""
        )
        users.commit()
    return "<p>Done!</p>"

if __name__ == '__main__':
    app.run(debug=True)