# Challenge 1: HTML Inspector (Basic)

## Description
Welcome to CyberCorp's website! They claim to be a leading cybersecurity company, but something tells me they might have left some secrets lying around. Can you find the hidden flag?

## Objective
Find the flag hidden in the website's source code.

## Difficulty
⭐ Basic

## Setup
1. Open `index.html` in a web browser
2. Or serve it with a simple HTTP server:
   ```bash
   python3 -m http.server 8000
   ```
3. Navigate to `http://localhost:8000`

## Hints
- The website gives you a hint about where to look
- Developers sometimes leave comments in their code
- Try right-clicking and selecting "View Page Source" or use F12

## Flag Format
`CTF{...}`

## Solution
<details>
<summary>Click to reveal solution</summary>

The flag is hidden in the HTML source code in multiple places:
1. In the CSS comments: `/* Flag: CTF{1nsp3ct_th3_s0urc3_luk3} */`
2. In the HTML comments: `<!-- Flag hidden here: CTF{1nsp3ct_th3_s0urc3_luk3} -->`

**Flag:** `CTF{1nsp3ct_th3_s0urc3_luk3}`

### Steps to solve:
1. Open the website in a browser
2. Right-click and select "View Page Source" or press F12
3. Look through the HTML source code for comments
4. Find the flag in the CSS or HTML comments

</details>

## Learning Objectives
- Understanding HTML source code inspection
- Recognizing that client-side code is always visible to users
- Learning to use browser developer tools