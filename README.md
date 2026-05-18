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

- **Main analyzer interface**
<img width="1024" height="768" alt="main-dashboard" src="https://github.com/user-attachments/assets/35b5646d-d991-45ab-9e7e-320c53ff6d6d" />

- **Strong Password (input given)**
<img width="1024" height="768" alt="strong-password" src="https://github.com/user-attachments/assets/284c8c1d-8364-48a0-ba19-546e6e3685bd" />

- **Password Generator**
<img width="1024" height="768" alt="password-generator" src="https://github.com/user-attachments/assets/83082ff7-d3af-4a2f-bb0f-b00a2a716395" />

- **Password history section**
<img width="1024" height="768" alt="history-section" src="https://github.com/user-attachments/assets/529f9459-0046-427c-948c-f80849173a07" />

- **Password report analysis downloded from the site**
<img width="1024" height="768" alt="password-report-analysis downloads" src="https://github.com/user-attachments/assets/50fb4080-df45-4fe1-9a69-ada52017164f" />


## 📁 Project Structure
```bash
**password-analyzer/**
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

**Open in browser:**
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
**MARADANA HIMATEJ**
**Cyber Security Student**

