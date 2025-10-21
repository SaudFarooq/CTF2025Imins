from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = "CH{ssti_render_power}"

# Intentionally vulnerable: user controls the template string via `tpl` parameter
BASE_TPL = """
<!doctype html>
<title>Greet</title>
<h1>{{ title }}</h1>
<div>
  {{ body }}
</div>
<small>Hint: Jinja expression context has access to config and joiner.</small>
"""

@app.route('/')
def greet():
    title = request.args.get('title', 'Welcome')
    body = request.args.get('tpl', 'Hello {{ name }}')
    name = request.args.get('name', 'friend')
    # Vulnerability: render inner user-controlled template first, then inject into outer template unsafely
    inner = render_template_string(body, name=name)
    return render_template_string(BASE_TPL, title=title, body=inner)

@app.route('/flag')
def flag():
    # Hidden endpoint; reachable via SSTI tricks
    return FLAG

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
