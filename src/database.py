import datetime
import sqlite3
from src.sql_scripts import SQLScripts

connection = sqlite3.connect('database.db', check_same_thread=False)
connection.row_factory = sqlite3.Row


def create_tables() -> None:
    connection.execute(SQLScripts.create_users_table)
    connection.execute(SQLScripts.create_leave_table)


def is_user_in_db(username: str, password: str) -> bool:
    return connection.execute(SQLScripts.is_user_in_db, (username, password)).fetchone() is not None


def create_user(username: str, password: str) -> None:
    connection.execute(SQLScripts.insert_user, (username, password))
    connection.commit()


def create_leave(username: str, reason: str, time: datetime.datetime) -> None:
    connection.execute(SQLScripts.insert_leave, (username, reason, time))
    connection.commit()


def delete_leave(leave_id: int) -> None:
    connection.execute(SQLScripts.delete_leave_request, (leave_id,))
    connection.commit()


def get_leave_by_username(username: str) -> list:
    return connection.execute(SQLScripts.get_leave_by_username, (username,)).fetchall()


def get_leave_by_id(leave_id: int) -> dict:
    return connection.execute(SQLScripts.get_leave_by_id, (leave_id,)).fetchone()

def leave_request_exists(username: str, time: datetime) -> bool:
    return connection.execute(SQLScripts.is_leave_request_in_db, (username, time)).fetchone() is not None


def get_user_by_username(username: str) -> dict:
    return connection.execute(SQLScripts.get_user_by_username, (username,)).fetchone()


def get_all_leave_requests() -> list:
    return connection.execute(SQLScripts.get_all_leave_requests).fetchall()


def get_all_users() -> list:
    return connection.execute(SQLScripts.get_all_users).fetchall()


def update_remaining_leave_days(username: str, days: int) -> None:
    connection.execute(SQLScripts.update_leave_days_for_user, (days, username))
    connection.commit()
   