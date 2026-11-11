"""Entrypoint script for make.fun competition 'cutest-cat-01'.

This script loads the submission candidate `entry.png`, validates its
integrity and formatting (verifying file existence, standard magic bytes
for PNG or JPEG formats, and keeping the file size under the 1 MB evaluation limit),
and copies the validated image to the destination directory specified by the
`MAKEFUN_OUTPUT_DIR` environment variable (defaulting to `/output`).
"""

import os
import shutil
import sys
from pathlib import Path

# Standard image format signature headers (magic bytes)
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
JPEG_HEADER = b"\xff\xd8\xff"

# Maximum allowable file size in bytes (1 MB = 1,048,576 bytes)
MAX_FILE_SIZE_BYTES = 1048576


def validate_image(path: Path) -> str:
    """Validate that the target file exists, is within size limits, and has valid magic bytes.

    Args:
        path: Path object pointing to the image file to inspect.

    Returns:
        str: Detected image format identifier ("PNG" or "JPEG").

    Raises:
        FileNotFoundError: If the specified file does not exist or is not a regular file.
        ValueError: If the file is empty, exceeds MAX_FILE_SIZE_BYTES, or has invalid magic bytes.
    """
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    file_size = path.stat().st_size
    if file_size == 0:
        raise ValueError(f"Image file is empty: {path}")
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File size ({file_size} bytes) exceeds maximum allowed limit of {MAX_FILE_SIZE_BYTES} bytes."
        )

    with path.open("rb") as f:
        header = f.read(8)

    if header.startswith(PNG_HEADER):
        return "PNG"
    elif header.startswith(JPEG_HEADER):
        return "JPEG"
    else:
        raise ValueError(f"Unrecognized image format for {path}. Expected PNG or JPEG magic bytes.")


def main() -> None:
    """Primary execution entrypoint for the competition evaluator."""
    script_dir = Path(__file__).resolve().parent
    entry_path = script_dir / "entry.png"
    if not entry_path.exists():
        entry_path = Path("entry.png").resolve()

    if not entry_path.exists():
        print(f"Error: Entry file not found at {entry_path}", file=sys.stderr)
        sys.exit(1)

    try:
        fmt = validate_image(entry_path)
    except Exception as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        sys.exit(1)

    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_dir = Path(output_dir_env)
    output_dir.mkdir(parents=True, exist_ok=True)

    dest_path = output_dir / "entry.png"
    shutil.copy2(entry_path, dest_path)
    print(f"Successfully validated {fmt} image ({entry_path.stat().st_size} bytes) and copied to {dest_path}")


if __name__ == "__main__":
    main()
