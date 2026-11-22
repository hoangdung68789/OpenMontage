"""Tự kiểm một phần kịch bản trước khi đi tiếp (thay cho việc anh duyệt từng phần trong chế độ tự lái).

  python qa_check.py <script_partN.md> [--min-words 700] [--mark]

Kiểm:
  1. Lời thoại (dòng bắt đầu bằng '> ') không chứa [Chưa xác minh], [unverified], TODO, ??, XXX.
  2. Đủ số từ lời thoại (mặc định >= 700 mỗi phần).
  3. Có mục Nguồn với >= 3 link; báo tỉ lệ đoạn có dòng '- Nguồn:'.
  4. Không trùng lời đối thủ: so cụm 8 từ với mọi phụ đề trong channel-studio/research (chống "reused content").
  5. Số từ ghi trong file ("Số từ: ...") phải khớp số từ lời thoại thật (lệch tối đa 15%), chống báo sai tiến độ.
  6. Cờ chính sách (cần anh xem): mô tả bạo lực chi tiết, tự hại, lời khuyên tài chính/sức khỏe/pháp lý.
Kết quả: <file>.qa.md cạnh kịch bản. Mã thoát 0 = QA ĐẠT, 2 = HỎNG (AI tự sửa), 3 = CẦN ANH XEM (đưa vào lô duyệt tuần).
--mark: khi đạt, thêm "· QA ĐẠT <ngày>" vào dòng tiêu đề (autopilot đọc dấu này).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, rel, today, utf8  # noqa: E402

BAD_MARKERS = r"\[Chưa xác minh\]|\[unverified\]|\bTODO\b|\?\?|\bXXX\b|\[cần kiểm\]"
POLICY = {
    "bạo lực chi tiết": r"\b(gore|gory|dismember\w*|decapitat\w*|disembowel\w*|entrails|mutilat\w*|blood spray\w*)\b",
    "tự hại": r"\b(suicide method|how to kill yourself|self-harm)\b",
    "lời khuyên tài chính/sức khỏe/pháp lý": r"\b(you should (invest|buy|sell|take)|guaranteed returns|cures? (cancer|disease)|legal advice)\b",
    "bạo lực tình dục": r"\b(rape|raped|sexual assault)\b",
}


def shingles(words, n=8):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def norm_words(t):
    return re.findall(r"[a-z0-9']+", t.lower())


def competitor_shingles():
    sh = set()
    for f in list(CS.glob("research/**/*.vtt")) + list(CS.glob("research/**/*.srt")) + list(CS.glob("research/**/subs/*.txt")):
        txt = re.sub(r"\d{2}:\d{2}[:.,\d ->]*|WEBVTT.*|<[^>]+>|(align|position|line|size):\S+", " ", f.read_text(encoding="utf-8", errors="ignore"))
        sh |= shingles(norm_words(txt))
    return sh


def main():
    utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--min-words", type=int, default=700)
    ap.add_argument("--mark", action="store_true")
    a = ap.parse_args()
    f = Path(a.script)
    t = f.read_text(encoding="utf-8")
    narr = [l[2:] for l in t.splitlines() if l.startswith("> ")]
    narration = "\n".join(narr)
    words = norm_words(narration.replace("[pause]", " "))
    segs = re.split(r"(?m)^### ", t)[1:]
    with_src = sum(1 for s in segs if re.search(r"(?m)^- Nguồn:", s))
    links = len(re.findall(r"https?://", t))
    fails, review, info = [], [], []
    bad = re.findall(BAD_MARKERS, narration, re.I)
    if bad:
        fails.append(f"lời thoại còn dấu chưa kiểm: {', '.join(sorted(set(bad)))} (bỏ khỏi lời thoại hoặc kiểm xong)")
    if len(words) < a.min_words:
        fails.append(f"lời thoại {len(words)} từ < {a.min_words}")
    if links < 3 or not re.search(r"(?im)^#+\s*Nguồn", t):
        fails.append(f"thiếu mục '## Nguồn' với >= 3 link (đang có {links} link)")
    claim = re.search(r"Số từ:\s*\**\s*(?:khoảng\s*)?([\d.,]+)", t)
    if claim:
        claimed = int(re.sub(r"[.,]", "", claim.group(1)))
        if claimed and abs(claimed - len(words)) / claimed > 0.15:
            fails.append(f"file ghi 'Số từ: {claim.group(1)}' nhưng lời thoại thật có {len(words)} từ "
                         f"(lệch {abs(claimed - len(words)) / claimed:.0%}); sửa con số và các mốc giờ, hoặc viết bổ sung")
    info.append(f"Lời thoại: {len(words)} từ (khoảng {len(words) / 125:.1f} phút ở 125 từ/phút). Đoạn có dòng Nguồn: {with_src}/{len(segs)}.")
    comp = competitor_shingles()
    mine = shingles(words)
    overlap = mine & comp
    rate = len(overlap) / max(len(mine), 1)
    info.append(f"Trùng cụm 8 từ với phụ đề đối thủ trong research/: {len(overlap)} cụm ({rate:.1%}).")
    if rate > 0.02 or len(overlap) >= 5:
        fails.append(f"trùng lời đối thủ {rate:.1%} ({len(overlap)} cụm 8 từ), ví dụ: \"{sorted(overlap)[0]}\". Viết lại bằng lời của mình")
    for k, rx in POLICY.items():
        hits = sorted(set(m.group(0) for m in re.finditer(rx, narration, re.I)))
        if hits:
            review.append(f"{k}: {', '.join(hits[:5])}")
    verdict = "HỎNG" if fails else "CẦN ANH XEM" if review else "QA ĐẠT"
    out = [f"# QA {f.name} — {today()}: **{verdict}**", ""] + [f"- {x}" for x in info]
    out += ["", "## Lỗi phải sửa"] + ([f"- {x}" for x in fails] or ["- (không có)"])
    out += ["", "## Cần anh xem (đưa vào lô duyệt tuần)"] + ([f"- {x}" for x in review] or ["- (không có)"])
    qf = f.with_suffix(".qa.md")
    qf.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    print(f"\nĐã ghi {rel(qf)}")
    if verdict == "QA ĐẠT" and a.mark:
        lines = t.splitlines()
        if "QA ĐẠT" not in lines[0]:
            lines[0] = lines[0].rstrip() + f" · QA ĐẠT {today()}"
            f.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print("Đã đánh dấu QA ĐẠT ở dòng tiêu đề.")
    sys.exit(0 if verdict == "QA ĐẠT" else 2 if fails else 3)


if __name__ == "__main__":
    main()
