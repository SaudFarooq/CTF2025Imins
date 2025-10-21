from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = "CH{reflected_xss_is_fun}"

INDEX = """
<!doctype html>
<title>Echo</title>
<h1>Say something</h1>
<form method=get>
  <input name=q placeholder="hello">
  <button>Go</button>
</form>
{% if q is not none %}
<p>You said: {{ q|safe }}</p>
{% endif %}
<!-- Hint: Use injected JS to fetch /flag with header X-Admin: 1 -->
"""

@app.route('/')
def index():
    q = request.args.get('q')
    return render_template_string(INDEX, q=q)

@app.route('/flag')
def flag():
    # Require a custom header so the flag isn't directly retrievable without XSS
    if request.headers.get('X-Admin') == '1':
        return FLAG
    return "Forbidden", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
