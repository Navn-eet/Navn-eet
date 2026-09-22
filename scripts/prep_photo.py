#!/usr/bin/env python3

from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py <source-image>")
        sys.exit(1)

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"Error: image not found: {source}")
        sys.exit(1)

    output = source.with_name("source-prepped.png")

    image = Image.open(source).convert("RGB")
    image_np = np.array(image)

    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Improve local contrast while avoiding extreme global contrast.
    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8),
    )

    enhanced = clahe.apply(gray)

    # Normalize gently so the subject remains readable.
    enhanced = cv2.normalize(
        enhanced,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    )

    # Put the result onto a white background.
    white = np.full_like(enhanced, 255)
    result = np.minimum(enhanced, white)

    Image.fromarray(result).save(output)

    print(f"Created: {output}")


if __name__ == "__main__":
    main()
