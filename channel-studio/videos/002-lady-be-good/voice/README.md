# Mẫu giọng 002 · **anh chốt Algenib** (22/11/2026)

Đoạn thử: S5.5 "Những trang cuối" (trích nhật ký, đọc gần như thì thầm, có chỗ ngừng dài).
Model: `gemini-3.8-flash-tts`, gọi thẳng API `v1beta` `generateContent` bằng `voice_samples.py`, vì `tools/audio/gemini_tts.py` còn lỗi 404 (thẻ T-002, Codex).
Lời dẫn giọng và văn bản gửi đi: `prompt_S5.5.txt`.
File âm thanh ở `projects/lady-be-good/assets/audio/voice_samples/` (không đưa lên git).

| Giọng | Độ dài | Âm lượng | Đỉnh | Số chỗ ngừng > 0,5 s | Chỗ ngừng dài nhất |
|---|---|---|---|---|---|
| Charon | 56,5 s | −20,7 LUFS | −1,4 dBFS | 18 | 2,1 s |
| Algenib | 57,8 s | −22,0 LUFS | −2,5 dBFS | 18 | 1,4 s |
| Gacrux | 59,2 s | −20,4 LUFS | −1,4 dBFS | 13 | 1,1 s |

Đo bằng ffmpeg `ebur128` và `silencedetect` (−40 dB).

## Lưu ý
- **Lỗi ở 3 mẫu đầu (đã sửa 22/11):** câu chỉ dẫn giọng bị đọc to ở đầu mỗi mẫu, nên mẫu dài 56–59 s. Nhận định "đọc chậm hơn 30%" trước đó là **sai**. Đã chuyển sang cấu trúc `DIRECTOR'S NOTES / TRANSCRIPT` trong `narrate.py` (đưa chỉ dẫn vào systemInstruction thì model báo lỗi 400).
- Mẫu Algenib bản 2 (`voice_samples/v2/S5.5.wav`): 37,2 s, kịch bản tính 44 s. Whisper khớp 94,7%, lệch 4 chỗ: "Be Good" thành "begood", "twelfth" thành "12th" (khác cách ghi), "writing" thành "riding", "dated" thành "stated" (cần nghe lại, có thể do máy nghe nhầm giọng khàn).
- Lời đọc cả video: `narrate.py` → `projects/lady-be-good/assets/audio/narration/<id>.wav`; báo cáo kiểm ở `narration_report.md`.
- Giọng được chọn giữ cố định giọng và model. Đổi giọng hay model thì phải làm mẫu và duyệt lại.
