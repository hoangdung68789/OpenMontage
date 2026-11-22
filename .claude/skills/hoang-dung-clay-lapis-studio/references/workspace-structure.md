# Cấu trúc thư mục và quy ước

## Nơi lưu trữ
| Loại | Nơi lưu | Ghi chú |
|---|---|---|
| Tài liệu, kịch bản, hồ sơ dự án, số liệu nghiên cứu | GitHub `hoangdung68789/OpenMontage`, nhánh `ccr-6640cec8-2anthl`, thư mục `channel-studio/` | Bền. Đẩy lên cuối mỗi phiên |
| Skill này | Cùng repo và nhánh: `.claude/skills/hoang-dung-clay-lapis-studio/`. Có thể cài thêm ở cấp tài khoản claude.ai (file `.skill`) | Sửa skill thì sửa ở repo, rồi đóng gói lại |
| Trạng thái từng video | Notion "Clay & Lapis – Video Pipeline" | Anh xem được trên điện thoại |
| File lớn (MP4, WAV dài) | Google Drive (biến `GDRIVE_REFRESH_TOKEN`, xin quyền riêng) hoặc tạm trong container | **Không đưa lên git.** GitHub chặn file trên 100 MB, và repo sẽ phình to |
| Khóa và token | Cài đặt môi trường `video-channel-studio` | Không bao giờ nằm trong file |

## Cây thư mục `channel-studio/`
```
channel-studio/
├── HANDOFF.md                 # trạng thái mới nhất: đọc đầu phiên, cập nhật cuối phiên
├── README.md                  # bản đồ ngắn
├── channel/
│   ├── channel_setup.md       # tên kênh, About, từ khóa, danh sách phát, cài đặt tải lên, checklist YPP, lịch đăng
│   └── automation_plan.md     # kế hoạch tự động hóa
├── videos/
│   └── NNN-slug/              # mỗi video một thư mục, ví dụ 001-gilgamesh-lost-lines
│       ├── README.md          # trạng thái, link Notion, checklist (templates/video_readme_template.md)
│       ├── proposal.md        # đề xuất đã duyệt
│       ├── script_partN.md    # kịch bản theo phần (templates/script_section_template.md)
│       ├── voice/             # ghi chú mẫu giọng (file âm thanh không đưa lên git)
│       ├── shorts/            # kịch bản và mốc cắt Shorts
│       ├── render/            # dự án HyperFrames để render trên máy anh (index.html, compositions/, assets/ gồm MP3 theo đoạn và JPG đã nén). Không có final.mp4
│       └── package/           # title.txt, description.md, tags.txt, subtitles/*.srt, thumbnail.png (dưới 2 MB)
├── projects/                  # bản sao của OpenMontage projects/<project-id>/ (checkpoint, artifacts)
├── research/                  # kết quả quét ngách và đối thủ (JSON), lưới thumbnail
└── guides/                    # ảnh hướng dẫn cho anh (ví dụ nhập khóa Gemini)
```

## Quy ước
- **Tên thư mục video:** `NNN-slug`, đánh số tăng dần, slug tiếng Anh viết thường có gạch nối. **Project ID của OpenMontage** dùng slug ngắn, ví dụ `gilgamesh-pilot`. Ghi cặp tên này trong README của video.
- **Kịch bản:** mỗi phần khoảng 1.000–1.300 từ (8–10 phút đọc). Đầu file ghi trạng thái: `chờ duyệt` hoặc `ĐÃ DUYỆT <ngày>`.
- **Hồ sơ dự án:** OpenMontage bắt buộc artifacts nằm ở `OpenMontage/projects/<id>/`, nhưng thư mục này bị gitignore. Đầu phiên `session_start.sh` chép từ `channel-studio/projects/` về. Cuối phiên `session_end.py` chép ngược lại, bỏ qua `assets/video`, `renders/` và file trên 20 MB.
- **Khi `git add` thư mục `channel-studio/projects/`** phải dùng `-f`, vì `.gitignore` có dòng `projects/` khớp với mọi thư mục tên `projects`. Script đã xử lý việc này.

## Bảng Notion: các cột
Video (tiêu đề) · Status (Ý tưởng → Nghiên cứu → Viết kịch bản → Chờ duyệt → Đang dựng → Chờ đăng → Đã lên lịch → Đã đăng) · Loại (Video dài / Short) · Chủ đề · Thời lượng (phút) · Ngày đăng · Link YouTube · Link Drive · Việc cần anh làm · Chi phí (USD) · Giờ xem 7 ngày · Sub mới 7 ngày · Mã (CLAY-VID-n).
Khi tạo dòng mới: dùng `notion-create-pages` với `parent.data_source_id = 4201dcd7-7c95-8188-8452-000b17602005`.
