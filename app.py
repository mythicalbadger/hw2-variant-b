from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

connect = sqlite3.connect('database.db')
connect.executescript(
"""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL
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
    if "user" in session:
        return "<h1>Logged in</h1>"
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        try:
            udb = sqlite3.connect("database.db").cursor().execute(f'SELECT * FROM users WHERE username = ? AND password = ?', (u, p)).fetchone()
            print(udb[1], udb[2])
            if udb:
                session["user"] = u
                return "<h1>Logged in</h1>"
        except:
            return redirect(url_for('l'))
        return redirect(url_for('l'))

@app.route('/logout', methods=['GET'])
def out():
    session.pop("user", None)
    return redirect(url_for('l'))


@app.route('/register', methods=['GET', 'POST'])
def r():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        with sqlite3.connect("database.db") as users:
            users.cursor().execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            users.commit()
            session["user"] = u
        return redirect(url_for('l'))
    
@app.route('/current_user')
def current_user():
    if "user" in session:
        return "<h1>" + session["user"] + "</h1>"
    return redirect(url_for('l'))
@app.route('/join', methods=['GET'])
def join():
    if "user" in session:
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
    return  redirect(url_for('l'))

@app.route('/leave', methods=['GET', 'POST'])
def leave():
    if "user" in session:
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
    return redirect(url_for('l'))

@app.route('/list', methods=['GET'])
def list():
    if "user" in session:
        if len((w := "<ul>" + "".join(f'<li>{r[1]} - AT: {r[3]} REASON: {r[2]}</li>' for r in sqlite3.connect("database.db").cursor().execute('SELECT * FROM leave').fetchall()) + "</ul>")) != len('123456789'):
            return "<h1>Leave Requests</h1>" + w
        return "<h1>Leave Requests</h1>" + "<p>List empty</p>"
    return redirect(url_for('l'))

@app.route('/users', methods=['GET'])
def users():
    if len((w := "<ul>" + "".join(f'<li>{r[1]}</li>' for r in sqlite3.connect("database.db").cursor().execute('SELECT * FROM users').fetchall()) + "</ul>")) != len('123456789'):
        return "<h1>Users</h1>" + w
    return "<h1>Users</h1>" + "<p>List empty</p>"
        

if __name__ == '__main__':
    app.run(debug=True)