#!/usr/bin/env python3
"""news-23 b15 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Reads the bundled entry.png next to this file, verifies its PNG
header (signature + IHDR 1024x1024 + IEND trailer), and writes the copy ONLY to
MAKEFUN_OUTPUT_DIR. Never writes next to itself: the graded run happens in a
read-only repo copy, so any write beside main.py would fail.
"""
import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError("entry.png must be 1024x1024, got %dx%d" % (width, height))
    if len(data) > 1024 * 1024:
        raise ValueError("entry.png exceeds 1 MiB")
    # IEND trailer: last 12 bytes must be length 0 + "IEND" + CRC.
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        raise ValueError("entry.png is truncated (missing IEND trailer)")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if os.path.abspath(out_dir) == os.path.abspath(here):
        raise ValueError("MAKEFUN_OUTPUT_DIR must point outside the repo")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    print("wrote", dst, len(data), "bytes")


if __name__ == "__main__":
    main()
