from flask import Flask, request, render_template_string, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_ctf'

# Simple user database
users = {
    'admin': 'super_secure_password_2024',
    'guest': 'guest123',
    'user': 'password'
}

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureBank Login</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            padding: 40px;
            width: 400px;
            text-align: center;
        }
        .logo {
            font-size: 2em;
            color: #1e3c72;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #1e3c72;
            outline: none;
        }
        .login-btn {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        .login-btn:hover {
            opacity: 0.9;
        }
        .error {
            color: #e74c3c;
            margin-top: 15px;
            padding: 10px;
            background: #fdf2f2;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }
        .hint {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
        }
        .footer {
            margin-top: 30px;
            font-size: 0.8em;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🏦 SecureBank</div>
        <div class="subtitle">Secure Online Banking Portal</div>
        
        <form method="POST" action="/">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="login-btn">Login</button>
        </form>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <div class="hint">
            💡 <strong>Hint:</strong> Sometimes the simplest approaches work best!<br>
            Try common usernames like 'admin' or see what happens with special characters.
        </div>
        
        <div class="footer">
            © 2024 SecureBank. All rights reserved.<br>
            <small>Demo version - Not for production use</small>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureBank Dashboard</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .dashboard {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
        }
        .logo {
            font-size: 1.8em;
            color: #1e3c72;
            font-weight: bold;
        }
        .user-info {
            color: #666;
        }
        .welcome {
            font-size: 1.3em;
            margin-bottom: 20px;
            color: #333;
        }
        .flag-section {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }
        .flag {
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            font-weight: bold;
            background: rgba(255,255,255,0.2);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .logout-btn {
            background: #e74c3c;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .logout-btn:hover {
            background: #c0392b;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="logo">🏦 SecureBank</div>
            <div class="user-info">
                Welcome, {{ username }}!
                <a href="/logout" class="logout-btn">Logout</a>
            </div>
        </div>
        
        <div class="welcome">
            🎉 Congratulations! You've successfully bypassed our authentication!
        </div>
        
        <div class="flag-section">
            <h2>🚩 Your Flag</h2>
            <div class="flag">CTF{4uth_byp4ss_1s_34sy_w1th_0r}</div>
            <p>Well done! You discovered that OR-based authentication bypass still works!</p>
        </div>
        
        <div>
            <h3>What you learned:</h3>
            <ul>
                <li>SQL injection in authentication forms</li>
                <li>Using OR conditions to bypass login checks</li>
                <li>The importance of parameterized queries</li>
                <li>Input validation and sanitization</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable authentication logic
        # This simulates a SQL injection vulnerability
        if "'" in username or "'" in password:
            # Simple SQL injection simulation
            if " or " in username.lower() or " or " in password.lower():
                session['username'] = username
                return redirect(url_for('dashboard'))
        
        # Normal authentication
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        return render_template_string(LOGIN_TEMPLATE, error="Invalid username or password!")
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)