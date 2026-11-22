"""Bộ nhớ series nhiều tập của ICYFOX: nhớ tập đã làm, viết tiếp đúng mạch, và kết thúc đúng tập đã định.

  python series.py new <id> --title "..." --pillar P2 --episodes 3 --premise "..." --arc "Tập 1 ...|Tập 2 ...|Tập 3 ..."
  python series.py brief <id> [--episode N] [--out file.md]     # BẮT BUỘC chạy trước khi viết một tập
  python series.py episode <id> N [--title ..] [--video-dir ..] [--status planned|scripting|approved|rendered|published]
                         [--summary ..] [--cliffhanger ..] [--open "tuyến 1|tuyến 2"] [--close TH1,TH2]
                         [--youtube-id ..] [--date YYYY-MM-DD]
  python series.py fact <id> "dữ kiện cần nhất quán" --source "link" [--ep N]
  python series.py extend <id> --to N --reason "số liệu: ..."   # chỉ khi có số liệu và anh đồng ý
  python series.py end <id> --next "câu chuyện kế tiếp"          # đóng series sau khi tập cuối đã đăng
  python series.py cancel <id> --reason "..."
  python series.py status | render

Dữ liệu: channel-studio/series/<id>/series.json (nguồn), SERIES.md và series/SERIES_INDEX.md (tự sinh).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icyfox_common import CS, load_json, rel, save_json, today, utf8  # noqa: E402

DIR = CS / "series"
EP_STATUS = ["planned", "scripting", "approved", "rendered", "published"]
EP_LABEL = {"planned": "dự kiến", "scripting": "đang viết", "approved": "đã duyệt kịch bản",
            "rendered": "đã dựng", "published": "đã đăng"}
S_LABEL = {"planned": "Chưa bắt đầu", "running": "Đang chạy", "ended": "ĐÃ KẾT THÚC", "cancelled": "Đã hủy"}


def path(sid):
    return DIR / sid / "series.json"


def load(sid):
    s = load_json(path(sid), None)
    if s is None:
        sys.exit(f"Không có series '{sid}'. Xem: python series.py status")
    return s


def all_series():
    return [load_json(p, {}) for p in sorted(DIR.glob("*/series.json"))]


def ep(s, n):
    for e in s["episodes"]:
        if e["n"] == n:
            return e
    return None


def open_threads(s):
    return [t for t in s["threads"] if not t.get("closed_in")]


def published(s):
    return [e for e in s["episodes"] if e["status"] == "published"]


def next_ep(s):
    for e in sorted(s["episodes"], key=lambda e: e["n"]):
        if e["status"] != "published":
            return e
    return None


def log(s, msg):
    s.setdefault("log", []).append(f"{today()} {msg}")


def save(s):
    save_json(path(s["id"]), s)
    render_one(s)
    render_index()


def render_one(s):
    N = s["planned_episodes"]
    out = [f"# Series: {s['title']}", "",
           f"Tự sinh từ `series.json`, đừng sửa tay. Trạng thái: **{S_LABEL[s['status']]}** · Trụ cột {s.get('pillar', '')} · "
           f"**Kết thúc ở tập {N}** · Đã đăng {len(published(s))}/{N}", "",
           f"**Tiền đề:** {s.get('premise', '')}", "", "## Mạch truyện đã định", ""]
    out += [f"{i + 1}. {a}" for i, a in enumerate(s.get("arc", []))]
    out += ["", "## Các tập", "", "| Tập | Tiêu đề | Trạng thái | Ngày đăng | Thư mục | Tóm tắt | Kết tập (cliffhanger) |",
            "|---|---|---|---|---|---|---|"]
    for e in sorted(s["episodes"], key=lambda e: e["n"]):
        final = " (TẬP CUỐI)" if e["n"] == N else ""
        out.append(f"| {e['n']}/{N}{final} | {e.get('title', '')} | {EP_LABEL[e['status']]} | {e.get('date', '')} | "
                   f"{e.get('video_dir', '')} | {e.get('summary', '')} | {e.get('cliffhanger', '')} |")
    out += ["", "## Tuyến truyện", ""]
    out += [f"- {t['id']} ({'mở' if not t.get('closed_in') else 'đã khép ở tập ' + str(t['closed_in'])}, "
            f"mở ở tập {t['opened_in']}): {t['text']}" for t in s["threads"]] or ["(chưa có)"]
    out += ["", "## Dữ kiện phải nhất quán", ""]
    out += [f"- {f['text']} (tập {f.get('ep', '-')}; nguồn: {f.get('source', '')})" for f in s.get("facts", [])] or ["(chưa có)"]
    if s["status"] == "ended":
        out += ["", f"**Series kết thúc ngày {s.get('ended')}.** Câu chuyện kế tiếp: {s.get('next_story', '')}"]
    out += ["", "## Nhật ký", ""] + [f"- {x}" for x in s.get("log", [])]
    (DIR / s["id"] / "SERIES.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def render_index():
    DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in all_series():
        if not s:
            continue
        nx = next_ep(s)
        nxt = (f"tập {nx['n']}" + (" (TẬP CUỐI)" if nx["n"] == s["planned_episodes"] else "")) if nx and s["status"] in ("planned", "running") else "-"
        rows.append(f"| {s['id']} | {s['title']} | {S_LABEL[s['status']]} | {len(published(s))}/{s['planned_episodes']} | "
                    f"{nxt} | {len(open_threads(s))} | {s.get('next_story', '') if s['status'] == 'ended' else ''} |")
    out = ["# Danh sách series", "", "Tự sinh bởi `series.py`. Quy tắc: `references/series-playbook.md`.", "",
           "| ID | Tên | Trạng thái | Đã đăng | Tập kế tiếp | Tuyến còn mở | Câu chuyện kế tiếp |",
           "|---|---|---|---|---|---|---|"] + (rows or ["| (chưa có series) | | | | | | |"])
    (DIR / "SERIES_INDEX.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def brief(s, n=None):
    N = s["planned_episodes"]
    e = ep(s, n) if n else next_ep(s)
    if s["status"] in ("ended", "cancelled"):
        return f"Series '{s['title']}' {S_LABEL[s['status']]}. KHÔNG viết thêm tập. Câu chuyện kế tiếp: {s.get('next_story', '')}"
    if not e:
        return f"Mọi tập đã đăng. Chạy: python series.py end {s['id']} --next \"...\""
    n = e["n"]
    prev = ep(s, n - 1)
    L = [f"# BỐI CẢNH ĐỂ VIẾT: {s['title']} — Tập {n}/{N}" + (" — TẬP CUỐI" if n == N else ""), "",
         f"Tiền đề series: {s.get('premise', '')}",
         f"Mạch đã định cho tập này: {s['arc'][n - 1] if n - 1 < len(s.get('arc', [])) else '(chưa ghi)'}", ""]
    L.append("## Câu chuyện đến nay")
    for x in sorted(s["episodes"], key=lambda x: x["n"]):
        if x["n"] < n:
            L.append(f"- Tập {x['n']} ({EP_LABEL[x['status']]}): {x.get('summary') or '(CHƯA có tóm tắt: viết bù trước khi làm tiếp)'}")
    if n == 1:
        L.append("- (đây là tập mở đầu)")
    if prev:
        L += ["", f"## Tập trước kết ở đâu (phải nối tiếp đúng chỗ này)", f"{prev.get('cliffhanger') or '(chưa ghi cliffhanger tập trước: ghi bù)'}"]
    th = open_threads(s)
    L += ["", "## Tuyến truyện đang mở"] + ([f"- {t['id']}: {t['text']} (mở ở tập {t['opened_in']})" for t in th] or ["- (không có)"])
    L += ["", "## Dữ kiện phải nhất quán"] + ([f"- {f['text']} [{f.get('source', '')}]" for f in s.get("facts", [])] or ["- (chưa có)"])
    L += ["", "## Yêu cầu bắt buộc cho tập này"]
    if n > 1:
        L.append("- Mở bằng đoạn nhắc lại tập trước, tối đa 45 giây, có ý mới (không chép lại lời tập trước).")
    L.append(f"- Tiêu đề có dạng: \"... (Part {n} of {N})\". Mô tả có link tập trước và danh sách phát của series.")
    if n < N:
        L.append("- Kết tập bằng một câu hỏi hoặc tình huống chưa giải quyết, dẫn sang tập sau. Không khép tuyến chính.")
        L.append(f"- Còn {N - n} tập sau tập này. Không giải quyết sớm những tuyến dành cho tập cuối.")
    else:
        L.append("- ĐÂY LÀ TẬP CUỐI: khép MỌI tuyến đang mở ở trên, nói rõ \"This is the final part of ...\".")
        L.append("- Cuối tập giới thiệu câu chuyện mới (series hoặc video kế tiếp) để giữ người xem.")
        L.append(f"- Sau khi đăng: python series.py end {s['id']} --next \"<câu chuyện kế tiếp>\"")
    L.append(f"- Viết xong: python series.py episode {s['id']} {n} --status approved --summary \"...\" --cliffhanger \"...\" "
             "--open \"tuyến mới|...\" --close TH1,...")
    return "\n".join(L)


def main():
    utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("new")
    p.add_argument("id")
    p.add_argument("--title", required=True)
    p.add_argument("--pillar", required=True)
    p.add_argument("--episodes", type=int, required=True)
    p.add_argument("--premise", required=True)
    p.add_argument("--arc", required=True, help="mạch từng tập, cách nhau bằng |")
    p.add_argument("--playlist", default="")
    p = sp.add_parser("brief")
    p.add_argument("id")
    p.add_argument("--episode", type=int)
    p.add_argument("--out")
    p = sp.add_parser("episode")
    p.add_argument("id")
    p.add_argument("n", type=int)
    for k in ("title", "video_dir", "summary", "cliffhanger", "open", "close", "youtube_id", "date"):
        p.add_argument("--" + k.replace("_", "-"), dest=k)
    p.add_argument("--status", choices=EP_STATUS)
    p = sp.add_parser("fact")
    p.add_argument("id")
    p.add_argument("text")
    p.add_argument("--source", required=True)
    p.add_argument("--ep", type=int)
    p = sp.add_parser("extend")
    p.add_argument("id")
    p.add_argument("--to", type=int, required=True)
    p.add_argument("--reason", required=True)
    p = sp.add_parser("end")
    p.add_argument("id")
    p.add_argument("--next", required=True)
    p.add_argument("--force-note", default="")
    p = sp.add_parser("cancel")
    p.add_argument("id")
    p.add_argument("--reason", required=True)
    sp.add_parser("status")
    sp.add_parser("render")
    x = ap.parse_args()

    if x.cmd == "status":
        render_index()
        print((DIR / "SERIES_INDEX.md").read_text(encoding="utf-8"))
        return
    if x.cmd == "render":
        for s in all_series():
            if s:
                render_one(s)
        render_index()
        print("Đã sinh lại SERIES.md và SERIES_INDEX.md")
        return
    if x.cmd == "new":
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,40}", x.id):
            sys.exit("ID series: chữ thường, số, gạch nối (ví dụ deep-jungle)")
        if path(x.id).exists():
            sys.exit("Series đã tồn tại")
        arc = [a.strip() for a in x.arc.split("|") if a.strip()]
        if not 2 <= x.episodes <= 6:
            sys.exit("Series ICYFOX dài 2–6 tập (xem series-playbook.md)")
        if len(arc) != x.episodes:
            sys.exit(f"--arc phải có đúng {x.episodes} mục (mỗi tập một mục), đang có {len(arc)}")
        s = {"id": x.id, "title": x.title, "pillar": x.pillar, "status": "planned", "planned_episodes": x.episodes,
             "premise": x.premise, "arc": arc, "playlist_title": x.playlist or x.title, "created": today(),
             "episodes": [{"n": i + 1, "status": "planned"} for i in range(x.episodes)],
             "threads": [], "facts": [], "log": []}
        log(s, f"tạo series {x.episodes} tập")
        save(s)
        print(f"Đã tạo series {x.id}: kết thúc ở tập {x.episodes}. File: {rel(path(x.id))}")
        return

    s = load(x.id)
    if x.cmd == "brief":
        b = brief(s, x.episode)
        if x.out:
            Path(x.out).write_text(b + "\n", encoding="utf-8")
            print("Đã ghi", x.out)
        print(b)
        return
    if x.cmd in ("episode", "fact", "extend") and s["status"] in ("ended", "cancelled"):
        sys.exit(f"Series {S_LABEL[s['status']]}: không sửa thêm. Bắt đầu câu chuyện mới bằng `series.py new`.")
    if x.cmd == "episode":
        N = s["planned_episodes"]
        if x.n < 1 or x.n > N:
            sys.exit(f"Series dự kiến kết thúc ở tập {N}. Muốn thêm tập phải có số liệu và anh đồng ý: series.py extend")
        e = ep(s, x.n)
        for k in ("title", "video_dir", "summary", "cliffhanger", "youtube_id", "date"):
            if getattr(x, k):
                e[k] = getattr(x, k)
        if x.status:
            if x.status == "published" and x.n > 1 and ep(s, x.n - 1)["status"] != "published":
                sys.exit(f"Tập {x.n - 1} chưa đăng: phải đăng theo thứ tự")
            if x.status in ("approved", "rendered", "published") and not (e.get("summary") and (e.get("cliffhanger") or x.n == N)):
                sys.exit("Phải có --summary và --cliffhanger (trừ tập cuối) trước khi đánh dấu duyệt/dựng/đăng")
            e["status"] = x.status
            if s["status"] == "planned":
                s["status"] = "running"
        if x.open:
            for txt in [t.strip() for t in x.open.split("|") if t.strip()]:
                tid = f"TH{len(s['threads']) + 1}"
                s["threads"].append({"id": tid, "text": txt, "opened_in": x.n, "closed_in": None})
                print(f"  mở tuyến {tid}: {txt}")
        if x.close:
            for tid in [t.strip().upper() for t in x.close.split(",") if t.strip()]:
                th = next((t for t in s["threads"] if t["id"] == tid), None)
                if not th:
                    sys.exit(f"Không có tuyến {tid}")
                th["closed_in"] = x.n
        log(s, f"tập {x.n}: " + ", ".join(f"{k}" for k in ("status", "summary", "cliffhanger", "open", "close") if getattr(x, k)))
        save(s)
        print(f"Đã cập nhật tập {x.n}/{N} ({EP_LABEL[e['status']]})")
        if x.n == N and e["status"] == "published":
            left = open_threads(s)
            print("TẬP CUỐI ĐÃ ĐĂNG. " + (f"Còn {len(left)} tuyến mở: khép chúng rồi chạy end." if left
                                         else f"Chạy ngay: python series.py end {s['id']} --next \"...\""))
        return
    if x.cmd == "fact":
        s.setdefault("facts", []).append({"text": x.text, "source": x.source, "ep": x.ep})
        log(s, "thêm dữ kiện")
        save(s)
        print("Đã ghi dữ kiện")
        return
    if x.cmd == "extend":
        if not re.search(r"\d", x.reason):
            sys.exit("Lý do kéo dài phải dẫn số liệu (ví dụ: tập 1 giữ chân 52%, gấp 1,8 lần trung vị kênh)")
        if x.to <= s["planned_episodes"] or x.to > 6:
            sys.exit("Chỉ được kéo dài lên tối đa 6 tập, và phải lớn hơn số tập hiện tại")
        for i in range(s["planned_episodes"] + 1, x.to + 1):
            s["episodes"].append({"n": i, "status": "planned"})
            s["arc"].append("(bổ sung khi kéo dài: ghi mạch tập này)")
        log(s, f"kéo dài {s['planned_episodes']} -> {x.to} tập. Lý do: {x.reason}")
        s["planned_episodes"] = x.to
        save(s)
        print(f"Đã kéo dài tới tập {x.to}. Ghi mạch cho các tập mới trong series.json (mục arc) rồi chạy render.")
        return
    if x.cmd == "end":
        missing = [e["n"] for e in s["episodes"] if e["status"] != "published"]
        left = open_threads(s)
        if missing and not x.force_note:
            sys.exit(f"Chưa đăng các tập {missing}. Không kết thúc được.")
        if left and not x.force_note:
            sys.exit("Còn tuyến mở: " + "; ".join(f"{t['id']} {t['text']}" for t in left)
                     + ". Khép bằng `episode ... --close` hoặc dùng --force-note \"lý do\".")
        s["status"], s["ended"], s["next_story"] = "ended", today(), x.next
        log(s, "KẾT THÚC series" + (f" (ghi chú: {x.force_note})" if x.force_note else "") + f". Tiếp theo: {x.next}")
        save(s)
        print(f"Series {s['id']} ĐÃ KẾT THÚC. Câu chuyện kế tiếp: {x.next}")
        return
    if x.cmd == "cancel":
        s["status"] = "cancelled"
        log(s, f"hủy: {x.reason}")
        save(s)
        print("Đã hủy series")


if __name__ == "__main__":
    main()
