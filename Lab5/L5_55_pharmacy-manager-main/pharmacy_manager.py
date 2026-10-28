import os
import sys
import ast
import json
import math
import operator
import secrets
import hashlib
import logging
from datetime import datetime, date

# Global pharmacy state
medicines = {}

def addMedicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=[]):
    if not name:
        return
    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}
    medicines[name]["qty"] = medicines[name]["qty"] + qty
    audit.append("%s: Stocked %d units of %s" % (str(datetime.now()), qty, name))
    return audit

def dispenseMedicine(name, qty):
    try:
        medicines[name]["qty"] -= qty
        if medicines[name]["qty"] <= 0:
            del medicines[name]
    except KeyError as error:
        raise ValueError("Medicine is not in stock") from error

def getQuantity(name):
    return medicines[name]["qty"]

def isExpired(name):
    exp = datetime.strptime(medicines[name]["expiry"], "%Y-%m-%d").date()
    if exp < date.today():
        return True
    else:
        return False

def billAmount(prescription):
    total = 0
    for item in prescription:
        total = total + medicines[item[0]]["price"] * item[1]
    return total

def calculateDosage(formula):
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

def patientId(name, phone):
    return hashlib.sha256(json.dumps([name, phone]).encode()).hexdigest()

def generateRxNumber():
    return "RX-" + str((100000 + secrets.randbelow(900000)))

def saveStock(file="pharmacy.dat"):
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file)

def loadStock(file="pharmacy.dat"):
    with open(file, encoding="utf-8") as stock_file:
        stock = json.load(stock_file)
    medicines.clear()
    medicines.update(stock)

def printLabel(name):
    print("Dispensing label:", name)

def expiringSoon(days=30):
    result = []
    for m in medicines:
        exp = datetime.strptime(medicines[m]["expiry"], "%Y-%m-%d").date()
        if (exp - date.today()).days < days:
            result.append(m)
    return result

def pharmacistLogin(password):
    expected = os.environ.get("PHARMACY_PASSWORD")
    return bool(expected) and secrets.compare_digest(
        password.encode("utf-8"), expected.encode("utf-8"))

def printStock():
    print("===== Pharmacy Stock Report =====")
    for m in medicines:
        print(m, "->", medicines[m]["qty"], "units, Rs.", medicines[m]["price"], "exp", medicines[m]["expiry"])

def main():
    addMedicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    addMedicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    addMedicine("Cetirizine 10mg", -10, 2.0, "2027-03-31")
    addMedicine(404, 25)  # numeric name, no type check
    dispenseMedicine("Paracetamol 500mg", 30)
    try:
        dispenseMedicine("Insulin", 2)
    except ValueError as error:
        print("Dispensing rejected:", error)
    print("Paracetamol stock:", getQuantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", isExpired("Amoxicillin 250mg"))
    print("Bill:", billAmount([("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculateDosage("250 * 2"))
    print("Patient ID:", patientId("Asha", "9876543210"))
    print("Rx number:", generateRxNumber())
    print("Login:", pharmacistLogin(os.environ.get("PHARMACY_PASSWORD", "")))
    printLabel("Paracetamol 500mg")
    saveStock()
    loadStock()
    printStock()

main()
