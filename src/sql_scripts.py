class SQLScripts:
    create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL, remaining_leave_days INTEGER NOT NULL);"
    create_leave_table = "CREATE TABLE IF NOT EXISTS leave (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, reason TEXT NOT NULL, time Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);"
    is_user_in_db = "SELECT * FROM users WHERE username = ? AND password = ?;"
    is_leave_request_in_db = "SELECT * FROM leave WHERE username = ? AND time = ?;"
    insert_user = "INSERT INTO users (username, password, remaining_leave_days) VALUES (?, ?, 10);"
    insert_leave = "INSERT INTO leave (username, reason, time) VALUES (?, ?, ?);"
    get_leave_by_username = "SELECT * FROM leave WHERE username = ?;"
    get_leave_by_id = "SELECT * FROM leave WHERE id = ?;"
    get_user_by_username = "SELECT * FROM users WHERE username = ?;"
    get_all_leave_requests = "SELECT * FROM leave;"
    get_all_users = "SELECT * FROM users;"
    update_leave_days_for_user = "UPDATE users SET remaining_leave_days = ? WHERE username = ?;"
    delete_leave_request = "DELETE FROM leave WHERE id = ?;"