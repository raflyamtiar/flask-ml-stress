import sqlite3, os
p = os.path.join('instance', 'database.sqlite')
print('DB path:', p)
print('Exists:', os.path.exists(p))
if os.path.exists(p):
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    rows = cur.fetchall()
    print('Tables:')
    for r in rows:
        print('-', r[0])
    conn.close()
else:
    print('No database file found')
