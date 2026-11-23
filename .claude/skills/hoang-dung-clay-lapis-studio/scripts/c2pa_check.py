"""Quét file trước khi đăng: có siêu dữ liệu C2PA / Content Credentials (JUMBF) không.
YouTube tự gắn nhãn AI cho nội dung có C2PA (support.google.com/youtube/answer/14328491).
Dùng: python c2pa_check.py file1 [file2 ...]  -> mã thoát 1 nếu có file chứa C2PA.
shortcut: chỉ dò chuỗi byte (c2pa, jumb), không giải mã manifest; đủ để chặn, cần chi tiết thì dùng c2patool.
"""
import sys
from pathlib import Path

MARKS = (b"c2pa", b"jumb", b"C2PA", b"contentauth")


def has_c2pa(p, chunk=1 << 24):
    with open(p, "rb") as f:
        prev = b""
        while data := f.read(chunk):
            buf = prev + data
            if any(m in buf for m in MARKS):
                return True
            prev = buf[-16:]
    return False


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    bad = [p for p in sys.argv[1:] if has_c2pa(p)]
    for p in sys.argv[1:]:
        print(("CÓ C2PA  " if p in bad else "sạch     ") + Path(p).name)
    sys.exit(1 if bad else 0)
