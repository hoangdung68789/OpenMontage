# Hợp đồng làm việc của AI cho kênh ICYFOX

Áp dụng cho **mọi** AI làm việc cho kênh (Claude trên cloud, Claude trên máy anh, Codex, phiên chạy theo lịch). Đọc lại **mỗi khi nhận một việc mới**. Hook của Claude Code nhắc bản tóm tắt ở mỗi lượt.

Vì sao có file này: ngày 22/11/2026 anh phản ánh các phiên khác "chỉ đúng khoảng 30%". Có khóa API YouTube nhưng không dùng, làm nửa vời, kết thúc bằng câu hỏi, không lưu kết quả. Mỗi luật dưới đây chặn một lỗi đã xảy ra thật.

## 1. Chu trình 6 bước cho mỗi việc
| # | Bước | Làm gì | Dấu hiệu đã làm |
|---|---|---|---|
| 1 | **Nhắc mục tiêu** | Đọc `channel-studio/MISSION.md` (hook đã in phần tóm tắt) và `PLAN.md`. Tự hỏi: việc này phục vụ mục tiêu nào, có trái kế hoạch không | Nêu được việc này phục vụ chỉ số nào |
| 2 | **Đọc đúng file** | Tra `read-map.md` theo loại việc. Đọc đủ các file "bắt buộc", đúng thứ tự | Câu trả lời có dòng "Đã đọc: …" |
| 3 | **Lập thẻ việc** | `tasks.py add "…" --type … --dod "…" --start`. Nếu đã có thẻ thì `tasks.py start <id>`. Việc lớn tách thành nhiều thẻ | Thẻ ở trạng thái "Đang làm", có mục "xong khi" kiểm được |
| 4 | **Làm thật** | Dùng công cụ và API thật (Data API, Analytics API, Gemini, OpenMontage, HyperFrames). Không mô phỏng, không "giả sử", không đưa kế hoạch làm sản phẩm thay cho sản phẩm | Có file sản phẩm thật trong repo |
| 5 | **Kiểm chứng** | Chạy kiểm tra thật (mục 3), rồi `tasks.py done` kèm báo cáo từng thành phần | `tasks.py done` in "Đã ghi nhật ký" |
| 6 | **Giao và lưu** | Trả lời anh theo khung KẾT LUẬN / CHI TIẾT / DẪN CHỨNG / BƯỚC TIẾP THEO, có bảng thành phần (mục 3.3). Chạy `session_end.py` | Có commit trên nhánh `ccr-6640cec8-2anthl` |

## 2. Luật chống làm nửa vời
1. **Không dừng giữa chừng.** Chỉ có 3 trạng thái được phép dừng:
   - **Xong:** `tasks.py done` đã chấp nhận.
   - **Chờ anh:** `tasks.py wait <id> --question "…"`. Chỉ dùng cho việc thuộc danh sách "việc quan trọng" (`autopilot.md` §4).
   - **Bị chặn:** `tasks.py block <id> --reason "<thông báo lỗi nguyên văn>" --tried "cách 1; cách 2"`. Bắt buộc đã thử ít nhất 2 cách.
   Hook Stop chặn lượt trả lời 1 lần nếu còn thẻ "đang làm" của phiên, hoặc còn thay đổi chưa lưu.
2. **Gặp lỗi thì tự xử lý trước.** Tra bảng "Đường dự phòng" trong `read-map.md` và bảng sự cố trong `environment-and-apis.md`. Báo lỗi cho anh phải kèm thông báo lỗi nguyên văn (che khóa) và các cách đã thử.
3. **Không thu hẹp yêu cầu.** Anh xin 3 thứ thì giao đủ 3 thứ. Không tự đổi đề, không kéo anh về chủ đề cũ.
4. **Không hỏi lại điều đã chốt.** Trước khi hỏi, tra `MISSION.md`, `PLAN.md`, `HANDOFF.md`, `decisions-log.md`. Còn điểm chưa rõ mà không quan trọng: tự chọn phương án mặc định hợp lý, ghi rõ đã chọn gì, rồi làm tiếp.
5. **Không bịa.** Số liệu, tên kênh, link, nguồn, ngày tháng đều phải từ công cụ hoặc nguồn thật. Không có thì ghi [Chưa xác minh].
6. **Việc dài thì chia thẻ và làm lần lượt đến hết** trong cùng lượt, hoặc đến khi chạm một trong 3 trạng thái dừng. Không dừng chỉ vì việc dài.
7. **Ngữ cảnh bị nén** (hook báo "Ngữ cảnh vừa được nén"): đọc lại `TASKS.md` và thẻ đang làm trước khi tiếp tục. Không làm lại việc đã xong.

## 3. QUY TẮC HOÀN THÀNH (anh yêu cầu 22/11/2026)
### 3.1 Khi nào được nói "xong"
Chỉ được nói "xong", "hoàn thành", "đã làm" khi **cả 4 điều sau đều đúng**:
1. **Sản phẩm có thật:** file nằm trong repo hoặc đường dẫn kiểm được, không rỗng. Nếu là thao tác trên YouTube, Notion hay Drive: kết quả đọc lại được qua API.
2. **Đã kiểm chứng thật:** đã chạy lệnh kiểm (test, `qa_check.py`, `npx hyperframes lint/check`, gọi lại API để đọc kết quả, mở file xem nội dung…). Không lấy việc "đã ra lệnh" làm bằng chứng cho "đã xong".
3. **`tasks.py done` đã chấp nhận.** Script tự kiểm theo loại việc (ví dụ kịch bản ≥ 400 từ và có ≥ 2 link nguồn, việc code phải có `--check` chạy đạt) và kiểm báo cáo từng thành phần. Không đạt thì thẻ giữ nguyên, script trả mã lỗi 2.
4. **Nhật ký lịch sử đã ghi.** `tasks.py done` tự ghi vào `channel-studio/logs/<năm-tháng>.md`, và mục đó được lưu git bằng `session_end.py`.

Thiếu một điều thì **chưa xong**. Báo đúng tình trạng: "Đã làm A và B (đã kiểm). C chưa xong vì …".

### 3.2 Báo cáo từng thành phần (bắt buộc khi `done`)
```bash
python .claude/skills/hoang-dung-clay-lapis-studio/scripts/tasks.py done T-012 \
  --evidence channel-studio/videos/002-lady-be-good/script_part1.md \
  --summary "Viết phần 1 kịch bản 002 (1.180 từ, 0:00–9:26), QA đạt" \
  --component "Lời thoại :: 1.180 từ, 14 đoạn, hook 60 giây :: qa_check.py ĐẠT, đếm từ tự động :: channel-studio/videos/002-lady-be-good/script_part1.md" \
  --component "Nguồn :: 9 nguồn, 12/14 đoạn có dòng Nguồn :: mở từng link, đối chiếu ngày và tên :: channel-studio/videos/002-lady-be-good/script_part1.md" \
  --component "Chống trùng đối thủ :: 0 cụm 8 từ trùng :: qa_check.py so với phụ đề trong research/ :: channel-studio/videos/002-lady-be-good/script_part1.qa.md" \
  --remaining "S1.6 chưa tìm được nguồn gốc, đã bỏ khỏi lời thoại"
```
Mỗi `--component` có 4 trường, ngăn bằng `::`:
- **Tên thành phần.**
- **Kết quả cụ thể:** có số liệu, không viết "ok" hay "tốt".
- **Cách đã kiểm chứng:** lệnh nào, mở file nào, gọi API nào.
- **Bằng chứng:** đường dẫn file (phải tồn tại) hoặc link.

Script từ chối nếu thiếu trường, viết chung chung, hoặc bằng chứng không tồn tại.

### 3.3 Báo cho anh
Câu trả lời cuối có bảng **Thành phần | Kết quả | Cách kiểm chứng | Bằng chứng**, giống mục trong nhật ký. Thành phần chưa xong ghi rõ "CHƯA XONG – lý do – việc tiếp theo".

### 3.4 Nhật ký lịch sử
- File: `channel-studio/logs/2026-11.md`, `2026-12.md`… Chỉ thêm, **không sửa, không xóa**.
- Ghi các sự kiện: HOÀN THÀNH (đầy đủ báo cáo), CHỜ ANH QUYẾT (câu hỏi), BỊ CHẶN (lỗi nguyên văn và các cách đã thử), BỎ (lý do).
- Xem nhanh: `python tasks.py log --n 5`.

### 3.5 Hook chống báo sai
Khi AI định dừng, hook Stop đọc câu trả lời cuối. Nếu câu đó có "đã xong / đã hoàn thành / đã hoàn tất…" mà 12 giờ qua không có thẻ nào được `done`, hook chặn 1 lần và yêu cầu: chạy `tasks.py done`, hoặc sửa câu trả lời cho đúng tình trạng.

## 4. Chống quên mục tiêu và kế hoạch (7 lớp)
| Lớp | Cơ chế | Tác dụng |
|---|---|---|
| 1 | `CLAUDE.md` và `AGENTS.md` ở gốc repo (luôn được nạp) | Trỏ tới MISSION và hợp đồng này |
| 2 | Hook SessionStart (khi mở, tiếp tục, xóa hoặc **nén ngữ cảnh**) | In MISSION, PLAN, hợp đồng, việc hôm nay, việc chờ anh |
| 3 | Hook UserPromptSubmit (mỗi lượt anh gửi) | Nhắc chu trình 6 bước, thẻ đang mở, việc GẤP theo kế hoạch |
| 4 | Hook Stop | Chặn dừng khi còn việc dở, chưa lưu, hoặc báo "xong" sai |
| 5 | `autopilot.py` | Đọc PLAN, sổ việc, series, số liệu, rồi tính việc trễ tiến độ theo ngày đăng |
| 6 | Sổ việc, series, nhật ký, HANDOFF trong git | Không mất khi đổi máy, đổi phiên hay đổi agent |
| 7 | `session_start.sh` (cloud không có hook) | In cùng nội dung với hook SessionStart |

**Lưu ý:** phiên cloud mở với nhiều repo có thư mục gốc là `/home/user`, không phải OpenMontage, nên hook trong `OpenMontage/.claude/settings.json` không chạy. Ở đó bắt buộc chạy `session_start.sh` trước tiên. Phiên trên máy anh (mở trong thư mục OpenMontage) có đủ hook.

## 5. Tự kiểm trước khi gửi câu trả lời
| Câu hỏi | Nếu "không" |
|---|---|
| Đã nhắc mục tiêu và đọc đủ file trong `read-map.md` chưa? | Đọc |
| Mỗi việc đều có thẻ chưa? Thẻ đều ở trạng thái xong, chờ anh, hoặc bị chặn chưa? | Làm tiếp |
| Mọi "xong" đều đã qua `tasks.py done` chưa? | Chạy, hoặc sửa câu chữ |
| Số liệu YouTube lấy từ API (Data hoặc Analytics) chưa? | Chạy script |
| Có bảng thành phần và nguồn kèm ngày tra chưa? | Bổ sung |
| Đã lưu git chưa? | `session_end.py` |
| Câu hỏi cho anh có thuộc danh sách "việc quan trọng" không? | Bỏ câu hỏi, tự quyết và ghi lại |
