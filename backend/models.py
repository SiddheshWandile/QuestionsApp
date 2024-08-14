from flask_mysqldb import MySQL
import pymysql
import bcrypt

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Pass@123'
    app.config['MYSQL_DB'] = 'user_auth'

    mysql.init_app(app)

    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD']
        )

        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS user_auth")

        cursor.execute("USE user_auth")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            question_no INT PRIMARY KEY,
            question_name VARCHAR(100),
            source_code TEXT NOT NULL
        )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM Questions")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.executemany("""
            INSERT INTO Questions (question_no, question_name, source_code) VALUES (%s, %s, %s)
            """, [
                (1, 'Binary Search', '# Binary Search Implementation\n\ndef binary_search(arr, x):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == x:\n            return mid\n        elif arr[mid] < x:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1'),
                (2, 'Fibonacci Series', '# Fibonacci Series Implementation\n\ndef fibonacci_series(n):\n    fib_sequence = [0, 1]\n    while len(fib_sequence) < n:\n        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])\n    return fib_sequence[:n]'),
                (3, 'Bubble Sort', '# Bubble Sort Implementation\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr'),
                (4, 'Merge Sort', '# Merge Sort Implementation\n\ndef merge_sort(arr):\n    if len(arr) > 1:\n        mid = len(arr) // 2\n        left_half = arr[:mid]\n        right_half = arr[mid:]\n        merge_sort(left_half)\n        merge_sort(right_half)\n        i = j = k = 0\n        while i < len(left_half) and j < len(right_half):\n            if left_half[i] < right_half[j]:\n                arr[k] = left_half[i]\n                i += 1\n            else:\n                arr[k] = right_half[j]\n                j += 1\n            k += 1\n        while i < len(left_half):\n            arr[k] = left_half[i]\n            i += 1\n            k += 1\n        while j < len(right_half):\n            arr[k] = right_half[j]\n            j += 1\n            k += 1\n    return arr'),
                (5, 'Quick Sort', '# Quick Sort Implementation\n\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    else:\n        pivot = arr[len(arr) // 2]\n        left = [x for x in arr if x < pivot]\n        middle = [x for x in arr if x == pivot]\n        right = [x for x in arr if x > pivot]\n        return quick_sort(left) + middle + quick_sort(right)')
            ])
            print("Questions added to the database.")
        else:
            print("Questions already exist in the database.")

        connection.commit()
        cursor.close()
        connection.close()

    except pymysql.Error as e:
        print(f"Error while connecting to MySQL: {e}")

def register_user(username, password):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM Login WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Username already exists. Registration failed.")
            return False

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO Login (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        mysql.connection.commit()
        cursor.close()

        return True

    except Exception as e:
        print(f"Error during user registration: {e}")
        return False

def validate_login(username, password):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT password FROM Login WHERE username = %s", (username,))
    stored_password = cursor.fetchone()
    cursor.close()

    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8')):
        return True
    else:
        return False

def get_question_source(question_no):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT source_code FROM Questions WHERE question_no = %s", [question_no])
    source_code = cursor.fetchone()
    cursor.close()

    if source_code:
        return source_code[0]
    return None
