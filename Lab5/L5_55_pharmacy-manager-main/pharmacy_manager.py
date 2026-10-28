"""Manage pharmacy stock, billing, arithmetic and JSON persistence."""

import os
import ast
import json
import math
import operator
import secrets
import hashlib
from datetime import datetime, date

# Global pharmacy state
MEDICINES = {}

def validate_record(name, qty, price, expiry):
    """Reject invalid inventory data before modifying stock."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a nonempty string")
    if (not isinstance(qty, int) or isinstance(qty, bool)) or qty < 0:
        raise ValueError("Quantity must be a nonnegative integer")
    if (type(price) not in (int, float) or not math.isfinite(price)
            or price < 0):
        raise ValueError("Price must be finite and nonnegative")
    if not isinstance(expiry, str):
        raise ValueError("Expiry must be an ISO date string")
    date.fromisoformat(expiry)


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add validated stock and return an independent audit by default."""
    validate_record(name, qty, price, expiry)
    if name in MEDICINES and (
            MEDICINES[name]["price"] != price
            or MEDICINES[name]["expiry"] != expiry):
        raise ValueError("Existing stock has different price or expiry")
    if audit is None:
        audit = []
    if name not in MEDICINES:
        MEDICINES[name] = {"qty": 0, "price": price, "expiry": expiry}
    MEDICINES[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


def dispense_medicine(name, qty):
    """Dispense available, unexpired stock; reject requests atomically."""
    if (not isinstance(qty, int) or isinstance(qty, bool)) or qty <= 0:
        raise ValueError("Dispensing quantity must be a positive integer")
    if name not in MEDICINES:
        raise ValueError("Medicine is not in stock")
    if is_expired(name):
        raise ValueError("Medicine has expired")
    if qty > MEDICINES[name]["qty"]:
        raise ValueError("Insufficient stock")
    MEDICINES[name]["qty"] -= qty
    if MEDICINES[name]["qty"] == 0:
        del MEDICINES[name]


def get_quantity(name):
    """Return the quantity of a stocked medicine."""
    return MEDICINES[name]["qty"]

def is_expired(name):
    """Report whether expiry is before today."""
    exp = datetime.strptime(MEDICINES[name]["expiry"], "%Y-%m-%d").date()
    return exp < date.today()

def bill_amount(prescription):
    """Calculate a bill for positive integer quantities."""
    total = 0
    for name, qty in prescription:
        if (not isinstance(qty, int) or isinstance(qty, bool)) or qty <= 0:
            raise ValueError("Billing quantity must be a positive integer")
        total += MEDICINES[name]["price"] * qty
    return total

def calculate_dosage(formula):
    """Evaluate bounded numeric arithmetic without executing Python code."""
    # formula comes from the doctor's note, e.g. "250 * 2"
    if not isinstance(formula, str) or len(formula) > 200:
        raise ValueError("Formula must contain at most 200 characters")
    operations = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.Mult: operator.mul, ast.Div: operator.truediv}

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in operations:
            value = operations[type(node.op)](
                evaluate(node.left), evaluate(node.right))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            value = -evaluate(node.operand)
        else:
            raise ValueError("Only numeric arithmetic is allowed")
        if not math.isfinite(value) or abs(value) > 1e12:
            raise ValueError("Arithmetic result is outside supported limits")
        return value

    try:
        return evaluate(ast.parse(formula, mode="eval").body)
    except (SyntaxError, ZeroDivisionError, OverflowError) as error:
        raise ValueError("Invalid arithmetic formula") from error

def patient_id(name, phone):
    """Hash structured patient details with SHA-256; not anonymization."""
    return hashlib.sha256(json.dumps([name, phone]).encode()).hexdigest()

def generate_rx_number():
    """Generate a random six-digit reference; uniqueness is not guaranteed."""
    return "RX-" + str((100000 + secrets.randbelow(900000)))

def save_stock(filename="pharmacy.json"):
    """Save inventory as UTF-8 JSON, never executable pickle data."""
    with open(filename, "w", encoding="utf-8") as stock_file:
        json.dump(MEDICINES, stock_file)

def load_stock(filename="pharmacy.json"):
    """Validate an entire JSON inventory before replacing live stock."""
    with open(filename, encoding="utf-8") as stock_file:
        stock = json.load(stock_file)
    if not isinstance(stock, dict):
        raise ValueError("Stock must be a JSON object")
    for name, record in stock.items():
        if not isinstance(record, dict) or set(record) != {
                "qty", "price", "expiry"}:
            raise ValueError("Invalid stock record")
        validate_record(name, **record)
    MEDICINES.clear()
    MEDICINES.update(stock)

def print_label(name):
    """Print a label literally without invoking a shell."""
    print("Dispensing label:", name)

def expiring_soon(days=30):
    """Return unexpired medicines expiring within the next days."""
    if (not isinstance(days, int) or isinstance(days, bool)) or days < 0:
        raise ValueError("Days must be a nonnegative integer")
    result = []
    for name, record in MEDICINES.items():
        exp = datetime.strptime(record["expiry"], "%Y-%m-%d").date()
        if 0 <= (exp - date.today()).days < days:
            result.append(name)
    return result

def pharmacist_login(password):
    """Compare a password against explicitly configured credentials."""
    if not isinstance(password, str):
        return False
    expected = os.environ.get("PHARMACY_PASSWORD")
    return bool(expected) and secrets.compare_digest(
        password.encode("utf-8"), expected.encode("utf-8"))

def print_stock():
    """Print a readable inventory report."""
    print("===== Pharmacy Stock Report =====")
    for name, record in MEDICINES.items():
        print(name, "->", record["qty"], "units, Rs.",
              record["price"], "exp", record["expiry"])

def main():
    """Run the standalone pharmacy demonstration."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2099-12-31")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2099-12-31")
    dispense_medicine("Paracetamol 500mg", 30)
    try:
        dispense_medicine("Insulin", 2)
    except ValueError as error:
        print("Dispensing rejected:", error)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login(os.environ.get("PHARMACY_PASSWORD", "")))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()

if __name__ == "__main__":
    main()
