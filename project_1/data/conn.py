import psycopg2 as pg

def connect():
    conn = pg.connect(
        host='localhost',
        user='postgres',
        password='pg!password',
        dbname='postgres',
        port='5432'
    )

    return conn

def fetch_diseases(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disease;")
    records = cursor.fetchall()
    print(records)

def insert_disease(conn, overview):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO disease (overview) VALUES ('{overview}')")
    conn.commit()


if __name__ == "__main__":
    conn = connect()
    fetch_diseases(conn)
    insert_disease(conn, "exemplo3")
    fetch_diseases(conn)