# Usage (from OpenMontage root): python alt_voice.py <out_dir> <engine> <voice> [section_id ...]
#   engine: gemini:<model>  (e.g. gemini:gemini-3.1-flash-tts-preview)  or  openai:<model>  (e.g. openai:gpt-4o-mini-tts)
# Fallback when gemini-3.8-flash-tts hits its free-tier daily cap (10 requests/day/model, 22/11/2026).
import base64, json, os, sys, time, wave
from pathlib import Path
import requests
sys.path.insert(0, ".claude/skills/hoang-dung-clay-lapis-studio/scripts")
import check_apis as c
c.load_dotenv_local()

STYLE = ("Calm, serious true-story documentary narrator for an American audience. Low, steady, restrained, never theatrical. "
         "Soften on quoted diary lines. Measured pace: a short breath at each '...', a longer silence at '... ...'.")
DIRECTION = f"# AUDIO PROFILE: documentary narrator\n### DIRECTOR'S NOTES\n{STYLE}\nSpeak only the transcript below, word for word.\n\n#### TRANSCRIPT\n"

out, (provider, model), voice, ids = Path(sys.argv[1]), sys.argv[2].split(":", 1), sys.argv[3], sys.argv[4:]
out.mkdir(parents=True, exist_ok=True)
secs = json.loads(Path("projects/lady-be-good/artifacts/script.json").read_text(encoding="utf-8"))["sections"]


def gemini(text):
    body = {"contents": [{"parts": [{"text": DIRECTION + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                      headers=c.key_header("GEMINI_API_KEY", "x-goog-api-key"), json=body, timeout=300)
    if not r.ok:
        return None, f"{r.status_code} {'PerDay ' if 'PerDay' in r.text else ''}{r.text[:160]}"  # PerDay sits past the cut
    part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
    data = base64.b64decode(part["data"])
    if part["mimeType"] == "audio/wav":
        return data, None
    rate = int(part["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in part["mimeType"] else 24000
    return ("pcm", rate, data), None


def openai(text):
    r = requests.post("https://api.openai.com/v1/audio/speech",
                      headers={"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}"},
                      json={"model": model, "voice": voice, "input": text, "instructions": STYLE, "response_format": "wav"},
                      timeout=300)
    return (r.content, None) if r.ok else (None, f"{r.status_code} {r.text[:160]}")


for s in secs:
    if ids and s["id"] not in ids:
        continue
    p = out / f"{s['id']}.wav"
    if p.exists() and not ids:
        continue
    text = s["text"].replace("[long pause]", "... ...").replace("[pause]", "...")
    for attempt in range(5):  # per-minute 429 (22/11: S3.3 failed after 60s of waiting, OK again a few minutes later)
        data, err = (gemini if provider == "gemini" else openai)(text)
        if data or not err.startswith(("429", "500", "503")) or "PerDay" in err:
            break
        time.sleep(60 * (attempt + 1))
    if not data:
        print(s["id"], "LỖI", err, flush=True)
        if "PerDay" in err:
            print("DỪNG: hết hạn mức ngày (fallbacks.md F1), chạy lại cùng lệnh sau 15:00 giờ VN", flush=True)
            sys.exit(2)
        continue
    if isinstance(data, tuple):
        with wave.open(str(p), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(data[1]); w.writeframes(data[2])
    else:
        p.write_bytes(data)
    with wave.open(str(p)) as w:
        print(s["id"], "OK", f"{w.getnframes() / w.getframerate():.1f}s (kịch bản {s['end_seconds'] - s['start_seconds']}s)", flush=True)
