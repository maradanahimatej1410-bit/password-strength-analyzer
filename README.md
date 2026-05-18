# Password Strength Analyzer

A Flask-based cybersecurity utility designed to evaluate password strength using entropy analysis, pattern detection, and secure local password history management.

This project focuses on practical password security concepts including:
- password complexity analysis
- entropy estimation
- brute-force resistance
- secure password generation
- password reuse detection
The application provides real-time feedback while maintaining a clean and fully functional user experience.

## Live Demo
https://password-strength-analyzer-wxun.onrender.com

## GitHub Repository
https://github.com/maradanahimatej1410-bit/password-strength-analyzer

## Features
### Password Strength Analysis
- Real-time password evaluation
- Strength percentage scoring
- Entropy estimation in bits
- Estimated brute-force crack-time analysis
- Detection of weak/common password patterns

### Security Validation
Checks for:
- minimum length
- uppercase letters
- lowercase letters
- numbers
- special symbols

### Password Generator
- Generates secure random passwords
- Configurable complexity
- One-click copy support

### Password History
- Stores password analysis history locally using SQLite
- Detects previously used passwords
- Delete individual records
- Clear complete history

### Export Functionality
- Export password analysis reports
- Reports exclude plaintext passwords for security

### User Experience
- Responsive dark-themed interface
- Real-time security feedback
- Smooth interactions and transitions
- Fully functional UI components

## Technologies Used
| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web framework |
| SQLite | Local database |
| zxcvbn | Password strength analysis |
| HTML | Structure |
| CSS | Styling |
| JavaScript | Frontend interactivity |

## Screenshots
Suggested screenshots to include:
- Main analyzer interface
- Password generator
- Password history section
- Security feedback examples

## Project Structure
password-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── store.py
│   └── passwords.db
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js

## Installation
### Clone Repository
git clone https://github.com/maradanahimatej1410-bit/password-strength-analyzer.git

### Open Project
cd password-strength-analyzer

### Create Virtual Environment
python -m venv .venv

### Activate Virtual Environment
#### Windows
.venv\Scripts\activate

#### Linux / macOS
source .venv/bin/activate

### Install Dependencies
pip install -r requirements.txt

## Run Locally
python app.py

Open in browser:
http://127.0.0.1:5001

## Security Concepts Demonstrated
* Password entropy calculation
* Secure password generation
* Password reuse detection
* SHA-256 hashing
* Local secure password handling
* Brute-force resistance estimation
* Real-time password validation

## Security Notes
* Passwords are never stored in plaintext
* Local password history uses deterministic hashing
* Exported reports never expose original passwords
* Designed for educational and local-use purposes

## Future Improvements
* Breached-password database checks
* PDF export support
* User authentication system
* Advanced password policy customization
* Automated testing
* Optional encrypted local vault

## Author
MARADANA HIMATEJ
Cyber Security Student
