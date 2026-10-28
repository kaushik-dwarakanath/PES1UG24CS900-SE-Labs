"""Behavioral regression tests for the static-analysis fixes."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from datetime import date, timedelta

import pharmacy_manager as pharmacy


class PharmacyTests(unittest.TestCase):
    """Check failures preserve inventory and unsafe inputs stay inert."""

    def setUp(self):
        pharmacy.MEDICINES.clear()
        pharmacy.add_medicine('Example', 10, 2.5)

    def test_independent_audit_and_explicit_audit(self):
        first = pharmacy.add_medicine('A')
        second = pharmacy.add_medicine('B')
        self.assertIsNot(first, second)
        self.assertEqual(len(first), 1)
        self.assertIs(pharmacy.add_medicine('C', audit=first), first)

    def test_invalid_stock_is_rejected(self):
        for arguments in [(404, 1, 1), ('A', -1, 1), ('A', True, 1),
                          ('A', 1, -1), ('A', 1, float('nan'))]:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    pharmacy.add_medicine(*arguments)
        self.assertEqual(list(pharmacy.MEDICINES), ['Example'])

    def test_dispensing_is_atomic(self):
        for quantity in [0, -1, 11, True, 1.5]:
            with self.assertRaises(ValueError):
                pharmacy.dispense_medicine('Example', quantity)
            self.assertEqual(pharmacy.get_quantity('Example'), 10)
        with self.assertRaises(ValueError):
            pharmacy.dispense_medicine('Missing', 1)
        pharmacy.dispense_medicine('Example', 10)
        self.assertNotIn('Example', pharmacy.MEDICINES)

    def test_expiry_boundaries(self):
        today = date.today()
        for name, offset in [('Old', -1), ('Today', 0), ('Soon', 2),
                             ('Boundary', 30)]:
            pharmacy.add_medicine(name, 2, 1,
                                  (today + timedelta(days=offset)).isoformat())
        self.assertTrue(pharmacy.is_expired('Old'))
        self.assertFalse(pharmacy.is_expired('Today'))
        self.assertEqual(set(pharmacy.expiring_soon()), {'Today', 'Soon'})
        with self.assertRaises(ValueError):
            pharmacy.dispense_medicine('Old', 1)

    def test_billing(self):
        self.assertEqual(pharmacy.bill_amount([('Example', 3)]), 7.5)
        with self.assertRaises(ValueError):
            pharmacy.bill_amount([('Example', -1)])

    def test_arithmetic_rejects_code(self):
        self.assertEqual(pharmacy.calculate_dosage('250 * 2'), 500)
        self.assertEqual(pharmacy.calculate_dosage('-(2 + 3) / 2'), -2.5)
        for formula in ["__import__('os').getcwd()", '2 ** 10000',
                        'True', '[1]', '1 / 0', '1e309', '1 +', '1' * 201]:
            with self.subTest(formula=formula):
                with self.assertRaises(ValueError):
                    pharmacy.calculate_dosage(formula)

    def test_json_roundtrip_and_atomic_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / 'stock.json'
            pharmacy.save_stock(filename)
            pharmacy.MEDICINES.clear()
            pharmacy.load_stock(filename)
            self.assertEqual(pharmacy.get_quantity('Example'), 10)
            for invalid in [[], {'Bad': {'qty': -1, 'price': 1,
                                        'expiry': '2099-12-31'}},
                            {'Bad': {'qty': 1}}]:
                filename.write_text(json.dumps(invalid), encoding='utf-8')
                with self.assertRaises(ValueError):
                    pharmacy.load_stock(filename)
                self.assertEqual(pharmacy.get_quantity('Example'), 10)

    def test_login_requires_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(pharmacy.pharmacist_login(''))
        with patch.dict(os.environ, {'PHARMACY_PASSWORD': 'test-credential'}):
            self.assertTrue(pharmacy.pharmacist_login('test-credential'))
            self.assertFalse(pharmacy.pharmacist_login('wrong'))
            self.assertFalse(pharmacy.pharmacist_login(None))

    def test_identifiers_and_literal_label(self):
        self.assertEqual(len(pharmacy.patient_id('A', '12')), 64)
        self.assertNotEqual(pharmacy.patient_id('A1', '2'),
                            pharmacy.patient_id('A', '12'))
        self.assertRegex(pharmacy.generate_rx_number(), r'^RX-\d{6}$')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            pharmacy.print_label('Example; echo injected')
        self.assertEqual(output.getvalue(),
                         'Dispensing label: Example; echo injected\n')


if __name__ == '__main__':
    unittest.main()
