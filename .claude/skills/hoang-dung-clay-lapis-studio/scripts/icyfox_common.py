"""Hàm dùng chung cho các script của skill ICYFOX. Không bao giờ in khóa hay token."""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

VN = timezone(timedelta(hours=7))


def utf8():
    """Console Windows (gbk/cp1252) làm hỏng tiếng Việt: ép UTF-8."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def repo_root():
    here = Path(__file__).resolve()
    for p in [Path.cwd()] + list(here.parents):
        if (p / "AGENT_GUIDE.md").exists() and (p / "channel-studio").is_dir():
            return p
    for p in here.parents:
        if (p / "AGENT_GUIDE.md").exists():
            return p
    return Path.cwd()


ROOT = repo_root()
# Kênh thứ hai: đặt YT_CHANNEL=US cho từng lệnh (không ghi vào .env) → khóa YT_US_*, dữ liệu channel-studio-us/
CHANNEL = os.environ.get("YT_CHANNEL", "").strip().upper()
CS = ROOT / (f"channel-studio-{CHANNEL.lower()}" if CHANNEL else "channel-studio")
SKILL = ROOT / ".claude" / "skills" / "hoang-dung-clay-lapis-studio"


def now_vn():
    return datetime.now(VN)


def today():
    return now_vn().strftime("%Y-%m-%d")


def rel(p):
    try:
        return str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def load_env():
    """Máy local: đọc OpenMontage/.env. Không ghi đè biến đã có. Không in giá trị."""
    for f in [Path.cwd() / ".env", ROOT / ".env"]:
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and v and not os.environ.get(k):
                    os.environ[k] = v
            return str(f)
    return None


def yt_vars():
    """Tên 3 biến OAuth của kênh đang chọn: mặc định YT_*, YT_CHANNEL=US → YT_US_*."""
    p = f"YT_{CHANNEL}_" if CHANNEL else "YT_"
    return [p + "CLIENT_ID", p + "CLIENT_SECRET", p + "REFRESH_TOKEN"]


def yt_headers():
    """Đổi refresh token của kênh đang chọn lấy access token. Trả về (headers, scopes)."""
    import requests
    load_env()
    need = yt_vars()
    if any(not os.environ.get(k) for k in need):
        sys.exit(f"Thiếu {' / '.join(need)} (xem channel-studio/config/HUONG_DAN_KHOA_API.md)")
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ[need[0]], "client_secret": os.environ[need[1]],
        "refresh_token": os.environ[need[2]], "grant_type": "refresh_token"}, timeout=30)
    if not r.ok:
        sys.exit(f"Lỗi đổi token YouTube: {r.status_code} {r.text[:200]}")
    j = r.json()
    return {"Authorization": "Bearer " + j["access_token"]}, j.get("scope", "")


def api(h, url, params, fatal=True):
    """GET có xử lý lỗi. Trả về (ok, json | thông báo lỗi)."""
    import requests
    r = requests.get(url, headers=h, params=params, timeout=60)
    if r.ok:
        return True, r.json()
    try:
        msg = r.json().get("error", {}).get("message", r.text)
    except ValueError:
        msg = r.text
    msg = f"{r.status_code} {msg[:300]}"
    if fatal:
        sys.exit(f"LỖI API {url.rsplit('/', 1)[-1]}: {msg}")
    return False, msg


def iso_dur(s):
    import re
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, hh, mm, ss = (int(x or 0) for x in m.groups()) if m else (0, 0, 0, 0)
    return d * 86400 + hh * 3600 + mm * 60 + ss


def pulse_block(path):
    """Lấy đoạn giữa <!-- pulse:start --> và <!-- pulse:end --> của MISSION.md / PLAN.md."""
    try:
        t = Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""
    a, b = t.find("<!-- pulse:start -->"), t.find("<!-- pulse:end -->")
    return t[a + len("<!-- pulse:start -->"):b].strip() if a >= 0 and b > a else ""


def data_block(path, name):
    """Lấy các dòng 'a|b|c' trong khối <!-- name ... --> (ví dụ phases, releases của PLAN.md)."""
    try:
        t = Path(path).read_text(encoding="utf-8")
    except OSError:
        return []
    a = t.find(f"<!-- {name}")
    if a < 0:
        return []
    b = t.find("-->", a)
    rows = []
    for line in t[a + len(name) + 5:b].splitlines():
        line = line.strip()
        if line and "|" in line and not line.startswith("#"):
            rows.append([c.strip() for c in line.split("|")])
    return rows
