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

    con.commit()
    con.close()

create_db()
