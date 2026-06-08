# Password Strength Checker

A lightweight, zero-dependency CLI tool that analyses password strength using entropy calculation, character variety checks, common password detection, and pattern analysis — all in a single Python file.

---

## Features

- **Entropy calculation** — measures true randomness in bits based on character pool size
- **Character variety checks** — detects lowercase, uppercase, digits, and symbols
- **Common password detection** — flags passwords found in a built-in top-25 list
- **Pattern analysis** — detects repeated characters (`aaa`) and sequential runs (`123`, `abc`)
- **Weighted scoring** — produces a 0–100 score mapped to Weak / Medium / Strong / Very Strong
- **Hidden input** — password is never echoed to the terminal (uses `getpass`)
- **Color-coded output** — red, yellow, and green results for instant readability
- **No dependencies** — pure Python stdlib, nothing to install

---

## Requirements

- Python 3.6 or higher
- No external packages required

---

## Installation

Clone the repository:

```bash
git clone https://joeprince20047-oss.github.io/password_checker/.git
cd password-checker
```

That's it. No virtual environment or `pip install` needed.

---

## Usage

```bash
python password_checker.py
```

You will be prompted to enter a password (input is hidden):

```
─── Password Strength Checker ───
Input is hidden. Press Ctrl+C to quit.

  Enter password:

Password Strength: STRONG (75/100)
  [███████████████░░░░░] 75/100

  Length    12 chars — good
  Entropy   78.5 bits
  Common    Not a common password ✓

  Character variety:
    lowercase ✓
    uppercase ✓
    digits ✓
    symbols ✓
```

Press `y` when prompted to check another password, or `n` to exit.

---

## Scoring Breakdown

| Check | Max Points |
|---|---|
| Length (16+ chars) | 30 |
| Symbols present | 15 |
| Uppercase letters | 10 |
| Lowercase letters | 10 |
| Digits present | 10 |
| Entropy (80+ bits) | 15 |
| Common password penalty | −20 |
| Repeated character penalty | −10 |
| Sequential character penalty | −10 |

| Score | Label |
|---|---|
| 80 – 100 | Very Strong |
| 60 – 79 | Strong |
| 40 – 59 | Medium |
| 0 – 39 | Weak |

---

## Project Structure

```
password-checker/
├── password_checker.py   # all logic — rules engine, scorer, CLI
└── README.md
```

---

## Optional: Make it pip-installable

To install directly from GitHub into any Python environment:

```bash
pip install git+https://joeprince20047-oss.github.io/password_checker/.git
```

Or build a standalone binary with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile password_checker.py
# output binary → dist/password_checker
```

---

## Security Notes

- Passwords are **never stored, logged, or transmitted**
- Input is read via `getpass` — not visible in terminal history
- This tool is for **local auditing only** — do not pipe passwords through untrusted environments

---

## License

MIT — free to use, modify, and distribute.
