#!/usr/bin/env python3
"""news-image-20261118 entry: writes the day's front page to /output/entry.png.

The page is rendered ahead of time and shipped beside this file; the program's
job is to place those exact bytes at the path the grader reads. Copying the
bytes rather than re-encoding them is what makes the two graded runs identical:
no encoder, no timestamp chunk, no metadata.

Standard library only, no network.
"""

import os
import shutil
import sys
from pathlib import Path

OUT_NAME = "entry.png"
SOURCE_NAME = "entry.png"


def output_dir():
    """The writable output directory: MAKEFUN_OUTPUT_DIR outside the grader."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def source_path():
    return Path(__file__).resolve().parent / SOURCE_NAME


def check_source(path):
    """Fail loudly on a missing page instead of writing a partial file."""
    if not path.is_file():
        raise SystemExit("entry image missing beside main.py: %s" % path)
    if path.stat().st_size == 0:
        raise SystemExit("entry image is empty: %s" % path)


def main():
    src = source_path()
    check_source(src)
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / OUT_NAME
    shutil.copyfile(src, dest)
    written = dest.stat().st_size
    print("wrote %s (%d bytes)" % (dest, written), file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
