import re
import math
import string
import getpass
import sys

# ─────────────────────────────────────────────
# 1. COMMON PASSWORDS (top 20 inline — no file needed)
# ─────────────────────────────────────────────
COMMON_PASSWORDS = {
    "password", "123456", "password123", "12345678", "qwerty",
    "abc123", "monkey", "1234567", "letmein", "trustno1",
    "dragon", "baseball", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "passw0rd", "shadow", "123123",
    "654321", "superman", "qazwsx", "michael", "football",
}

# ─────────────────────────────────────────────
# 2. RULES ENGINE
# ─────────────────────────────────────────────

def check_length(pw):
    n = len(pw)
    if n >= 16:
        return 30, "Excellent (16+ chars)"
    elif n >= 12:
        return 25, "Good (12–15 chars)"
    elif n >= 8:
        return 15, "Acceptable (8–11 chars)"
    else:
        return 0, f"Too short ({n} chars — need at least 8)"

def check_variety(pw):
    score = 0
    notes = []
    has_lower  = bool(re.search(r'[a-z]', pw))
    has_upper  = bool(re.search(r'[A-Z]', pw))
    has_digit  = bool(re.search(r'\d', pw))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', pw))

    if has_lower:  score += 10; notes.append("lowercase ✓")
    else:          notes.append("lowercase ✗")
    if has_upper:  score += 10; notes.append("uppercase ✓")
    else:          notes.append("uppercase ✗")
    if has_digit:  score += 10; notes.append("digits ✓")
    else:          notes.append("digits ✗")
    if has_symbol: score += 15; notes.append("symbols ✓")
    else:          notes.append("symbols ✗")

    return score, notes

def calc_entropy(pw):
    pool = 0
    if re.search(r'[a-z]', pw): pool += 26
    if re.search(r'[A-Z]', pw): pool += 26
    if re.search(r'\d', pw):    pool += 10
    if re.search(r'[^a-zA-Z0-9]', pw): pool += 32

    if pool == 0:
        return 0, 0

    entropy = len(pw) * math.log2(pool)
    if entropy >= 80:   score = 15
    elif entropy >= 60: score = 10
    elif entropy >= 40: score = 5
    else:               score = 0

    return score, round(entropy, 1)

def check_common(pw):
    if pw.lower() in COMMON_PASSWORDS:
        return -20, "Found in common passwords list ✗"
    return 0, "Not a common password ✓"

def check_patterns(pw):
    deductions = 0
    warnings = []
    if re.search(r'(.)\1{2,}', pw):
        deductions -= 10
        warnings.append("Repeated characters detected ✗")
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', pw.lower()):
        deductions -= 10
        warnings.append("Sequential characters detected ✗")
    return deductions, warnings

# ─────────────────────────────────────────────
# 3. SCORER
# ─────────────────────────────────────────────

def score_password(pw):
    results = {}

    length_score, length_note = check_length(pw)
    variety_score, variety_notes = check_variety(pw)
    entropy_score, entropy_bits = calc_entropy(pw)
    common_score, common_note = check_common(pw)
    pattern_score, pattern_warnings = check_patterns(pw)

    total = max(0, min(100,
        length_score + variety_score + entropy_score + common_score + pattern_score
    ))

    if total >= 80:
        label = "VERY STRONG"
        color = "\033[92m"   # green
    elif total >= 60:
        label = "STRONG"
        color = "\033[92m"
    elif total >= 40:
        label = "MEDIUM"
        color = "\033[93m"   # yellow
    else:
        label = "WEAK"
        color = "\033[91m"   # red

    return {
        "total": total,
        "label": label,
        "color": color,
        "length_note": length_note,
        "variety_notes": variety_notes,
        "entropy_bits": entropy_bits,
        "common_note": common_note,
        "pattern_warnings": pattern_warnings,
    }

# ─────────────────────────────────────────────
# 4. CLI INTERFACE
# ─────────────────────────────────────────────

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"

def print_bar(score):
    filled = int(score / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"  [{bar}] {score}/100")

def display_result(r):
    print()
    print(f"{BOLD}Password Strength: {r['color']}{r['label']}{RESET}{BOLD} ({r['total']}/100){RESET}")
    print_bar(r["total"])
    print()
    print(f"  {DIM}Length   {RESET}{r['length_note']}")
    print(f"  {DIM}Entropy  {RESET}{r['entropy_bits']} bits")
    print(f"  {DIM}Common   {RESET}{r['common_note']}")
    print()
    print(f"  {DIM}Character variety:{RESET}")
    for note in r["variety_notes"]:
        print(f"    {note}")
    if r["pattern_warnings"]:
        print()
        print(f"  {DIM}Pattern warnings:{RESET}")
        for w in r["pattern_warnings"]:
            print(f"    {w}")
    print()

def main():
    print(f"\n{BOLD}─── Password Strength Checker ───{RESET}")
    print(f"{DIM}Input is hidden. Press Ctrl+C to quit.{RESET}\n")

    while True:
        try:
            pw = getpass.getpass("  Enter password: ")
            if not pw:
                print("  No input received.\n")
                continue
            result = score_password(pw)
            display_result(result)

            again = input("  Check another? (y/n): ").strip().lower()
            if again != "y":
                print(f"\n{DIM}Goodbye.{RESET}\n")
                break
            print()

        except KeyboardInterrupt:
            print(f"\n\n{DIM}Exited.{RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
