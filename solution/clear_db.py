import sqlite3
conn = sqlite3.connect('growls.db')

c = conn.cursor()
c.execute("DROP TABLE growls")
conn.commit()
conn.close()
