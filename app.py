from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

connect = sqlite3.connect('database.db')
connect.executescript("""
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS leave (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, reason TEXT NOT NULL, time Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);
""")


@app.route("/")
def main():
    return "<p>Hello, World!</p>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return "<h1>Logged in</h1>"
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user_in_db = sqlite3.connect("database.db").cursor().execute(
                f'SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
            print(user_in_db[1], user_in_db[2])
            if user_in_db:
                session["user"] = username
                return "<h1>Logged in</h1>"
        except:
            return redirect(url_for('login'))
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    session["user"] = None
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect("database.db") as db:
            db.cursor().execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            session["user"] = username
        return redirect(url_for('login'))


@app.route('/current_user')
def current_user():
    user = "None" if session["user"] == None else session["user"]
    if "user" in session:
        return "<h1>" + user + "</h1>"
    return redirect(url_for('login'))


@app.route('/create_leave_request', methods=['GET', 'POST'])
def create_leave_request():
    if "user" in session:
        if request.method == 'GET':
            return render_template('create_leave_request.html')
        elif request.method == 'POST':
            r = request.form['reason']
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute("""
        INSERT INTO leave (username, reason, time) VALUES (?, ?, DATE('now'))
    """, (session["user"], r))
                users.commit()
            return redirect(url_for('my_leave_requests'))
    return redirect(url_for('login'))


@app.route('/my_leave_requests', methods=['GET'])
def my_leave_requests():
    if "user" in session:
        if len((w := "<ul>" + "".join(f'<li>{r[1]} - AT: {r[3]} REASON: {r[2]}</li>' for r in
                                      sqlite3.connect("database.db").cursor().execute(
                                              'SELECT * FROM leave WHERE username = ?',
                                              (session["user"],)).fetchall()) + "</ul>")) != len('123456789'):
            return "<h1>Leave Requests</h1>" + w
        return "<h1>Leave Requests</h1>" + "<p>List empty</p>"
    return redirect(url_for('login'))


@app.route('/leave_requests', methods=['GET'])
def leave_requests():
    if "user" in session:
        if len((w := "<ul>" + "".join(f'<li>{r[1]} - AT: {r[3]} REASON: {r[2]}</li>' for r in
                                      sqlite3.connect("database.db").cursor().execute(
                                              'SELECT * FROM leave WHERE username != ?',
                                              (session["user"],)).fetchall()) + "</ul>")) != len('123456789'):
            return "<h1>Leave Requests</h1>" + w
        return "<h1>Leave Requests</h1>" + "<p>List empty</p>"
    return redirect(url_for('login'))


@app.route('/users', methods=['GET'])
def users():
    if len((w := "<ul>" + "".join(f'<li>{r[1]}</li>' for r in sqlite3.connect("database.db").cursor().execute(
            'SELECT * FROM users').fetchall()) + "</ul>")) != len('123456789'):
        return "<h1>Users</h1>" + w
    return "<h1>Users</h1>" + "<p>List empty</p>"


if __name__ == '__main__':
    app.run(debug=True)
