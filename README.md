# Secure Blog Web Application (Flask)

## Description
This project is a secure blog web application developed using Python Flask and SQLite.  
It demonstrates the implementation of secure web development practices and protection against common web application vulnerabilities following OWASP guidelines.

The application allows users to register, authenticate, create posts, and manage content through a role-based access control system.

---

## Features

### Application Features
- User registration and login
- Secure password hashing (PBKDF2-SHA256)
- Role-Based Access Control (Admin / User)
- Create and view blog posts
- Delete posts (owner or admin only)
- Session-based authentication

### Security Features
- HTTPS support
- Secure session cookies
- CSRF protection (Flask-WTF)
- Input validation and sanitization
- SQL injection protection using parameterized queries
- XSS protection using Jinja2 auto-escaping
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- Session timeout and secure cookie configuration

---

## Security Testing

Security testing was performed using **OWASP ZAP**.

Process:
1. Initial vulnerability scan to identify security issues
2. Implementation of security controls
3. Second scan to verify mitigation of vulnerabilities

The implemented measures significantly reduced the risk of common web attacks such as SQL Injection, Cross-Site Scripting (XSS), CSRF, and Man-in-the-Middle attacks.

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML / CSS
- Jinja2 Templates
- Flask-WTF
- OWASP ZAP

---

## Project Structure


secure-blog
│
├── app.py
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── new_post.html
│ └── post.html


---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt

Run the application:

python app.py

Open the browser at:

http://localhost:5000
Educational Context

This project was developed as part of the Information Systems Security course at the University of Piraeus.
The goal of the project was to implement a web application and progressively apply security mechanisms and vulnerability assessment techniques.

Disclaimer

This project is intended for educational purposes and security experimentation.
