# Mẫu giọng 002 · chờ anh chọn (22/11/2026)

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
- **Đọc chậm hơn dự tính:** kịch bản tính 44 s cho đoạn này (125 từ/phút), giọng thật đọc 56–59 s, chậm hơn khoảng 30%. Nếu giữ nhịp này, cả video sẽ dài khoảng 35 phút thay vì 27:29. Sau khi anh chọn giọng, tôi sẽ thử bớt dấu "..." để nhịp nhanh hơn.
- **Chưa kiểm bằng máy nghe chép lời** (đọc thiếu hay thừa chữ so với kịch bản). Lần chạy whisper bị dừng vì máy đang quá tải CPU.
- Giọng nào được chọn sẽ giữ cố định cả giọng và model. Đổi giọng hay model thì phải làm mẫu và duyệt lại.
