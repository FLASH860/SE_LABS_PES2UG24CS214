import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

# Sane upper limits so huge inputs can't overflow floats or hang the program
MAX_INCOME = 10**12        # 1 lakh crore
MAX_PRINCIPAL = 10**12
MAX_RATE = 100             # % per annum
MAX_YEARS = 100

# Indian / international grouping or plain digits: 50000, 50,000, 5,00,000
INCOME_PATTERN = re.compile(r"^(\d+|\d{1,3}(,\d{2,3})+)$")
INT_PATTERN = re.compile(r"^\d+$")
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")


def _to_positive_int(text):
    """Return int(text) for plain ASCII digits, else None."""
    text = text.strip()
    if not text.isascii() or not INT_PATTERN.fullmatch(text):
        return None
    return int(text)


def parse_income(income):
    """'50,000' -> 50000. Returns None for invalid input instead of crashing."""
    if not isinstance(income, str):
        return None
    income = income.strip()
    if not income.isascii() or not INCOME_PATTERN.fullmatch(income):
        return None
    value = int(income.replace(",", ""))
    if value > MAX_INCOME:
        return None
    return value


def monthly_emi(details):
    """'principal,rate,years' -> EMI rounded to 2 decimals, or None if invalid."""
    if not isinstance(details, str):
        return None
    parts = details.split(",")
    if len(parts) != 3:
        return None
    principal, rate, years = (_to_positive_int(p) for p in parts)
    if principal is None or rate is None or years is None:
        return None
    if not (0 < principal <= MAX_PRINCIPAL):
        return None
    if not (0 <= rate <= MAX_RATE):
        return None
    if not (0 < years <= MAX_YEARS):
        return None

    n = years * 12
    if rate == 0:                       # 0% loan: avoid divide-by-zero
        return round(principal / n, 2)
    r = rate / 1200
    growth = (1 + r) ** n
    return round(principal * r * growth / (growth - 1), 2)


def pan_category(pan):
    """'ABCPE1234F' -> 'Individual'. Returns None for invalid / unknown PANs."""
    if not isinstance(pan, str):
        return None
    pan = pan.strip()
    if not pan.isascii():
        return None
    pan = pan.upper()
    if not PAN_PATTERN.fullmatch(pan):
        return None
    return CATEGORIES.get(pan[3])


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result if result is not None else "Invalid income")

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result if result is not None else "Invalid loan details")

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()
