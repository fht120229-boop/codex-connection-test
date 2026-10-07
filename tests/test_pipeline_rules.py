import unittest

from battery_ocr.qr_decoder import explicit_chemistry_from_text


class ChemistryEvidenceTests(unittest.TestCase):
    def test_explicit_lfp_marker(self):
        result = explicit_chemistry_from_text("Battery chemistry: LiFePO4 / LFP")
        self.assertEqual(result["chemistry"], "LFP")
        self.assertTrue(result["explicit"])

    def test_model_code_alone_is_unknown(self):
        self.assertIsNone(explicit_chemistry_from_text("ABC-48120-07"))

    def test_nmc_marker(self):
        self.assertEqual(explicit_chemistry_from_text("三元锂")["chemistry"], "NMC")


if __name__ == "__main__":
    unittest.main()
