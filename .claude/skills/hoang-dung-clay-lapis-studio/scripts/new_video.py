"""Tạo thư mục video theo cấu trúc dựng v2 (references/edit-workflow.md §1) và sinh bảng âm thanh.

  python new_video.py create 003-slug --title "The Lost Patrol" --genre survival [--pillar P2]
  python new_video.py cuesheet <render/project/sfx_cues.json> <05_sound/CUE_SHEET.md>

Không bao giờ ghi đè file đã có (chạy lại an toàn).
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
REPO = SK.parents[2]
TEMPLATE = SK / "templates" / "video-project"
VIDEOS = REPO / "channel-studio" / "videos"
GENRES = {"war", "mystery", "disaster", "ancient", "survival", "default"}
PILLAR_OF = {"mystery": "P1", "survival": "P2", "war": "P3", "disaster": "P4", "ancient": "P5", "default": "?"}
EXTRA_DIRS = ["03_assets/img", "03_assets/video", "03_assets/maps", "03_assets/audio/vo",
              "03_assets/audio/music", "03_assets/audio/sfx"]
CAUSE = {"land": "tiêu đề đáp", "pop": "điểm/mốc/số xuất hiện", "whoosh": "chuyển cảnh nhanh (whip/wipe/iris) hoặc cụm ảnh",
         "impact": "lóe sáng / số lớn / cao trào", "riser": "dồn vào cao trào", "type": "chữ đánh máy"}


def create(slug, title, genre, pillar, root=VIDEOS):
    if not re.fullmatch(r"\d{3}-[a-z0-9-]+", slug):
        sys.exit("slug phải dạng NNN-ten-video (ví dụ 003-lost-patrol)")
    if genre not in GENRES:
        sys.exit(f"genre phải là một trong {sorted(GENRES)}")
    dest = root / slug
    subs = {"{{NNN}}": slug[:3], "{{SLUG}}": slug, "{{TITLE}}": title, "{{GENRE}}": genre,
            "{{PILLAR}}": pillar or PILLAR_OF[genre], "{{DATE}}": dt.date.today().isoformat(),
            "{{TITLE_TEXT}}": title.replace('"', "'")}
    made, kept = [], []
    for src in sorted(TEMPLATE.rglob("*")):
        if src.is_dir():
            continue
        out = dest / src.relative_to(TEMPLATE)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            kept.append(out)
            continue
        if src.name == ".keep":
            out.touch()
        else:
            text = src.read_text(encoding="utf-8")
            for k, v in subs.items():
                text = text.replace(k, v)
            out.write_text(text, encoding="utf-8")
        made.append(out)
    for d in EXTRA_DIRS:
        (dest / d).mkdir(parents=True, exist_ok=True)
    print(f"Thư mục video: {dest}")
    print(f"  tạo mới {len(made)} file, giữ nguyên {len(kept)} file đã có")
    print("  Tiếp: viết 00_brief/script_outline.md (GĐ 1), quy trình ở references/edit-workflow.md")
    return dest


def cuesheet(cues_json, out_md):
    data = json.loads(Path(cues_json).read_text(encoding="utf-8"))
    rows = [f"| {c['t_picture']:.2f} | {Path(c['file']).stem} | {CAUSE.get(c['kind'], c['kind'])} (cảnh {c.get('scene', '?')}) | {c['volume']:.2f} |"
            for c in sorted(data.get("cues", []), key=lambda c: c["t_picture"])]
    trans = [t for t in data.get("transitions", []) if t != "none"]
    body = ["# Bảng hiệu ứng âm thanh", "",
            f"Thể loại: `{data.get('genre')}` · {len(rows)} tiếng · chuyển cảnh: {', '.join(trans)}", "",
            "| Giây (hình) | Tiếng | Nguyên nhân | Âm lượng |", "|---|---|---|---|", *rows, ""]
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_md).write_text("\n".join(body), encoding="utf-8")
    print(f"Đã ghi {out_md} ({len(rows)} tiếng)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("create")
    c.add_argument("slug")
    c.add_argument("--title", required=True)
    c.add_argument("--genre", default="default")
    c.add_argument("--pillar")
    c.add_argument("--root", type=Path, default=VIDEOS)
    q = sp.add_parser("cuesheet")
    q.add_argument("cues_json")
    q.add_argument("out_md")
    a = ap.parse_args(argv)
    if a.cmd == "create":
        create(a.slug, a.title, a.genre, a.pillar, a.root)
    else:
        cuesheet(a.cues_json, a.out_md)


if __name__ == "__main__":
    main()
