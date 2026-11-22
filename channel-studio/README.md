# channel-studio: kênh YouTube Clay & Lapis

Không gian làm việc của kênh. Quy trình vận hành nằm trong skill `.claude/skills/hoang-dung-clay-lapis-studio/`.

| Thư mục / file | Nội dung |
|---|---|
| `HANDOFF.md` | Trạng thái mới nhất. **Đọc đầu tiên** |
| `channel/` | Thiết lập kênh, lịch đăng, kế hoạch tự động hóa |
| `videos/NNN-slug/` | Mỗi video một thư mục: README, proposal, kịch bản theo phần, gói đăng |
| `projects/` | Bản sao hồ sơ dự án OpenMontage (checkpoint, artifacts). Thư mục `projects/` gốc bị gitignore nên phải sao lưu ở đây |
| `research/` | Số liệu quét ngách và đối thủ |
| `guides/` | Ảnh hướng dẫn cho anh |

Mở phiên: `bash .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_start.sh`
Đóng phiên: `python3 .claude/skills/hoang-dung-clay-lapis-studio/scripts/session_end.py -m "…" --trailer "…"`
