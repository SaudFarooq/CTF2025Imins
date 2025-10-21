from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT,
            role TEXT,
            secret_data TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY,
            flag_name TEXT,
            flag_value TEXT,
            description TEXT
        )
    ''')
    
    # Insert sample data
    products = [
        (1, 'Laptop', 'High-performance laptop', 999.99, 'Electronics'),
        (2, 'Smartphone', 'Latest smartphone model', 699.99, 'Electronics'),
        (3, 'Headphones', 'Noise-canceling headphones', 199.99, 'Audio'),
        (4, 'Keyboard', 'Mechanical gaming keyboard', 149.99, 'Accessories'),
        (5, 'Mouse', 'Wireless gaming mouse', 79.99, 'Accessories'),
    ]
    
    users = [
        (1, 'admin', 'admin@techshop.com', 'administrator', 'admin_secret_key_2024'),
        (2, 'manager', 'manager@techshop.com', 'manager', 'manager_access_token'),
        (3, 'user', 'user@techshop.com', 'customer', 'user_session_data'),
    ]
    
    flags = [
        (1, 'main_flag', 'CTF{sql_1nj3ct10n_m4st3r_h4ck3r}', 'Main challenge flag'),
        (2, 'bonus_flag', 'CTF{un10n_s3l3ct_pr0}', 'Bonus flag for advanced techniques'),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?)', products)
    cursor.executemany('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)', users)
    cursor.executemany('INSERT OR REPLACE INTO flags VALUES (?, ?, ?, ?)', flags)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechShop - Product Search</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(45deg, #74b9ff, #0984e3);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }
        .search-section {
            padding: 40px;
            text-align: center;
        }
        .search-form {
            max-width: 600px;
            margin: 0 auto;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
            text-align: left;
        }
        input[type="text"], select {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="text"]:focus, select:focus {
            border-color: #74b9ff;
            outline: none;
        }
        .search-btn {
            background: linear-gradient(45deg, #74b9ff, #0984e3);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        .search-btn:hover {
            opacity: 0.9;
        }
        .results {
            padding: 0 40px 40px 40px;
        }
        .product {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .product-info h3 {
            margin: 0 0 5px 0;
            color: #333;
        }
        .product-info p {
            margin: 0;
            color: #666;
        }
        .product-price {
            font-size: 1.3em;
            font-weight: bold;
            color: #0984e3;
        }
        .hint-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 40px;
        }
        .hint-box h3 {
            margin: 0 0 10px 0;
            color: #856404;
        }
        .hint-box p {
            margin: 5px 0;
            color: #856404;
        }
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 TechShop</h1>
            <p>Find the best tech products at amazing prices!</p>
        </div>
        
        <div class="search-section">
            <form class="search-form" method="POST" action="/">
                <div class="form-group">
                    <label for="search">Search Products:</label>
                    <input type="text" id="search" name="search" placeholder="Enter product name or description..." value="{{ search_term }}">
                </div>
                <div class="form-group">
                    <label for="category">Category:</label>
                    <select id="category" name="category">
                        <option value="">All Categories</option>
                        <option value="Electronics" {{ 'selected' if category == 'Electronics' else '' }}>Electronics</option>
                        <option value="Audio" {{ 'selected' if category == 'Audio' else '' }}>Audio</option>
                        <option value="Accessories" {{ 'selected' if category == 'Accessories' else '' }}>Accessories</option>
                    </select>
                </div>
                <button type="submit" class="search-btn">Search Products</button>
            </form>
        </div>
        
        <div class="hint-box">
            <h3>🎯 Challenge Hint</h3>
            <p><strong>Objective:</strong> Find the hidden flag in the database!</p>
            <p><strong>Hint 1:</strong> The search functionality might be vulnerable to SQL injection</p>
            <p><strong>Hint 2:</strong> Try using special characters like single quotes (') in your search</p>
            <p><strong>Hint 3:</strong> Look for other tables in the database using UNION SELECT</p>
            <p><strong>Hint 4:</strong> The flag might be in a table called 'flags' or 'users'</p>
        </div>
        
        {% if error %}
        <div class="error">
            <strong>Database Error:</strong> {{ error }}
        </div>
        {% endif %}
        
        <div class="results">
            {% if products %}
                <h2>Search Results ({{ products|length }} found):</h2>
                {% for product in products %}
                <div class="product">
                    <div class="product-info">
                        <h3>{{ product[1] }}</h3>
                        <p>{{ product[2] }}</p>
                        <small>Category: {{ product[4] }}</small>
                    </div>
                    <div class="product-price">${{ "%.2f"|format(product[3]) }}</div>
                </div>
                {% endfor %}
            {% elif search_term %}
                <h2>No products found for "{{ search_term }}"</h2>
                <p>Try a different search term or check your spelling.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def search():
    products = []
    search_term = ''
    category = ''
    error = None
    
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        category = request.form.get('category', '').strip()
        
        try:
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            
            # Vulnerable SQL query - intentionally susceptible to SQL injection
            query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
            
            if category:
                query += f" AND category = '{category}'"
            
            print(f"Executing query: {query}")  # Debug output
            
            cursor.execute(query)
            products = cursor.fetchall()
            conn.close()
            
        except Exception as e:
            error = str(e)
            print(f"Database error: {error}")
    
    return render_template_string(MAIN_TEMPLATE, 
                                products=products, 
                                search_term=search_term, 
                                category=category,
                                error=error)

@app.route('/debug')
def debug():
    """Debug endpoint to show database structure"""
    try:
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        result = {"tables": []}
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            result["tables"].append({
                "name": table_name,
                "columns": [col[1] for col in columns]
            })
        
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)