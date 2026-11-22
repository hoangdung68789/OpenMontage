# Quy trình sản xuất một video

Pipeline của OpenMontage: `animated-explainer` (`pipeline_defs/animated-explainer.yaml`). Trước mỗi bước, đọc `skills/pipelines/explainer/<stage>-director.md` và `AGENT_GUIDE.md` (Rule Zero, các quy định khi trình bày quyết định). Mỗi checkpoint ghi bằng `lib/checkpoint.write_checkpoint`. Artifact phải hợp lệ theo schema trong `schemas/artifacts/`.

## Mục lục
1. Nghiên cứu · 2. Đề xuất · 3. Kịch bản · 4. Giọng · 5. Phân cảnh · 6. Tài nguyên · 7. Dựng · 8. Kiểm tra chất lượng · Nhận diện hình ảnh · Thumbnail

## 1. Nghiên cứu (research, không cần duyệt)
- Khoảng 10–20 lượt tra web, cộng 2–3 lượt tìm trên YouTube bằng yt-dlp (`ytsearch25:<chủ đề>`, chế độ flat) để xem các video đang có và lượt xem.
- Tìm cho bằng được **"khoảng trống"**: phát hiện mới (mảnh văn bản, khai quật, công bố khoa học từ 2010), những ngộ nhận phổ biến, những góc mà các video hơn 1 triệu view chưa kể.
- Đầu ra: `projects/<id>/artifacts/research_brief.json`. Kiểm tra bằng `jsonschema` trước khi ghi checkpoint `research`.

## 2. Đề xuất (proposal, cần duyệt)
- 3 concept thật sự khác nhau về cấu trúc và cách mở đầu.
- Trình bày **cả HyperFrames lẫn Remotion** (quy định bắt buộc), kèm đề xuất.
  - Mặc định của kênh là HyperFrames + cách dựng atelier.
  - Remotion cần chạy `npm install` trong `remotion-composer`.
- Cách dựng: atelier (đề xuất, vì có nhận diện riêng và tránh bị coi là rập khuôn) hoặc cảnh mẫu.
- Ghi chi phí giọng đọc. Gemini 3.8 Flash TTS: 25 token/giây âm thanh, 9 USD cho 1 triệu token đến 31/12/2026, 18 USD từ 01/01/2027.
- Khi anh duyệt: ghi `proposal_packet.json` và `decision_log.json` (mỗi lựa chọn ghi `option_id`, `label`, `score`, `reason`), checkpoint với `human_approved=True`.

## 3. Kịch bản (script, duyệt từng phần)
- **Thời lượng:** theo nội dung, không độn chữ. Gilgamesh đã chốt 35–40 phút. Nhịp đọc khoảng 125 từ/phút, ngừng 0,3–1,2 giây ở các điểm chuyển.
- **Chia phần:** 4 phần, mỗi phần 2–3 chương. Gửi duyệt từng phần.
- **Mỗi đoạn có:**
  - Lời tiếng Anh (dòng bắt đầu bằng `>`).
  - Ghi chú giọng: nhịp, chỗ nhấn, chỗ ngừng.
  - Ghi chú hình: 1 thay đổi mỗi 8–10 giây.
  - Bản dịch tiếng Việt.
  - Nguồn.

  Xem `templates/script_section_template.md`.
- **Chi tiết không kiểm được** thì đưa vào mục "Đã bỏ" hoặc "Cần kiểm". Không đọc giọng những chi tiết này.
- **Đoạn "dòng mới tìm lại"** là đặc trưng của kênh: kể chuyện ai tìm ra, năm nào, công bố ở đâu, kèm hiệu ứng dòng chữ hình nêm phát sáng màu lapis.
- **An toàn quảng cáo:** cảnh tình dục chỉ nói kín đáo, không hiện máu hay đầu lâu, chuyện bạo lực kể bằng hình ảnh tượng trưng.
- **Đếm từ và căn giờ:** dùng đoạn Python dưới đây (giả định 125 từ/phút, +0,9 giây cho mỗi `[pause]`, +1,2 giây cho tiêu đề chương):
  ```python
  import re
  t = open(p).read()
  for b in re.split(r'(?=### S\d\.\d · )', t)[1:]:
      txt = re.search(r'\n> (.+?)\n', b).group(1)
      w = len(txt.replace('[pause]', '').split())
  ```
- Khi đủ các phần: gộp thành `script.json` hợp lệ theo `schemas/artifacts/script.schema.json`, ghi checkpoint `script`.

## 4. Giọng
- **Giọng kênh đã chốt (22/11/2026): `gemini-3.8-flash-tts` (thay bằng 3.1-preview cùng ngày, xem dòng dưới), giọng Algenib**, cho mọi video dài và Shorts. Không làm mẫu giọng, không hỏi lại. Chỉ làm 3 mẫu khi anh yêu cầu đổi giọng.
- Công cụ: `channel-studio/videos/002-lady-be-good/voice/narrate.py <thư_mục_ra> Algenib [mã đoạn…]`. Script đọc `projects/<id>/artifacts/script.json`, ghi mỗi đoạn một file WAV, tự làm tiếp nếu chạy dở. Video khác thì đổi đường dẫn `script.json` trong script.
  - Gọi thẳng API `v1beta` `generateContent`, vì `tools/audio/gemini_tts.py` còn lỗi 404 (thẻ T-002). T-002 xong thì chuyển về công cụ.
  - **Bẫy đã gặp:** chỉ dẫn giọng ghép thẳng vào đầu văn bản sẽ bị đọc to. `systemInstruction` bị model từ chối (lỗi 400). Phải dùng bố cục `# AUDIO PROFILE / ### DIRECTOR'S NOTES / #### TRANSCRIPT`.
  - API trả về file WAV hoàn chỉnh (`audio/wav`). Không bọc thêm một lớp WAV nữa.
- Kiểm: `voice/check_voice.py` (whisper small.en, chạy ở mức ưu tiên Idle với 2 luồng CPU, so với kịch bản) và `voice/narration_report.py` (độ dài, LUFS, % khớp). Whisper ghi số bằng chữ số, nên đoạn nhiều số sẽ khớp thấp dù giọng đọc đúng.
- Nhịp đọc thật của Algenib: đoạn S5.5 đọc 37,2 giây, kịch bản ước tính 44 giây.
- Đọc dài: chia theo đoạn của kịch bản, mỗi lần gọi một đoạn, rồi ghép lại.

- **Hạn mức (đo 22/11/2026):** gói miễn phí chỉ có 10 lượt/ngày cho mỗi model TTS, đặt lại lúc 15:00 giờ VN. Một video 30 đoạn cần 3 ngày. `narrate.py` tự dừng khi hết lượt và tự bỏ qua đoạn đã có, nên chỉ cần chạy lại sau 15:00. Muốn nhanh hơn phải bật thanh toán (việc tài khoản của anh). Shorts dùng chung lượt.

- **Model giọng hiện hành (anh chốt 22/11/2026): `gemini-3.1-flash-tts-preview`, giọng Algenib.** Lệnh: `python channel-studio/videos/002-lady-be-good/voice/alt_voice.py <thư mục ra> gemini:gemini-3.1-flash-tts-preview Algenib [đoạn…]`. Mỗi model Gemini có hạn mức riêng; hết lượt thì `alt_voice.py` tự dừng. Một video chỉ dùng một model. Không dùng ElevenLabs gói free (không thương mại, 10.000 ký tự); OpenAI cần nạp tiền.

## 5. Phân cảnh (scene_plan, cần duyệt)
- Mỗi cảnh có: mốc giây (theo độ dài thật của file giọng), loại cảnh, mô tả, nguồn hình kèm giấy phép, chữ trên màn hình.
- Các loại cảnh:
  - Ảnh di vật thật, cho chuyển động chậm có chủ đích (parallax, đẩy máy).
  - Bản đồ Lưỡng Hà động.
  - Thẻ chương.
  - Thẻ số liệu, thẻ thời gian.
  - Hiệu ứng "dòng mới tìm lại".
  - Minh họa kiểu phù điêu (không giống thật).

## 6. Tài nguyên (assets, cần duyệt)
- **Ảnh Wikimedia:** tìm qua API `commons.wikimedia.org/w/api.php` (`prop=imageinfo&iiprop=extmetadata`). Chỉ nhận PD, CC0, CC BY, CC BY-SA. Ghi danh sách ghi công vào `asset_manifest`.
- **Met:** API `/public/collection/v1.1/search`, lọc `isPublicDomain`.
- **Nhạc:** `pixabay_music`. Nền ambient trầm, nhỏ hơn giọng khoảng 18–22 dB [nhận định, chỉnh theo tai nghe].
- Lưu ở `projects/<id>/assets/...` (không đưa lên git).

## 7. Dựng (edit/compose)
- Dùng HyperFrames: đọc skill `/hyperframes` và `/hyperframes-cli` trước khi làm.
- Sau mỗi lần sửa composition, chạy `npx hyperframes lint` và `npx hyperframes check`. Cả hai phải đạt.
- Render 1080p. Lần đầu (video thử) phải đo và ghi vào HANDOFF: thời gian render, dung lượng file, xem có vừa tài nguyên của một phiên không.

## 8. Kiểm tra chất lượng trước khi trình anh
- Tiếng khớp hình. Không có khung hình đen. Âm lượng ổn (khoảng −14 LUFS cho YouTube, nhận định).
- Mọi ảnh đều có trong danh sách ghi công.
- Không có chữ sai chính tả trên màn hình. Tên riêng viết thống nhất.
- Đã quyết định có khai báo AI hay không, kèm lý do.

## Nhận diện hình ảnh "Clay & Lapis"
- **Màu:**
  | Vai trò | Màu | Mã |
  |---|---|---|
  | Nền | Đen nhựa đường | `#1B1714` |
  | Chính | Đất nung | `#B5734A` |
  | Nhấn | Lapis | `#1F4E8C` |
  | Điểm sáng | Vàng | `#C9A54C` |
- **Chữ:** tiêu đề dùng serif cổ điển, nhãn dùng sans gọn.
- **Chuyển động:** chậm, có chủ đích. Nhịp thấp đến vừa.
- **Không dùng:**
  - Ảnh AI người ngoài hành tinh hoặc phong cách "ancient aliens".
  - Ảnh AI giống thật.
  - Kiểu trình chiếu ảnh không có lời kể.
  - Cắt nhịp kiểu meme.
  - Lặp đúng một cách mở đầu qua nhiều video.

## Thumbnail (rút ra từ 8 thumbnail thắng lớn, xem `channel-studio/research/competitor_thumbnails_grid.jpg`)
- Tên chủ đề 2–4 chữ, cỡ rất lớn, ít chữ phụ.
- Một chủ thể chính.
- Phong cách minh họa riêng cho từng nền văn minh. Ví dụ Lưỡng Hà dùng màu đất nung, kiểu phù điêu. Không chép phong cách gốm đen cam Hy Lạp mà 2 kênh đối thủ đang dùng giống hệt nhau.
- Kích thước 1280×720, dưới 2 MB. Làm 2 phiên bản để thử bằng tính năng Test & Compare của YouTube [chưa xác minh tính năng này có ở mọi kênh].
