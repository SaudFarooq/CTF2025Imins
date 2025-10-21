# Cyberhackathon CTF Web Challenges

This repository contains 5 web security challenges for a cyberhackathon CTF event, ranging from basic to high difficulty.

## Challenge Overview

### Basic Challenges (2)
1. **HTML Inspector** ⭐ - Find the flag hidden in HTML source code
2. **Auth Bypass** ⭐ - Simple authentication bypass vulnerability

### Medium to High Challenges (3)
3. **SQL Injection** ⭐⭐ - Extract data using SQL injection techniques
4. **File Inclusion** ⭐⭐⭐ - Local File Inclusion (LFI) vulnerability
5. **Template Injection** ⭐⭐⭐ - Server-Side Template Injection (SSTI) exploit

## Quick Setup

Run the automated setup script to start all challenges:

```bash
./setup_all.sh
```

This will build and start all Docker containers automatically.

## Manual Setup

Each challenge is contained in its own directory with:
- Source code
- Docker configuration
- README with setup instructions and solutions
- Requirements file

### Individual Challenge Setup

1. Navigate to a challenge directory (e.g., `cd challenges/02-auth-bypass`)
2. Install dependencies: `pip install -r requirements.txt`
3. Run with Docker: `docker-compose up -d`
4. Or run directly: `python app.py`

## Challenge URLs

Once running, access the challenges at:

1. **HTML Inspector**: Open `challenges/01-html-inspector/index.html` in browser
2. **Auth Bypass**: http://localhost:5001
3. **SQL Injection**: http://localhost:5002
4. **File Inclusion**: http://localhost:5003
5. **Template Injection**: http://localhost:5004

## Challenge Details

| Challenge | Difficulty | Port | Key Concepts |
|-----------|------------|------|--------------|
| HTML Inspector | ⭐ Basic | Static | Source code inspection, client-side security |
| Auth Bypass | ⭐ Basic | 5001 | SQL injection, authentication bypass |
| SQL Injection | ⭐⭐ Medium | 5002 | UNION SELECT, database enumeration |
| File Inclusion | ⭐⭐⭐ Medium-High | 5003 | LFI, directory traversal, file system access |
| Template Injection | ⭐⭐⭐ High | 5004 | SSTI, code execution, sandbox escape |

## Flag Format

All flags follow the format: `CTF{...}`

## Learning Objectives

- **HTML Inspector**: Understanding client-side security and source code inspection
- **Auth Bypass**: Learning about SQL injection in authentication systems
- **SQL Injection**: Mastering UNION SELECT and database enumeration techniques
- **File Inclusion**: Understanding LFI vulnerabilities and directory traversal
- **Template Injection**: Advanced SSTI exploitation and code execution

## Stopping Challenges

To stop all running challenges:
```bash
# Stop individual challenge
cd challenges/[challenge-name]
docker-compose down

# Or stop all Docker containers
docker stop $(docker ps -q)
```

## Solutions

Each challenge directory contains a detailed README with:
- Challenge description and objectives
- Setup instructions
- Hints and tips
- Complete solution walkthrough
- Learning objectives

## Security Notice

⚠️ **Warning**: These challenges contain intentional vulnerabilities for educational purposes. Do not deploy in production environments.

Good luck and happy hacking! 🚩