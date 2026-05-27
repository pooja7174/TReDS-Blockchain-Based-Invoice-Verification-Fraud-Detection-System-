import sqlite3


def connect_db():

    conn = sqlite3.connect('treds.db')

    return conn


def create_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            invoice_id TEXT,
            company TEXT,
            amount TEXT,
            buyer TEXT,
            status TEXT
        )
    ''')

    conn.commit()

    conn.close()


def insert_invoice(invoice_id, company, amount, buyer, status):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO invoices
        (invoice_id, company, amount, buyer, status)

        VALUES (?, ?, ?, ?, ?)
    ''', (invoice_id, company, amount, buyer, status))

    conn.commit()

    conn.close()


def get_all_invoices():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM invoices')

    invoices = cursor.fetchall()

    conn.close()

    return invoices


def update_invoice_status(invoice_id, new_status):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE invoices
        SET status = ?
        WHERE invoice_id = ?
        ''',
        (new_status, invoice_id)
    )

    conn.commit()

    conn.close()

def update_invoice_status(invoice_id, new_status):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute('''
        UPDATE invoices
        SET status = ?
        WHERE invoice_id = ?
    ''', (new_status, invoice_id))

    conn.commit()

    conn.close()

def update_invoice_status(invoice_id, status):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE invoices
        SET status = ?
        WHERE invoice_id = ?
        ''',
        (status, invoice_id)
    )

    conn.commit()

    conn.close()