# Usage (from OpenMontage root): python voice_samples.py <section_id> <out_dir> <voice> [<voice> ...]
# shortcut: calls Gemini v1beta generateContent directly because tools/audio/gemini_tts.py 404s (card T-002, Codex); switch to the tool once T-002 is done.
import base64, json, os, sys, wave
from pathlib import Path
import requests
sys.path.insert(0, ".claude/skills/hoang-dung-clay-lapis-studio/scripts")
import check_apis as c
c.load_dotenv_local()

MODEL = "gemini-3.8-flash-tts"
DIRECTION = ("Read the following as the narrator of a calm, serious true-story documentary for an American audience. "
             "Low, steady and restrained, never theatrical. Slow down and soften almost to a whisper on the quoted diary lines. "
             "Take a real breath at each '...', and a long silence before the final sentence.\n\n")

sec_id, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
script = json.loads(Path("projects/lady-be-good/artifacts/script.json").read_text(encoding="utf-8"))
text = next(s["text"] for s in script["sections"] if s["id"] == sec_id)
text = text.replace("[long pause]", "... ...").replace("[pause]", "...")
headers = c.key_header("GEMINI_API_KEY", "x-goog-api-key") or c.key_header("GOOGLE_API_KEY", "x-goog-api-key")
(out / "prompt.txt").write_text(f"model: {MODEL}\nsection: {sec_id}\n\n{DIRECTION}{text}\n", encoding="utf-8")
for voice in sys.argv[3:]:
    body = {"contents": [{"parts": [{"text": DIRECTION + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                      headers=headers, json=body, timeout=180)
    if not r.ok:
        print(voice, "LỖI", r.status_code, r.text[:200]); continue
    part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm = base64.b64decode(part["data"])
    rate = int(part["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in part["mimeType"] else 24000
    p = out / f"{sec_id}_{voice}.wav"
    if part["mimeType"] == "audio/wav":  # already a full WAV file
        p.write_bytes(pcm)
    else:  # raw PCM (audio/L16)
        with wave.open(str(p), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    with wave.open(str(p)) as w: print(voice, "OK", p, f"{w.getnframes()/w.getframerate():.1f}s", w.getframerate(), "Hz")
