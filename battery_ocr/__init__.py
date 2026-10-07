"""Battery nameplate OCR and code-decoding pipeline.

The package keeps chemistry classification evidence-based: an image alone does
not become LFP/NMC unless the nameplate or decoded code contains an explicit
marker.
"""

__all__ = ["BatteryOCRPipeline", "explicit_chemistry_from_text"]


def __getattr__(name):
    # Keep imports usable for evidence-only tooling that does not install the
    # optional OpenCV/Paddle/YOLO stack.
    if name == "BatteryOCRPipeline":
        from .pipeline import BatteryOCRPipeline
        return BatteryOCRPipeline
    if name == "explicit_chemistry_from_text":
        from .qr_decoder import explicit_chemistry_from_text
        return explicit_chemistry_from_text
    raise AttributeError(name)
