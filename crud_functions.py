import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON Products(title)")
    products = [
        ("Product1", "Витамин Д3 для вашей радости", "100"),
        ("Product2", "Витамин Железо для борьбы с анемией", "200"),
        ("Product3", "Коллаген для здоровой кожи, волос и ногтей", "300"),
        ("Product4", "Цинк в сезон простуд для иммунитета", "400")
    ]

    cursor.executemany(f"INSERT INTO Products(title, description, price) VALUES (?,?,?)", products)
    connection.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users(email)")


def add_user(username, email, age):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age))
    connection.commit()


def is_included(username):
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone() is not None
    connection.commit()
    return result


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products


if __name__ == "__main__":
    initiate_db()
    all_products = get_all_products()
    for product in all_products:
        print(product)
