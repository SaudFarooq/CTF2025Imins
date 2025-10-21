from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)
FLAG = "CH{sqli_to_admin}"

LOGIN_TMPL = """
<!doctype html>
<title>Login</title>
<h1>Login</h1>
<form method=post>
  <input name=username placeholder="username">
  <input name=password placeholder="password">
  <button>Login</button>
</form>
<p>Hint: admin has a flag.</p>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string(LOGIN_TMPL)
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # Vulnerable SQLi: string concatenation
    query = f"SELECT id, is_admin FROM users WHERE username = '{username}' AND password = '{password}'"
    with sqlite3.connect('app.db') as conn:
        c = conn.cursor()
        try:
            c.execute(query)
            row = c.fetchone()
        except sqlite3.Error as e:
            return f"SQL error: {e}"
    if row:
        user_id, is_admin = row
        if is_admin:
            return FLAG
        return f"Welcome user {user_id}!"
    return "Invalid credentials"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
