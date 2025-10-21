from flask import Flask, request, render_template_string, session, redirect, url_for
import os
import subprocess
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ssti_challenge_secret_key_2024'

# Create flag file
def create_flag_file():
    with open('flag.txt', 'w') as f:
        f.write('CTF{s3rv3r_s1d3_t3mpl4t3_1nj3ct10n_pwn3d}')
    
    with open('secret_admin_flag.txt', 'w') as f:
        f.write('CTF{4dv4nc3d_ssti_c0d3_3x3cut10n}')

create_flag_file()

# User database
users = {
    'admin': {'password': 'admin_secure_2024', 'role': 'administrator'},
    'user': {'password': 'user123', 'role': 'user'},
    'guest': {'password': 'guest', 'role': 'guest'}
}

MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TemplateEngine - Dynamic Content Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 15px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }
        .nav {
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            padding: 0;
        }
        .nav ul {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            justify-content: center;
        }
        .nav li {
            margin: 0;
        }
        .nav a {
            display: block;
            padding: 15px 25px;
            text-decoration: none;
            color: #495057;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .nav a:hover, .nav a.active {
            background: #e9ecef;
            border-bottom-color: #ff6b6b;
            color: #ff6b6b;
        }
        .content {
            flex: 1;
            padding: 40px;
        }
        .generator-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            border-left: 4px solid #ff6b6b;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        input[type="text"], textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        textarea {
            height: 120px;
            resize: vertical;
            font-family: 'Courier New', monospace;
        }
        input[type="text"]:focus, textarea:focus, select:focus {
            border-color: #ff6b6b;
            outline: none;
        }
        .generate-btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        .generate-btn:hover {
            opacity: 0.9;
        }
        .output {
            background: #f1f3f4;
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 25px;
            margin-top: 25px;
            min-height: 100px;
        }
        .output h3 {
            margin-top: 0;
            color: #333;
        }
        .hint-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .hint-box h3 {
            margin: 0 0 15px 0;
            color: #856404;
        }
        .hint-box p {
            margin: 8px 0;
            color: #856404;
        }
        .hint-box code {
            background: rgba(0,0,0,0.1);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .login-section {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .user-info {
            background: #e8f5e8;
            border: 1px solid #c8e6c9;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 TemplateEngine</h1>
            <p>Dynamic Content Generator with Advanced Template Processing</p>
        </div>
        
        <nav class="nav">
            <ul>
                <li><a href="/" class="active">Generator</a></li>
                <li><a href="/examples">Examples</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
        
        <div class="content">
            {% if not session.get('username') %}
            <div class="login-section">
                <h3>🔐 Login Required</h3>
                <p>Please login to use the template generator:</p>
                <form method="POST" action="/login" style="display: inline-block; margin-right: 20px;">
                    <input type="hidden" name="username" value="guest">
                    <input type="hidden" name="password" value="guest">
                    <button type="submit" class="generate-btn">Login as Guest</button>
                </form>
                <form method="POST" action="/login" style="display: inline-block;">
                    <input type="text" name="username" placeholder="Username" style="width: 120px; margin-right: 10px;">
                    <input type="password" name="password" placeholder="Password" style="width: 120px; margin-right: 10px;">
                    <button type="submit" class="generate-btn">Login</button>
                </form>
            </div>
            {% else %}
            <div class="user-info">
                <strong>👤 Logged in as:</strong> {{ session.username }} 
                <a href="/logout" style="margin-left: 20px; color: #ff6b6b;">Logout</a>
            </div>
            {% endif %}
            
            <div class="hint-box">
                <h3>🎯 Challenge Hint</h3>
                <p><strong>Objective:</strong> Exploit Server-Side Template Injection (SSTI) to execute code and find the flag!</p>
                <p><strong>Hint 1:</strong> This application uses Jinja2 templates to render user input</p>
                <p><strong>Hint 2:</strong> Try template expressions like <code>{{ 7*7 }}</code> in your input</p>
                <p><strong>Hint 3:</strong> Explore the template context with <code>{{ config }}</code> or <code>{{ self }}</code></p>
                <p><strong>Hint 4:</strong> Use <code>{{ ''.__class__.__mro__[1].__subclasses__() }}</code> to find useful classes</p>
                <p><strong>Hint 5:</strong> Look for file reading capabilities or command execution</p>
                <p><strong>Hint 6:</strong> The flag might be in flag.txt or you might need to execute system commands</p>
            </div>
            
            {% if session.get('username') %}
            <div class="generator-section">
                <h2>📝 Template Generator</h2>
                <form method="POST" action="/generate">
                    <div class="form-group">
                        <label for="template_type">Template Type:</label>
                        <select id="template_type" name="template_type">
                            <option value="greeting">Greeting Message</option>
                            <option value="report">Report Template</option>
                            <option value="email">Email Template</option>
                            <option value="custom">Custom Template</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="user_input">Your Content:</label>
                        <textarea id="user_input" name="user_input" placeholder="Enter your content here... You can use template variables like {{ name }} or {{ date }}">{{ user_input or '' }}</textarea>
                    </div>
                    <div class="form-group">
                        <label for="name">Name (optional):</label>
                        <input type="text" id="name" name="name" placeholder="Enter a name" value="{{ name or '' }}">
                    </div>
                    <button type="submit" class="generate-btn">Generate Template</button>
                </form>
            </div>
            
            {% if output %}
            <div class="output">
                <h3>📄 Generated Output:</h3>
                {{ output|safe }}
            </div>
            {% endif %}
            
            {% if error %}
            <div class="error">
                <strong>Template Error:</strong> {{ error }}
            </div>
            {% endif %}
            {% endif %}
        </div>
        
        <div class="footer">
            © 2024 TemplateEngine Inc. Powered by Advanced Template Processing
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(MAIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['role'] = users[username]['role']
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    template_type = request.form.get('template_type', 'custom')
    user_input = request.form.get('user_input', '')
    name = request.form.get('name', 'User')
    
    output = ''
    error = None
    
    try:
        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Prepare template context
        template_context = {
            'name': name,
            'date': current_date,
            'username': session.get('username'),
            'role': session.get('role'),
            'template_type': template_type
        }
        
        # Create the template based on type
        if template_type == 'greeting':
            template = f"Hello {name}! Welcome to our service. {user_input}"
        elif template_type == 'report':
            template = f"Report generated on {current_date} by {session.get('username')}. Content: {user_input}"
        elif template_type == 'email':
            template = f"Dear {name}, {user_input} Best regards, {session.get('username')}"
        else:  # custom
            template = user_input
        
        # VULNERABLE: Direct template rendering without sanitization
        # This allows Server-Side Template Injection (SSTI)
        output = render_template_string(template, **template_context)
        
    except Exception as e:
        error = str(e)
    
    return render_template_string(MAIN_TEMPLATE, 
                                output=output, 
                                error=error,
                                user_input=user_input,
                                name=name)

@app.route('/examples')
def examples():
    examples_content = '''
    <div class="generator-section">
        <h2>📚 Template Examples</h2>
        <h3>Basic Variables:</h3>
        <ul>
            <li><code>{{ name }}</code> - Display the name</li>
            <li><code>{{ date }}</code> - Display current date</li>
            <li><code>{{ username }}</code> - Display logged-in username</li>
        </ul>
        
        <h3>Mathematical Operations:</h3>
        <ul>
            <li><code>{{ 7 * 7 }}</code> - Perform calculations</li>
            <li><code>{{ range(5) }}</code> - Generate ranges</li>
        </ul>
        
        <h3>Advanced Examples:</h3>
        <ul>
            <li><code>Hello {{ name }}, today is {{ date }}</code></li>
            <li><code>Welcome {{ username }}, you have {{ role }} privileges</code></li>
        </ul>
    </div>
    '''
    
    return render_template_string(MAIN_TEMPLATE.replace('{{ output|safe }}', examples_content))

@app.route('/docs')
def docs():
    docs_content = '''
    <div class="generator-section">
        <h2>📖 Documentation</h2>
        <h3>Template Syntax:</h3>
        <p>Our template engine supports Jinja2 syntax:</p>
        <ul>
            <li><strong>Variables:</strong> <code>{{ variable_name }}</code></li>
            <li><strong>Expressions:</strong> <code>{{ 2 + 2 }}</code></li>
            <li><strong>Filters:</strong> <code>{{ name|upper }}</code></li>
            <li><strong>Functions:</strong> <code>{{ range(10) }}</code></li>
        </ul>
        
        <h3>Available Context:</h3>
        <ul>
            <li><code>name</code> - User provided name</li>
            <li><code>date</code> - Current date</li>
            <li><code>username</code> - Logged-in username</li>
            <li><code>role</code> - User role</li>
            <li><code>template_type</code> - Selected template type</li>
        </ul>
        
        <h3>Security Notice:</h3>
        <p><em>This is a demo application. In production, always sanitize user input!</em></p>
    </div>
    '''
    
    return render_template_string(MAIN_TEMPLATE.replace('{{ output|safe }}', docs_content))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)