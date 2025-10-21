#!/bin/bash

echo "🚩 Setting up Cyberhackathon CTF Web Challenges"
echo "=============================================="

# Function to setup individual challenge
setup_challenge() {
    local challenge_dir=$1
    local challenge_name=$2
    local port=$3
    
    echo "📁 Setting up $challenge_name..."
    cd "$challenge_dir"
    
    if [ -f "requirements.txt" ]; then
        echo "   Installing Python dependencies..."
        pip install -r requirements.txt > /dev/null 2>&1
    fi
    
    if [ -f "docker-compose.yml" ]; then
        echo "   Building Docker container..."
        docker-compose build > /dev/null 2>&1
        echo "   Starting container on port $port..."
        docker-compose up -d > /dev/null 2>&1
    fi
    
    cd ..
    echo "   ✅ $challenge_name ready on http://localhost:$port"
}

# Navigate to challenges directory
cd challenges

# Setup each challenge
setup_challenge "02-auth-bypass" "Authentication Bypass" "5001"
setup_challenge "03-sql-injection" "SQL Injection" "5002"
setup_challenge "04-file-inclusion" "File Inclusion" "5003"
setup_challenge "05-template-injection" "Template Injection" "5004"

echo ""
echo "🎯 All challenges are now running!"
echo "================================="
echo ""
echo "Challenge URLs:"
echo "1. HTML Inspector: Open challenges/01-html-inspector/index.html in browser"
echo "2. Auth Bypass: http://localhost:5001"
echo "3. SQL Injection: http://localhost:5002"
echo "4. File Inclusion: http://localhost:5003"
echo "5. Template Injection: http://localhost:5004"
echo ""
echo "To stop all challenges: docker-compose down (in each challenge directory)"
echo ""
echo "Happy hacking! 🚩"