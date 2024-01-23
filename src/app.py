from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session

import database

app = Flask(__name__)
app.secret_key = "secret"

database.create_tables()


@app.route("/")
def main():
    return "<p>Hello, World!</p>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('my_leave_requests'))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if database.is_user_in_db(username=username, password=password):
            session["user"] = username
            return redirect(url_for('my_leave_requests'))
        else:
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

        if database.is_user_in_db(username=username, password=password):
            return redirect(url_for('register'))

        database.create_user(username, password)
        session["user"] = username

        return redirect(url_for('login'))


@app.route('/current_user')
def current_user():
    if "user" not in session:
        return redirect(url_for('login'))
    return "<h1>" + session["user"] + "</h1>"


@app.route('/create_leave_request', methods=['GET', 'POST'])
def create_leave_request():
    if "user" not in session:
        return redirect(url_for('login'))

    user = database.get_user_by_username(username=session['user'])

    if request.method == 'GET':
        return render_template('create_leave_request.html')
    elif request.method == 'POST':
        reason = request.form['reason']
        time = datetime.strptime(request.form['time'], "%Y-%m-%d")
        database.create_leave(username=session['user'], reason=reason, time=time)
        database.update_remaining_leave_days(username=session['user'], days=user['remaining_leave_days'] - 1)
        return redirect(url_for('my_leave_requests'))


@app.route('/my_leave_requests', methods=['GET'])
def my_leave_requests():
    if "user" not in session:
        return redirect(url_for('login'))

    requests = database.get_leave_by_username(username=session['user'])
    return render_template('my_leave_requests.html', requests=requests)


@app.route('/leave_requests', methods=['GET'])
def leave_requests():
    if "user" not in session:
        return redirect(url_for('login'))

    requests = database.get_all_leave_requests()
    return render_template('leave_requests.html', requests=requests)


@app.route('/users', methods=['GET'])
def list_users():
    if "user" not in session:
        return redirect(url_for('login'))

    users = database.get_all_users()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
