from flask import Flask, request, jsonify, abort

app = Flask(__name__)
FLAG = "CH{idor_gotcha}"

USERS = {
    "1": {"username": "alice", "email": "alice@example.com", "role": "user"},
    "2": {"username": "bob", "email": "bob@example.com", "role": "user"},
    "1337": {"username": "admin", "email": "root@example.com", "role": "admin", "flag": "CH{idor_gotcha}"},
}

@app.route('/')
def home():
    return "Profile API: GET /profile?userId=1"

@app.route('/profile')
def profile():
    user_id = request.args.get('userId', '1')
    user = USERS.get(user_id)
    if not user:
        abort(404)
    # IDOR: no auth checks
    return jsonify(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
