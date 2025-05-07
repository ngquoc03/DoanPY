import sqlite3

def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()

    # Employee table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT,
            salary TEXT
        )
    """)

    # Supplier table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier(
            invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            desc TEXT
        )
    """)

    # Category table (FIXED)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS category(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            supplier TEXT,
            name TEXT NOT NULL,
            price TEXT,
            qty TEXT,
            status TEXT
        )
    """)

    con.commit()
    con.close()

create_db()
