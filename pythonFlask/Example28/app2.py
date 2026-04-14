import sqlite3

conn=sqlite3.connect("stage4.db")
cur=conn.cursor()

cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)




# You can see the hashed password here