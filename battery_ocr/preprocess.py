"""OpenCV preprocessing used before nameplate OCR."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


@dataclass
class PreprocessedImage:
    original: np.ndarray
    gray: np.ndarray
    binary: np.ndarray


def preprocess_image(image_path: str, max_side: int = 1600, min_side: int = 900) -> PreprocessedImage:
    """Resize, grayscale, denoise and threshold an image for OCR.

    The original color image is retained for QR decoding and the binary image
    is intended for text recognition. Resizing preserves aspect ratio.
    """

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"cannot read image: {image_path}")
    height, width = image.shape[:2]
    long_side = max(height, width)
    if long_side < min_side:
        # Small phone thumbnails benefit from a bounded upscale before OCR.
        scale = min(2.0, float(max_side) / long_side)
    else:
        scale = min(1.0, float(max_side) / long_side)
    if scale != 1.0:
        interpolation = cv2.INTER_CUBIC if scale > 1.0 else cv2.INTER_AREA
        image = cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=interpolation)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, 7, 50, 50)
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
    )
    return PreprocessedImage(original=image, gray=denoised, binary=binary)


def save_debug_images(result: PreprocessedImage, directory: str) -> dict:
    """Save intermediate images for debugging and return their paths."""

    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "gray": output / "gray.png",
        "binary": output / "binary.png",
    }
    cv2.imwrite(str(paths["gray"]), result.gray)
    cv2.imwrite(str(paths["binary"]), result.binary)
    return {key: str(value) for key, value in paths.items()}
