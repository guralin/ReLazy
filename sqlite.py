import sqlite3

conn = sqlite3.connect('st.db')

c = conn.cursor()
c.execute('''INSERT INTO test values("hei","hei");''')
c.execute('''SELECT * FROM test''')
data = c.fetchall()
print(data)

conn.commit()
conn.close()


