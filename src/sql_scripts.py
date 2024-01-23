class SQLScripts:
    create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);"

    create_leave_table = "CREATE TABLE IF NOT EXISTS leave (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, reason TEXT NOT NULL, time Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);"

    is_user_in_db = "SELECT * FROM users WHERE username = ? AND password = ?;"
    insert_user = "INSERT INTO users (username, password) VALUES (?, ?);"
    insert_leave = "INSERT INTO leave (username, reason, time) VALUES (?, ?, ?);"
    get_leave_by_username = "SELECT * FROM leave WHERE username = ?;"
    get_all_leave_requests = "SELECT * FROM leave;"
    get_all_users = "SELECT * FROM users;"