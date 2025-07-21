import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="password", host="localhost")
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cur.fetchall()
print("Tables:", tables)

cur.execute("SELECT * FROM customer LIMIT 5;")
print(cur.fetchall())

cur.close()
conn.close()

