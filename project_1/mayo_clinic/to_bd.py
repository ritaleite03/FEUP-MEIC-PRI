import sqlite3
import pandas as pd
import sqlite3

conn = sqlite3.connect('mayoclinic.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    overview TEXT,
    symptoms TEXT,
    causes TEXT,
    risk_factors TEXT,
    complications TEXT,
    prevention TEXT
);
''')


df = pd.read_csv('diseases_info.csv')
df.rename(columns={'Risk factors': 'risk_factors'}, inplace=True)
df.to_sql('diseases', conn, if_exists='append', index=False)

conn.commit()


cur.execute('SELECT symptoms FROM diseases LIMIT 1;')
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
