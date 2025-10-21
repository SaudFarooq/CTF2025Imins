from flask import Flask, request, render_template_string, send_file
import os
import base64

app = Flask(__name__)

# Create some sample files
def create_sample_files():
    os.makedirs('pages', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    
    # Sample page files
    with open('pages/home.html', 'w') as f:
        f.write('''
        <div class="page-content">
            <h2>🏠 Welcome to FileShare</h2>
            <p>FileShare is a secure document management system designed for businesses.</p>
            <h3>Features:</h3>
            <ul>
                <li>📁 Secure file storage</li>
                <li>🔐 Access control</li>
                <li>📊 Activity logging</li>
                <li>🌐 Web-based interface</li>
            </ul>
            <p>Use the navigation menu to explore different sections of our platform.</p>
        </div>
        ''')
    
    with open('pages/about.html', 'w') as f:
        f.write('''
        <div class="page-content">
            <h2>📋 About FileShare</h2>
            <p>FileShare was founded in 2024 with the mission of providing secure file management solutions.</p>
            <h3>Our Team:</h3>
            <ul>
                <li>John Smith - CEO</li>
                <li>Jane Doe - CTO</li>
                <li>Bob Wilson - Security Engineer</li>
            </ul>
            <p>We pride ourselves on security and reliability.</p>
        </div>
        ''')
    
    with open('pages/contact.html', 'w') as f:
        f.write('''
        <div class="page-content">
            <h2>📞 Contact Us</h2>
            <p>Get in touch with our support team:</p>
            <ul>
                <li>📧 Email: support@fileshare.com</li>
                <li>📱 Phone: +1 (555) 123-4567</li>
                <li>🏢 Address: 123 Security St, Cyber City, CC 12345</li>
            </ul>
            <p>Our support team is available 24/7 to assist you.</p>
        </div>
        ''')
    
    # Log files
    with open('logs/access.log', 'w') as f:
        f.write('''2024-10-21 10:30:15 - INFO - User admin logged in from 192.168.1.100
2024-10-21 10:31:22 - INFO - File document.pdf accessed by admin
2024-10-21 10:32:45 - WARNING - Failed login attempt for user 'guest' from 192.168.1.105
2024-10-21 10:33:12 - INFO - User manager logged in from 192.168.1.102
2024-10-21 10:34:33 - ERROR - Database connection failed
2024-10-21 10:35:44 - INFO - System backup completed successfully
2024-10-21 10:36:55 - WARNING - Unusual file access pattern detected
''')
    
    with open('logs/error.log', 'w') as f:
        f.write('''2024-10-21 09:15:23 - ERROR - Failed to load configuration file
2024-10-21 09:20:11 - ERROR - Database timeout occurred
2024-10-21 09:25:44 - CRITICAL - Security breach attempt detected
2024-10-21 09:30:15 - ERROR - File not found: /secure/admin_notes.txt
2024-10-21 09:35:22 - WARNING - Multiple failed authentication attempts
2024-10-21 09:40:33 - ERROR - Permission denied accessing /etc/passwd
''')
    
    # Config files
    with open('config/database.conf', 'w') as f:
        f.write('''# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fileshare
DB_USER=dbadmin
DB_PASS=db_secure_password_2024
DB_SSL=true

# Connection Pool
MAX_CONNECTIONS=100
TIMEOUT=30
''')
    
    with open('config/app.conf', 'w') as f:
        f.write('''# Application Configuration
APP_NAME=FileShare
APP_VERSION=1.2.3
DEBUG=false
SECRET_KEY=app_super_secret_key_2024

# Security Settings
ENABLE_LOGGING=true
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=pdf,doc,docx,txt,jpg,png

# Admin Settings
ADMIN_EMAIL=admin@fileshare.com
ADMIN_PANEL_ENABLED=true
''')
    
    # Secret flag file
    with open('flag.txt', 'w') as f:
        f.write('CTF{l0c4l_f1l3_1nclus10n_pwn3d}')
    
    # Additional sensitive files
    with open('admin_notes.txt', 'w') as f:
        f.write('''CONFIDENTIAL - ADMIN NOTES
==========================

TODO:
- Update server security patches
- Review user access permissions  
- Backup database weekly
- Check for suspicious file access patterns

PASSWORDS:
- Admin panel: admin123!@#
- Database backup: backup_secure_2024
- Emergency access: emergency_key_xyz

FLAG LOCATION: The main flag is stored in flag.txt
BONUS FLAG: CTF{d1r3ct0ry_tr4v3rs4l_m4st3r}

Remember to delete this file before production!
''')

# Initialize sample files
create_sample_files()

MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FileShare - Document Management</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.2em;
        }
        .header p {
            margin: 10px 0 0 0;
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
            border-bottom-color: #667eea;
            color: #667eea;
        }
        .content {
            flex: 1;
            padding: 40px;
        }
        .page-content {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .page-content h2 {
            margin-top: 0;
            color: #333;
        }
        .page-content h3 {
            color: #667eea;
            margin-top: 25px;
        }
        .page-content ul {
            line-height: 1.8;
        }
        .page-content p {
            line-height: 1.6;
            color: #555;
        }
        .hint-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
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
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .file-content {
            background: #f1f3f4;
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
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
            <h1>📁 FileShare</h1>
            <p>Secure Document Management System</p>
        </div>
        
        <nav class="nav">
            <ul>
                <li><a href="/?page=home" class="{{ 'active' if page == 'home' else '' }}">Home</a></li>
                <li><a href="/?page=about" class="{{ 'active' if page == 'about' else '' }}">About</a></li>
                <li><a href="/?page=contact" class="{{ 'active' if page == 'contact' else '' }}">Contact</a></li>
            </ul>
        </nav>
        
        <div class="content">
            <div class="hint-box">
                <h3>🎯 Challenge Hint</h3>
                <p><strong>Objective:</strong> Find the hidden flag using Local File Inclusion!</p>
                <p><strong>Hint 1:</strong> Notice how the page parameter loads different content</p>
                <p><strong>Hint 2:</strong> Try manipulating the page parameter to access other files</p>
                <p><strong>Hint 3:</strong> Look for files like flag.txt, admin_notes.txt, or config files</p>
                <p><strong>Hint 4:</strong> Directory traversal with ../ might help you access files outside the pages folder</p>
                <p><strong>Hint 5:</strong> Try: ?page=../flag.txt or ?page=../admin_notes.txt</p>
            </div>
            
            {% if error %}
            <div class="error">
                <strong>Error:</strong> {{ error }}
            </div>
            {% endif %}
            
            {% if file_content %}
            <div class="file-content">{{ file_content }}</div>
            {% else %}
            {{ content|safe }}
            {% endif %}
        </div>
        
        <div class="footer">
            © 2024 FileShare Inc. All rights reserved.
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    page = request.args.get('page', 'home')
    content = ''
    file_content = ''
    error = None
    
    try:
        # Vulnerable file inclusion - directly using user input
        file_path = f'pages/{page}.html'
        
        # If the file doesn't exist in pages, try direct path
        if not os.path.exists(file_path):
            file_path = page
        
        # Check if it's a text file we can display
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
                
            # If it's an HTML file, render it as content
            if file_path.endswith('.html'):
                content = file_content
                file_content = ''
        else:
            error = f"File not found: {file_path}"
            # Default to home page
            with open('pages/home.html', 'r') as f:
                content = f.read()
                
    except Exception as e:
        error = f"Error reading file: {str(e)}"
        # Default to home page on error
        try:
            with open('pages/home.html', 'r') as f:
                content = f.read()
        except:
            content = "<p>Error loading default page.</p>"
    
    return render_template_string(MAIN_TEMPLATE, 
                                content=content, 
                                file_content=file_content,
                                page=page, 
                                error=error)

@app.route('/debug')
def debug():
    """Debug endpoint to show file structure"""
    file_structure = {}
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        relative_root = root[2:] if root.startswith('./') else root
        if relative_root == '':
            relative_root = '.'
            
        file_structure[relative_root] = {
            'directories': dirs,
            'files': files
        }
    
    return file_structure

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)