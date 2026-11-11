# cutest-cat-01 entrypoint (Python 3.13 / standard library only)
# Draws the cutest cat by providing entry.png to the evaluation sandbox
import os
import shutil
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    src = base_dir / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"Successfully copied {src} to {dst} ({dst.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
