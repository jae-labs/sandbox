import sqlite3


def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SEMGREP TRIGGER: String formatting into an execute call
    # Rule: python.lang.security.audit.sqli.sqlite-string-format
    query = "SELECT * FROM users WHERE id = %s" % user_id
    cursor.execute(query)

    return cursor.fetchone()
