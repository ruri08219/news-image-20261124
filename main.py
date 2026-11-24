#!/usr/bin/env python3
"""news-image-20261124 entry: ship the finished image, copy it to /output.

The image (entry.png, 1024x1024) was rendered locally in the builder session
with Pillow and is shipped in this repository. This program uses only the
Python standard library: it verifies the shipped file (PNG magic bytes,
size, SHA-256, 1 MiB gate) and copies it byte-for-byte to /output/entry.png.
It is deterministic: two runs write the same bytes.
"""
import hashlib
import pathlib
import sys

EXPECTED_SHA256 = "e6e1e3ebb02a4bfc45a4aa3fcc88bfeff6be48f0050d6a15a7d2f4a566ee23c7"
EXPECTED_SIZE = 187527
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    src = pathlib.Path(__file__).with_name("entry.png")
    data = src.read_bytes()
    if data[:8] != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) != EXPECTED_SIZE:
        print(f"entry.png size {len(data)} != {EXPECTED_SIZE}", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("entry.png sha256 mismatch", file=sys.stderr)
        return 1
    outdir = pathlib.Path("/output")
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "entry.png"
    out.write_bytes(data)
    check = out.read_bytes()
    if hashlib.sha256(check).hexdigest() != EXPECTED_SHA256:
        print("written copy sha256 mismatch", file=sys.stderr)
        return 1
    print(f"wrote /output/entry.png ({len(check)} bytes, sha256 {digest[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
