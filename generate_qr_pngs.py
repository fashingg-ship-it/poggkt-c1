# -*- coding: utf-8 -*-
"""Generate the two POGGKT silk-print QR PNGs.

- Guide PNG: site-base-url.txt + ?entry=guide
- Support PNG: the Google Form URL in support-qr-url.txt

If support-qr-url.txt has no URL yet, the support PNG is not written.
If assets/SILK_PRINT_LOCKED.txt exists, overwrite is refused unless --force.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H

ROOT = Path(__file__).resolve().parent
SITE_FILE = ROOT / "site-base-url.txt"
SUPPORT_FILE = ROOT / "support-qr-url.txt"
OUT_DIR = ROOT / "assets"
OUT_SUPPORT = OUT_DIR / "qr-entry-support-20261104已确认发丝印厂.png"
OUT_GUIDE = OUT_DIR / "qr-entry-guide-20261104已确认发丝印厂.png"
OUT_README = OUT_DIR / "qr-encoded-urls.txt"
LOCK_FILE = OUT_DIR / "SILK_PRINT_LOCKED.txt"


def first_url_line(path: Path) -> str:
    if not path.is_file():
        return ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if re.match(r"^https?://", s, re.I):
            return s.strip()
    return ""


def normalize_base(raw: str) -> str:
    s = raw.strip()
    if not re.match(r"^https?://", s, re.I):
        s = "https://" + s
    if not s.endswith("/"):
        s += "/"
    return s


def read_base_url() -> str:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args and args[0].strip():
        return normalize_base(args[0].strip())
    found = first_url_line(SITE_FILE)
    if not found:
        sys.exit(f"No http(s) URL in {SITE_FILE.name}")
    return normalize_base(found)


def is_force() -> bool:
    return "--force" in sys.argv[1:]


def clear_read_only(path: Path) -> None:
    if path.is_file():
        try:
            path.chmod(path.stat().st_mode | 0o222)
        except OSError:
            pass


def fitted_version(data: str) -> int:
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    return int(qr.version)


def write_png(path: Path, data: str, version: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clear_read_only(path)
    qr = qrcode.QRCode(
        version=version,
        error_correction=ERROR_CORRECT_H,
        box_size=14,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=False)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)


def refuse_if_locked() -> None:
    if not LOCK_FILE.is_file():
        return
    if is_force():
        print("WARNING: --force overrides the silk-print lock. Printed packs will not match.")
        return
    print("REFUSED — silk-print QR PNGs are locked.")
    print(f"Lock marker: {LOCK_FILE}")
    print("To reprint on purpose: python generate_qr_pngs.py --force")
    sys.exit(2)


def main() -> None:
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("Usage: python generate_qr_pngs.py [base-url] [--force]")
        return

    refuse_if_locked()

    base = read_base_url()
    u_guide = base.rstrip("/") + "/?entry=guide"
    u_support = first_url_line(SUPPORT_FILE)

    version = fitted_version(u_guide)
    if u_support:
        version = max(version, fitted_version(u_support))

    write_png(OUT_GUIDE, u_guide, version)
    support_note = "NOT GENERATED — paste a Google Form viewform URL into support-qr-url.txt, then run again."
    if u_support:
        if "docs.google.com/forms/" not in u_support:
            sys.exit("support-qr-url.txt must be a docs.google.com/forms viewform link.")
        write_png(OUT_SUPPORT, u_support, version)
        support_note = u_support

    lines = [
        "These URLs are encoded inside the PNG files (for silk print verification).",
        "",
        "qr-entry-guide-20261104已确认发丝印厂.png (opens Quick start; choose Knee, Shoulder, Hip, or Foot on the page)",
        f"  {u_guide}",
        "",
        "qr-entry-support-20261104已确认发丝印厂.png (opens the Google Form directly)",
        f"  {support_note}",
        "",
    ]
    OUT_README.write_text("\n".join(lines), encoding="utf-8")

    print(f"QR version {version}, error correction H, same module size on both codes")
    print("OK — guide QR")
    print(" ", OUT_GUIDE)
    print(" ", u_guide)
    if u_support:
        print("OK — support QR")
        print(" ", OUT_SUPPORT)
        print(" ", u_support)
    else:
        print("SKIP — support QR. Add the new Google Form link to support-qr-url.txt and run again.")
    print(" ", OUT_README)


if __name__ == "__main__":
    main()
