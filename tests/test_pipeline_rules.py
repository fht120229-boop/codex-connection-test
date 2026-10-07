import unittest

from battery_ocr.qr_decoder import explicit_chemistry_from_text
from battery_ocr.fields import extract_structured_fields


class ChemistryEvidenceTests(unittest.TestCase):
    def test_explicit_lfp_marker(self):
        result = explicit_chemistry_from_text("Battery chemistry: LiFePO4 / LFP")
        self.assertEqual(result["chemistry"], "LFP")
        self.assertTrue(result["explicit"])

    def test_model_code_alone_is_unknown(self):
        self.assertIsNone(explicit_chemistry_from_text("ABC-48120-07"))

    def test_nmc_marker(self):
        self.assertEqual(explicit_chemistry_from_text("三元锂")["chemistry"], "NMC")

    def test_structured_nameplate_fields(self):
        fields = extract_structured_fields("品牌: ACME\n型号: X-100\n25.6 V 100 Ah\nLFP")
        self.assertEqual(fields["brand"], "ACME")
        self.assertEqual(fields["model"], "X-100")
        self.assertEqual(fields["voltage"], "25.6")
        self.assertEqual(fields["capacity"], "100")
        self.assertEqual(fields["chemistry"], "LFP")


if __name__ == "__main__":
    unittest.main()
