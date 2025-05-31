import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_new_user_with_old_login():
    add_user('test', 'test', 'test')
    assert add_user('test', 'test', 'test') == False

def test_autenficacia():
    add_user('test', 'test', 'test')
    assert authenticate_user('test','test')
# Возможные варианты тестов:

def test_nonuser_autenficacia():
    assert authenticate_user('grigoriy_malcov','grigoriy_malcov.com') == False

# def test_spisoc(setup_database, connection):
#     cursor = connection.cursor()
#     cursor.execute('SELECT username, email FROM users')
#     cur = cursor.fetchall()
#     assert display_users == print(f"Логин: {user[0]}, Электронная почта: {user[1]}") for user in cur 
            
