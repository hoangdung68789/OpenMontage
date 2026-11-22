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
- Công cụ `gemini_tts` (OpenMontage, `tools/audio/gemini_tts.py`), model `gemini-3.8-flash-tts`, xuất WAV. Gọi qua registry:
  ```python
  from tools.tool_registry import registry
  registry.discover()
  registry.get("gemini_tts").execute({...})
  ```
- Xem danh sách giọng: `{"operation": "list_voices"}` với `GEMINI_API_KEY=proxy-injected`. Danh sách có rất nhiều giọng và ngôn ngữ, cần lọc giọng tiếng Anh Mỹ.
- **Mẫu giọng:** lấy đoạn S0.4 (nhiều sắc thái nhất), làm 3 giọng khác nhau. Gửi anh MP3 (`ffmpeg -i x.wav -b:a 128k x.mp3`), gửi bằng SendUserFile.
- Mẫu được duyệt thì giữ cố định giọng và model. Đổi giọng hay model phải làm mẫu và duyệt lại (theo `skills/meta/voice-performance-director.md`).
- Đọc dài: chia theo từng đoạn, mỗi lần gọi dưới khoảng 10 phút âm thanh, rồi ghép lại.

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
