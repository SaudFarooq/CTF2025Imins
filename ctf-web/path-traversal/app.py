from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)

BASE_DIR = os.path.join(os.getcwd(), 'files')
SECRET_DIR = os.path.join(os.getcwd(), 'secret')

@app.route('/')
def home():
    return 'Download with /download?file=readme.txt'

@app.route('/download')
def download():
    file = request.args.get('file', '')
    # Vulnerable: naive join without normalization and allow .. traversal to reach secret/flag.txt
    requested_path = os.path.join(BASE_DIR, file)
    if not os.path.exists(requested_path):
        # Simulate helpful error leaking base path
        return f"File not found at {requested_path}", 404
    try:
        return send_from_directory(BASE_DIR, file, as_attachment=True)
    except Exception:
        abort(403)

if __name__ == '__main__':
    # Put a benign file in files
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(os.path.join(BASE_DIR, 'readme.txt'), 'w') as f:
        f.write('Not the flag. Look harder.')
    app.run(host='0.0.0.0', port=8000)
