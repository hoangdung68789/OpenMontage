# Quy trình dựng video v2 (áp dụng từ 23/11/2026)

Thay cho cách dựng v1 (ảnh tĩnh + Ken Burns + hòa hình). Cơ sở nghiên cứu: `edit-standard.md`. Thư viện hiệu ứng: `edit-library.md`. Công thức theo thể loại: `genre-recipes.md`. Công cụ: `channel-studio/motion-kit/icyfox_motion.py` (v2).

Mục tiêu đo được của một video dài đạt chuẩn:
- Không có đoạn đứng hình: `static_pct` ≤ 2%, đoạn tĩnh dài nhất < 4 giây, `pct_still` ≤ 25% (`motion_metrics.py`).
- Có thay đổi thị giác trung bình mỗi 1,5–6 giây, không khoảng nào quá 8 giây (`icyfox_motion.py validate`).
- Chữ đọc kịp: thời gian hiện ≥ 0,5 + 0,3 giây × số từ + 1 giây; tương phản đạt WCAG AA (`hyperframes check`).
- Tiếng: −14 LUFS tích hợp, đỉnh thật ≤ −1 dBTP (`icyfox_motion.py finish`). Hiệu ứng âm thanh ≤ 15/phút, mỗi tiếng có nguyên nhân trên hình.

## 1. Cấu trúc thư mục mới cho mỗi video
Tạo bằng `python3 SK/scripts/new_video.py create NNN-slug --title "…" --genre war`; bảng âm thanh: `new_video.py cuesheet render/project/sfx_cues.json 05_sound/CUE_SHEET.md` (không ghi đè file đã có).

```
channel-studio/videos/NNN-slug/
├── README.md                 # thẻ video: trụ cột, thể loại dựng, trạng thái từng giai đoạn
├── 00_brief/                 # GĐ 1: đề xuất + nghiên cứu
│   ├── script_outline.md     #   dàn ý, hook 60 giây, chương, nguồn (autopilot đọc file này)
│   └── sources.md            #   nguồn dữ kiện + nguồn ảnh (giấy phép)
├── 01_script/                # GĐ 2: kịch bản
│   ├── script_part1.md …     #   mỗi phần QA ĐẠT (qa_check.py --mark)
│   └── script_full_ready.txt #   có file này = kịch bản đủ
├── 02_storyboard/            # GĐ 3: phân cảnh (bản vẽ của video)
│   ├── STORYBOARD.md         #   bảng: câu thoại → loại cảnh → máy quay → chuyển cảnh → chữ → âm thanh
│   └── motion_plan.json      #   kế hoạch máy đọc được cho motion kit
├── 03_assets/                # GĐ 4: tài nguyên
│   ├── img/  video/  maps/   #   ảnh, đoạn phim, nền bản đồ
│   ├── audio/vo/             #   giọng đọc theo đoạn + manifest.json (voicestudio_tts.py)
│   ├── audio/music/          #   nhạc nền (giấy phép thương mại)
│   ├── audio/sfx/            #   hiệu ứng âm thanh riêng của video (ngoài bộ chung motion-kit/sfx)
│   └── CREDITS.md            #   mỗi file: nguồn, tác giả, giấy phép, link
├── render/                   # GĐ 5: dự án HyperFrames sinh ra + MP4
│   └── RENDERED.txt          #   đường dẫn, dung lượng, thời gian render, số đo chuyển động
├── 05_sound/                 # GĐ 6: âm thanh
│   ├── CUE_SHEET.md          #   từ sfx_cues.json: giây, tiếng, nguyên nhân
│   └── LOUDNESS.txt          #   số đo LUFS, LRA, đỉnh thật sau finish
├── 06_review/                # GĐ 7: kiểm định
│   ├── REVIEW.md             #   lỗi P0/P1/P2 + cách sửa + kết quả kiểm lại
│   ├── metrics.txt           #   motion_metrics.py
│   └── contact_sheet.jpg     #   lưới khung hình
└── package/                  # GĐ 8: gói đăng (publish-package.md)
```
Video cũ (001, 002) giữ cấu trúc cũ; `autopilot.py` đọc được cả hai (tìm `script_*` ở gốc và trong `00_brief/`, `01_script/`).

## 2. Các giai đoạn và cổng kiểm (không qua cổng thì không sang bước sau)
| GĐ | Việc | Công cụ | Cổng kiểm (đạt khi) | Thẻ tasks.py |
|---|---|---|---|---|
| 1 Brief | Chọn chủ đề có bằng chứng, dàn ý, hook | `niche_outliers.py`, `trend_verify.py`, `topic_check.py` | Dàn ý có nguồn, hook 60 giây viết đủ | outline |
| 2 Kịch bản | Viết từng phần | `qa_check.py --mark` | Mỗi phần QA ĐẠT, số từ khớp | script |
| 3 Phân cảnh | Chia kịch bản thành nhịp (beat), chọn thể loại dựng theo `genre-recipes.md`, viết STORYBOARD.md rồi motion_plan.json | `icyfox_motion.py validate` | Validate đạt: khoảng trống ≤ 8 s, chuyển cảnh xoay vòng, cắt/lóe ≤ 1/3, SFX ≤ 15/phút, chữ đọc kịp, ảnh có ghi công | scene |
| 4 Tài nguyên + giọng | Tải ảnh, bản đồ, nhạc; đọc giọng | `voicestudio_tts.py narrate`, `media-use` | Mọi file có dòng CREDITS; `dur` mỗi cảnh = độ dài giọng thật của đoạn | voice / scene |
| 5 Dựng | Sinh dự án, kiểm, render nháp | `icyfox_motion.py build`, `npx hyperframes lint`, `check`, `render -q draft` | lint 0 lỗi, check đạt (chữ đạt AA) | render |
| 6 Âm thanh | Nghe điểm đặt SFX, nhạc hạ khi có lời, chuẩn hóa | `icyfox_motion.py finish` | −14 LUFS ±1, đỉnh ≤ −1 dBTP, CUE_SHEET đủ nguyên nhân | render |
| 7 Kiểm định | Xem lưới khung, đo chuyển động, ghi P0/P1/P2 | `motion_metrics.py`, ffmpeg tile | static ≤ 2%, tĩnh dài nhất < 4 s; không còn P0, P1 | render (tasks.py tự chạy cổng) |
| 8 Render chuẩn + gói | Render `-q standard`, gói đăng | `hyperframes render`, `publish-package.md` | `RENDERED.txt` + `package/` đủ file | render / package |

Mức lỗi ở GĐ 7: **P0** hỏng hình/tiếng/chữ sai sự thật (phải sửa); **P1** người xem sẽ thấy (chữ chưa đọc kịp, chuyển cảnh lặp, SFX lệch hình, màu nhảy giữa cảnh: phải sửa); **P2** đánh bóng (ghi lại, sửa nếu còn thời gian).

## 3. Phân cảnh (GĐ 3) làm thế nào
1. Đọc kịch bản, đánh dấu **nhịp**: mỗi câu hoặc cụm 1–3 câu mang một ý = một nhịp. Mỗi nhịp phải có ít nhất một thay đổi thị giác (cảnh mới, góc máy mới, chữ, điểm tô, số).
2. Gắn **chức năng** cho từng nhịp: mở (hook), bối cảnh, bằng chứng, chuyển hướng, cao trào, kết. Chức năng quyết định loại cảnh (bảng ở `edit-library.md` §1).
3. Chọn **thể loại dựng** (`genre`) theo trụ cột, đọc công thức trong `genre-recipes.md`, ghi đè bằng `style` nếu video cần khác.
4. Đặt **điểm nhấn** đúng chỗ, mỗi thứ dùng ít: một `payoff` cho cả chương (riser + impact), một từ nhấn `*…*` mỗi dòng chữ, `big` cho con số quan trọng nhất.
5. Viết STORYBOARD.md (mẫu: `SK/templates/video-project/02_storyboard/STORYBOARD.md`), rồi chuyển thành `motion_plan.json`. Chạy `validate` cho tới khi đạt.

## 4. Lệnh dựng đầy đủ
```bash
V=channel-studio/videos/NNN-slug
python3 channel-studio/motion-kit/icyfox_motion.py validate $V/02_storyboard/motion_plan.json
python3 channel-studio/motion-kit/icyfox_motion.py build    $V/02_storyboard/motion_plan.json $V/render/project
cd $V/render/project && npx -y hyperframes@0.8.171 lint . && npx -y hyperframes@0.8.171 check .
npx -y hyperframes@0.8.171 render . -q draft -o renders/draft.mp4
cd - && python3 channel-studio/motion-kit/icyfox_motion.py finish $V/render/project/renders/draft.mp4 $V/render/draft_final.mp4 > $V/05_sound/LOUDNESS.txt
python3 SK/scripts/motion_metrics.py $V/render/draft_final.mp4 > $V/06_review/metrics.txt
ffmpeg -i $V/render/draft_final.mp4 -vf "fps=1/6,scale=480:-1,tile=4x3" -frames:v 1 $V/06_review/contact_sheet.jpg
```
Đóng thẻ: `tasks.py done T-xxx --evidence $V/render/draft_final.mp4 …` (thẻ loại render tự chạy cổng chuyển động).

## 5. Danh sách kiểm định (GĐ 7, ghi vào REVIEW.md)
- [ ] 3 giây đầu có chuyển động và chữ/hình nói rõ câu hỏi của video.
- [ ] Không cảnh nào đứng yên > 4 s; mỗi ảnh có ít nhất 2 góc máy khác nhau nếu dài > 7 s.
- [ ] Chuyển cảnh: 3–5 kiểu, không 2 mối nối liền nhau cùng kiểu, mỗi kiểu có lý do (xem bảng lý do ở `edit-library.md` §3).
- [ ] Chữ đáp rồi đứng yên; lối ra ngắn hơn lối vào; mỗi dòng ≤ 1 từ nhấn; chữ trong vùng an toàn; không đè lên mặt người, chi tiết chính.
- [ ] Màu: cùng một màu phim trên mọi cảnh; màu nhấn chỉ dùng cho điều quan trọng.
- [ ] Âm thanh: giọng rõ nhất; nhạc hạ khi có lời; mỗi SFX khớp hình (lệch ≤ 1 khung); chỉ một riser cho mỗi cao trào.
- [ ] Ghi công đủ trên hình (ảnh lưu trữ) và trong CREDITS.md.
- [ ] Số đo: metrics.txt, LOUDNESS.txt đạt mốc ở đầu file này.
