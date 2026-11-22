# Usage (from OpenMontage root): python narrate.py <out_dir> <voice> [section_id ...]   (no ids = all sections)
# shortcut: calls Gemini v1beta generateContent directly because tools/audio/gemini_tts.py 404s (card T-002, Codex); switch to the tool once T-002 is done.
# Direction uses the DIRECTOR'S NOTES / TRANSCRIPT layout: plain prefixed text was read aloud, and systemInstruction is rejected (400) for this model (22/11/2026).
import base64, json, sys, time, wave
from pathlib import Path
import requests
sys.path.insert(0, ".claude/skills/hoang-dung-clay-lapis-studio/scripts")
import check_apis as c
c.load_dotenv_local()

MODEL = "gemini-3.8-flash-tts"
DIRECTION = ("# AUDIO PROFILE: documentary narrator\n"
             "### DIRECTOR'S NOTES\n"
             "Style: calm, serious true-story documentary for an American audience. Low, steady, restrained, never theatrical. Soften on quoted diary lines.\n"
             "Pacing: measured. A short breath at each '...', a longer silence at '... ...'.\n"
             "Speak only the transcript below, word for word.\n\n"
             "#### TRANSCRIPT\n")

out, voice, ids = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
out.mkdir(parents=True, exist_ok=True)
secs = json.loads(Path("projects/lady-be-good/artifacts/script.json").read_text(encoding="utf-8"))["sections"]
headers = c.key_header("GEMINI_API_KEY", "x-goog-api-key") or c.key_header("GOOGLE_API_KEY", "x-goog-api-key")
for s in secs:
    if ids and s["id"] not in ids:
        continue
    p = out / f"{s['id']}.wav"
    if p.exists() and not ids:  # resume a full run
        continue
    text = s["text"].replace("[long pause]", "... ...").replace("[pause]", "...")
    body = {"contents": [{"parts": [{"text": DIRECTION + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for attempt in range(4):
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                          headers=headers, json=body, timeout=300)
        if r.ok or r.status_code not in (429, 500, 503):
            break
        if r.status_code == 429 and "PerDay" in r.text:  # free tier = 10 requests/day/model; retrying only burns time
            print(s["id"], "DỪNG: hết hạn mức ngày của Gemini (gói miễn phí 10 lượt/ngày), chạy lại sau khi hạn mức đặt lại", flush=True)
            sys.exit(2)
        time.sleep(20 * (attempt + 1))
    if not r.ok:
        print(s["id"], "LỖI", r.status_code, r.text[:200], flush=True); continue
    part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
    data = base64.b64decode(part["data"])
    if part["mimeType"] == "audio/wav":  # already a full WAV file
        p.write_bytes(data)
    else:  # raw PCM (audio/L16;rate=N)
        rate = int(part["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in part["mimeType"] else 24000
        with wave.open(str(p), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(data)
    with wave.open(str(p)) as w:
        print(s["id"], "OK", f"{w.getnframes() / w.getframerate():.1f}s (kịch bản {s['end_seconds'] - s['start_seconds']}s)", flush=True)
