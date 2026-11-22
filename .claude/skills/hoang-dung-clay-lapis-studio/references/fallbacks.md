# Giám sát tác vụ và phương án thay thế

Anh Dũng yêu cầu ngày 22/11/2026: "tự động giám sát tác vụ, bắt lỗi và tìm phương pháp thay thế". Lý do: lời đọc 002 lặp lỗi 429 gần 30 phút mà không ai biết.

## 1. Giám sát chạy thế nào

| Việc | Cách làm |
|---|---|
| Ghi log tác vụ nền | Mọi tác vụ chạy lâu (lời đọc, render, quét, whisper) ghi log vào `channel-studio/state/jobs/<YYYY-MM-DD>-<việc>.log`, ví dụ `... 2>&1 \| tee channel-studio/state/jobs/2026-11-23-voice-002.log` |
| Theo dõi khi đang chạy | Trong phiên: dùng công cụ Monitor bắt dòng `LỖI`, `Traceback`, `Error` và dòng báo xong. Không ngồi chờ, không lặp `sleep` |
| Soát định kỳ | `python scripts/watchdog.py`: thẻ "đang làm" quá 6 giờ không cập nhật (nghi treo), thẻ quá hạn, thẻ bị chặn, lỗi ở đuôi log. Mã thoát 1 = có việc GẤP |
| Gắn vào tự lái | `autopilot.py` gọi `watchdog.scan()` và đưa kết quả lên đầu chương trình làm việc. Phiên 09:00 và 17:00 xử lý mục "Giám sát" trước mọi việc khác |
| Soát log ngoài | `python scripts/watchdog.py <đường dẫn log>` cho log nằm ngoài `state/jobs/` |

## 2. Gặp lỗi thì làm gì

1. **Dừng ngay** nếu là lỗi không tự hết (hạn mức ngày, hết tiền, sai khóa). Không thử lại vô ích.
2. Tra mã lỗi ở bảng dưới, làm theo cột "Phương án thay thế".
3. Trong lúc chờ: làm việc khác không phụ thuộc (phân cảnh, tìm ảnh có giấy phép, kịch bản Shorts, gói đăng, radar).
4. Ghi vào thẻ việc (`tasks.py`): lỗi gì, đã thử gì, khi nào chạy lại. Hết đường thì chuyển thẻ sang `blocked` kèm lý do.
5. Lỗi mới chưa có trong bảng (F0): đọc log, tìm nguyên nhân gốc, sửa, rồi **thêm một dòng vào bảng này**.

## 3. Bảng phương án thay thế

Phương án thay thế **không được** phá việc anh đã chốt (giọng Algenib, model `gemini-3.1-flash-tts-preview`, một model cho một video) hay luật cứng (`policy-guardrails.md`).

| Mã | Lỗi | Dấu hiệu trong log | Phương án thay thế | Không được làm |
|---|---|---|---|---|
| F1 | Gemini hết hạn mức ngày | `429` + `PerDay` | Dừng. Chạy lại cùng lệnh sau 15:00 giờ VN (hạn mức đặt lại; file đã có được bỏ qua). Trong lúc chờ làm bước khác của video. Nếu lời đọc làm trễ lịch đăng: báo anh lựa chọn bật trả phí Gemini (việc chi tiền là của anh) | Đổi giọng hay model giữa chừng một video; lách bằng nhiều tài khoản hoặc nhiều project |
| F2 | `tools/audio/gemini_tts.py` lỗi 404 | `404` khi gọi `gemini_tts` | Gọi thẳng API v1beta bằng `voice/alt_voice.py` | Sửa `gemini_tts.py` (thẻ T-002 của Codex) |
| F3 | YouTube Data API hết hạn mức | `quotaExceeded`, `dailyLimitExceeded` | Chờ hạn mức đặt lại (15:00 giờ VN); việc gấp thì dùng yt-dlp và ghi rõ "API hết hạn mức" trong báo cáo | Tạo thêm project để lấy hạn mức |
| F4 | yt-dlp bị chặn | `HTTP Error 429`, `Sign in to confirm` | Thử lại sau 24 giờ; dùng YouTube Data API nếu còn hạn mức | Dùng proxy |
| F5 | Không đọc được doanh thu | `401` ở YouTube Analytics (chỉ số tiền) | Ghi "chưa đọc được doanh thu (401)" trong báo cáo Chủ nhật. Sau khi bật kiếm tiền (YPP), nhờ anh cấp lại quyền `yt-analytics-monetary` | Bịa số |
| F6 | Whisper/PyAV không đọc được file | `InvalidDataError`, `av.error` | Giải mã bằng ffmpeg ra WAV 16 kHz mono rồi chạy lại whisper | Bỏ qua bước kiểm lời đọc |
| F7 | HyperFrames render lỗi | lỗi từ `hyperframes`, `lint` báo lỗi | Chạy `npx hyperframes lint` và `check`, sửa theo báo lỗi; vẫn hỏng thì dựng bằng Remotion | Giao video chưa qua `check` |
| F8 | Máy quá tải | `MemoryError`, `out of memory` | Chạy lại ở mức ưu tiên Idle, giảm luồng (whisper 2 luồng), render từng đoạn | Tắt tiến trình của phiên khác khi anh chưa cho phép |
| F9 | Push GitHub lỗi | `lỗi push`, `rejected` | `session_end.py` tự thử lại 4 lần; commit vẫn nằm trên máy. Báo `rejected (fetch first)` = phiên khác vừa đẩy: xem `git log HEAD..FETCH_HEAD`, rồi `git fetch origin ccr-6640cec8-2anthl && git merge --no-edit FETCH_HEAD`. Xung đột thì nhật ký và decisions-log giữ cả hai bên, `tasks.json` gộp theo mã thẻ (bản `updated` mới hơn thắng), `TASKS.md` sinh lại bằng `tasks.py render`; rồi chạy lại `session_end.py` (đã gặp 22/11 23:59) | `git push --force` |
| F10 | Bị giới hạn tốc độ (429 theo phút, không có `PerDay`) | `429`, `RESOURCE_EXHAUSTED` không kèm `PerDay` | Không phải hết lượt ngày (22/11: S3.3 của 002 lỗi 429, vài phút sau gọi lại được 200). Chờ 2–5 phút rồi chạy lại cùng lệnh; script tự giãn cách 60/120/180 giây. Lỗi lặp quá 3 lần liền thì gọi thử 1 câu ngắn để đọc `quotaId` | Coi nhầm là hết lượt ngày rồi bỏ cả ngày |
| F0 | Lỗi chưa có trong bảng | `Traceback`, `LỖI`, `Error` | Đọc log, tìm nguyên nhân gốc, sửa; ghi thêm dòng mới vào bảng này | Thử lại mù quáng nhiều lần |

Mẫu lỗi máy dò nằm trong `scripts/watchdog.py` (biến `SIGNATURES`). Thêm dòng ở đây thì thêm mẫu ở đó.
