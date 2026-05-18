# 🔐 Password Strength Analyzer
A Flask-based cybersecurity utility designed to evaluate password strength using entropy analysis, pattern detection, and secure local password history management.
This project focuses on practical password security concepts including:
- password complexity analysis
- entropy estimation
- brute-force resistance
- secure password generation
- password reuse detection
The application provides real-time feedback while maintaining a clean and fully functional user experience.

## 🌐 Live Demo
https://password-strength-analyzer-wxun.onrender.com


## 🖥️ GitHub Repository
https://github.com/maradanahimatej1410-bit/password-strength-analyzer

## ✨ Features

### 🔍 Password Strength Analysis
- Real-time password evaluation
- Strength percentage scoring
- Entropy estimation in bits
- Estimated brute-force crack-time analysis
- Detection of weak/common password patterns

### 🛡️ Security Validation
Checks for:
- minimum length
- uppercase letters
- lowercase letters
- numbers
- special symbols

### 🔑 Password Generator
- Generates secure random passwords
- Configurable complexity
- One-click copy support

### 🗂️ Password History
- Stores password analysis history locally using SQLite
- Detects previously used passwords
- Delete individual records
- Clear complete history

### 📄 Export Functionality
- Export password analysis reports
- Reports exclude plaintext passwords for security

### 🎨 User Experience
- Responsive dark-themed interface
- Real-time security feedback
- Smooth interactions and transitions
- Fully functional UI components


## ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web framework |
| SQLite | Local database |
| zxcvbn | Password strength analysis |
| HTML | Structure |
| CSS | Styling |
| JavaScript | Frontend interactivity |


## 📸 Screenshots
Suggested screenshots to include:
- Main analyzer interface
<img width="1024" height="768" alt="main-dashboard" src="https://github.com/user-attachments/assets/083ed7ed-593f-4ef5-8aae-95e6da0ac5d9" />
- Strong Password (input given)
<img width="1024" height="768" alt="strong-password" src="https://github.com/user-attachments/assets/1fd885d7-6915-4109-8896-c5df7d6b687c" />
- Password Generator
<img width="1024" height="768" alt="password-generator" src="https://github.com/user-attachments/assets/222c0b7c-52dd-4e31-a725-8707ce791af4" />
- Password history section
<img width="1024" height="768" alt="history-section" src="https://github.com/user-attachments/assets/d80a366f-2094-44f4-86ef-f1bf3ba71ee4" />
- Password report analysis downloded from the site
<img width="1024" height="768" alt="password-report-analysis downloads" src="https://github.com/user-attachments/assets/8337dbef-7265-4e4d-899c-33c8a04d692b" />


## 📁 Project Structure
```bash
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
````

## 🚀 Installation
### Clone Repository
```bash
git clone https://github.com/maradanahimatej1410-bit/password-strength-analyzer.git
```

### Open Project
```bash
cd password-strength-analyzer
```

### Create Virtual Environment
```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows
```bash
.venv\Scripts\activate
```

#### Linux / macOS
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```


## ▶️ Run Locally
```bash
python app.py
```

Open in browser:
```text
http://127.0.0.1:5001
```

## 🧠 Security Concepts Demonstrated
* Password entropy calculation
* Secure password generation
* Password reuse detection
* SHA-256 hashing
* Local secure password handling
* Brute-force resistance estimation
* Real-time password validation

## 🔒Security Notes
* Passwords are never stored in plaintext
* Local password history uses deterministic hashing
* Exported reports never expose original passwords
* Designed for educational and local-use purposes

## 🔮 Future Improvements
* Breached-password database checks
* PDF export support
* User authentication system
* Advanced password policy customization
* Automated testing
* Optional encrypted local vault


## 👨‍💻 Author
MARADANA HIMATEJ
Cyber Security Student

