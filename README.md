# Password Strength Analyzer

A practical Flask-based cybersecurity utility for analyzing password strength, estimating entropy and crack time, generating secure passwords, and detecting local password reuse without storing plaintext passwords.

## Features

- Real-time password strength percentage from 0% to 100%
- zxcvbn-backed password analysis for common patterns and guessability
- Entropy estimate in bits
- Offline brute-force crack time estimate
- Requirement checks for length, uppercase, lowercase, numbers, and symbols
- Clear security feedback with practical recommendations
- Configurable secure password generator
- Copy-to-clipboard support with user feedback
- SQLite-backed password history
- Password reuse detection using deterministic hashes only
- Delete individual history records or clear all history
- Export a text report that never includes the raw password
- Responsive dark interface with no decorative-only controls

## Technologies Used

- Python
- Flask
- SQLite
- zxcvbn
- HTML
- CSS
- JavaScript

## Screenshots

Add screenshots here after running the app locally:

- Main analyzer screen
- Generated strong password analysis
- Saved history view

## Project Structure

```text
password-analyzer/
├── app.py
├── database/
│   ├── __init__.py
│   ├── store.py
│   └── passwords.db
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
python app.py
```

Open the app at:

```text
http://127.0.0.1:5001
```

The SQLite database is created automatically inside the `database/` directory.

## Security Notes

- Passwords are never stored in plaintext.
- History stores a SHA-256 hash with a local pepper value.
- Exported reports include analysis results only, not the password.
- This is an educational local utility, not a replacement for enterprise password auditing systems.

## Future Improvements

- Optional master-key protected local database
- Importable breached-password hash list checks
- PDF export
- Unit and browser automation tests
- User-configurable hashing pepper through a setup screen
