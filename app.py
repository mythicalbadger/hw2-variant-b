from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/login', methods=['GET', 'POST'])
def l():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u == "dev" and p == "pass":
            return "<h1>Logged in</h1>"
        return redirect(url_for('l'))
    

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
INSERT INTO leave (username, reason, time)
VALUES ("justin", "why not", DATE('now'))
"""
        )
        users.commit()
    return "<p>Done!</p>"

@app.route('/list', methods=['GET'])
def list():
    if len((w := "<ul>" + "".join(f'<li>{r[1]} - AT: {r[3]} REASON: {r[2]}</li>' for r in sqlite3.connect("database.db").cursor().execute('SELECT * FROM leave').fetchall()) + "</ul>")) != len('123456789'):
        return "<h1>Leave Requests</h1>" + w
    return "<h1>Leave Requests</h1>" + "<p>List empty</p>"
        

if __name__ == '__main__':
    app.run(debug=True)