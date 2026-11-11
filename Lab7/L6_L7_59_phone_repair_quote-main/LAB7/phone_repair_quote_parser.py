"""Defensive input parsers for phone repair quotes."""


def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four digits.
    Non-strings, empty values and non-ASCII digits return an empty string.
    Short digit strings remain visible; length/checksum validation is separate.
    """
    if not isinstance(imei, str):
        return ""
    imei = imei.replace('-', '').replace(' ', '')
    if not imei or any(char not in "0123456789" for char in imei):
        return ""
    return '*' * (len(imei) - 4) + imei[-4:]


def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a {part: quantity} dictionary.
    Skip malformed entries; accept positive ASCII integer quantities only.
    Require whitespace before the quantity marker, allowing names like 'box'.
    For duplicate part names, the last valid quantity wins (original behavior).
    Quantities exceeding 4300 digits are rejected before integer conversion.
    """
    order = {}
    if not isinstance(text, str):
        return order
    for item in text.split(';'):
        part, marker, qty = item.rpartition("x")
        if not marker or not part or not part[-1].isspace():
            continue
        part = part.strip()
        qty = qty.strip()
        if (not part or not qty or len(qty) > 4300
                or any(char not in "0123456789" for char in qty)):
            continue
        try:
            quantity = int(qty)
        except ValueError:
            # Respect a stricter interpreter integer-string conversion limit.
            continue
        if quantity > 0:
            order[part] = quantity
    return order


def parse_model(text):
    """
    Splits 'Brand Model name' into a (brand, model) tuple.
    Normalize whitespace; a brand alone returns (brand, '').
    Empty and non-string inputs return ('', '').
    """
    if not isinstance(text, str):
        return "", ""
    words = text.split()
    if not words:
        return "", ""
    return words[0].title(), " ".join(words[1:])


def main():
    print("==== Running mask_imei ====")
    value = input("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    print("Masked IMEI:", mask_imei(value))

    print("\n==== Running parse_parts_order ====")
    value = input("Enter parts and quantities as PART xQTY separated by ; (e.g. screen x1; battery x2): ")
    print("Parts order:", parse_parts_order(value))

    print("\n==== Running parse_model ====")
    value = input("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    print("Brand and model:", parse_model(value))


if __name__ == "__main__":
    main()
