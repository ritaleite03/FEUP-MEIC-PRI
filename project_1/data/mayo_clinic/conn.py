import psycopg2 as pg

def connect_to_db():
    try:
        conn = pg.connect(
            host='localhost',
            user='postgres',
            password='p.postgres',
            dbname='postgres_db',
            port='5432'
        )

        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to mayo_clinic db: {e}")

    return conn, cursor

def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()

def fetch_diseases(cursor):
    cursor.execute("SELECT * FROM disease;")
    records = cursor.fetchall()
    print(records)

def insert_disease(conn, cursor, overview):
    cursor.execute(f"INSERT INTO disease (overview) VALUES ('{overview}')")
    conn.commit()

if __name__ == "__main__":
    conn, cursor = connect_to_db()
    fetch_diseases(cursor)
    insert_disease(conn, cursor, "exemplo1")
    fetch_diseases(cursor)
    close_db_connection(conn, cursor)
