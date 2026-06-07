import sqlite3

conn = sqlite3.connect("D:\\email look\\email-insight\\backend\\email_insight.db")
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print("Tables:", tables)

for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    count = cur.fetchone()[0]
    print(f"  {t}: {count} rows")

if "users" in tables:
    cur.execute("SELECT id, email, username FROM users")
    for row in cur.fetchall():
        print(f"  User: id={row[0]}, email={row[1]}, username={row[2]}")

conn.close()
