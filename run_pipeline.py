#!/usr/bin/env python3
"""Run the battery OCR pipeline and print JSON."""

import argparse
import json

from battery_ocr import BatteryOCRPipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--yolo-model", help="optional YOLO text detector weights")
    parser.add_argument("--no-paddle", action="store_true", help="skip PaddleOCR")
    args = parser.parse_args()
    result = BatteryOCRPipeline(yolo_model=args.yolo_model, use_paddle=not args.no_paddle).run(args.image)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
