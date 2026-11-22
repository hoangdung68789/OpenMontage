# Nghiên cứu đối thủ và ngách

## Công cụ (trong `scripts/research/`)
| Script | Việc | Cách chạy |
|---|---|---|
| `niche_scan.py` | Quét nhiều ngách: mỗi ngách 2 từ khóa, lấy 10 kênh có video nhiều view nhất, đo 120 video gần nhất của mỗi kênh | `python3 niche_scan.py <thư_mục_kết_quả>`, sửa danh sách `NICHES` trong file trước khi chạy |
| `summarize.py` | Tóm tắt kết quả quét ngách | `python3 summarize.py <thư_mục_kết_quả>` |
| `deep_scan.py` | Quét sâu một ngách: 12 từ khóa, 30 kênh, 60 video mỗi kênh | `python3 deep_scan.py <thư_mục_kết_quả>`, sửa `QUERIES` |
| `deep_analyze.py` | So hiệu suất theo thời lượng, chủ đề, mẫu tiêu đề; liệt kê 15 video vượt trội nhất | `python3 deep_analyze.py <thư_mục>/deep.json` |

Tất cả dùng yt-dlp ở chế độ `--flat-playlist`, kèm `--extractor-args youtubetab:approximate_date` để có ngày đăng gần đúng.
- **Lấy được:** tiêu đề, view (đã làm tròn), thời lượng, số sub của kênh, ngày đăng gần đúng (dạng "x tháng trước").
- **Không lấy được:** số liệu từng video như like hay bình luận, vì YouTube bắt kiểm tra bot. Muốn có thì dùng YouTube Data API.
- Lưu kết quả ở `channel-studio/research/<ngày>-<chủ-đề>/`.

## Định nghĩa
- **Điểm vượt trội** của một video = view của video ÷ trung vị view 30 video gần nhất của chính kênh đó.
- **VIRAL** (theo quy tắc của anh): view ≥ 5 × trung bình 10 video gần nhất của chính kênh đó. Không đủ dữ liệu thì không được gọi là viral.
- **Kênh trẻ:** video cũ nhất dưới 24 tháng tuổi. Tuổi này là gần đúng, chỉ tính được khi kênh có dưới 120 video.

## Phát hiện đã có (quét ngày 22/11/2026, 30 kênh, 1.454 video dài)
| Thời lượng | Điểm trung vị | Tỉ lệ video ≥ 3× |
|---|---|---|
| 8–20 phút | 0,90 | 6% |
| 20–60 phút | 1,05 | 19% |
| 60–120 phút | 0,96 | 13% |
| Trên 120 phút | 1,21 | 22% |

- **Chủ đề:**
  - Lưỡng Hà, Sumer: 36% video ≥ 3× (mẫu nhỏ, 22 video).
  - Mẫu tiêu đề "ENTIRE / Complete": trung vị 1,20.
  - Bắc Âu: 1,14. Hy Lạp: 0,92.
- **Tín hiệu đáng chú ý:**
  - Các kênh lịch sử dẫn đầu ghi "[No AI]" trên tiêu đề (Historically, Beginning To Now). Ở ngách này, giọng AI là điểm trừ.
  - Nhóm kênh "lịch sử ru ngủ" đông nhưng trung vị thấp, và thường ghi "No Ads" trên tiêu đề, đi ngược mục tiêu kiếm tiền.
- **Tần suất đăng:**
  - Kênh đăng ≤ 12 video/năm: trung vị 1,7 triệu view/video.
  - Kênh đăng ≥ 60 video/năm: trung vị 50 nghìn view/video.
  - Đây là tương quan, không phải nhân quả.
- **Đối thủ tham chiếu:** Fall of Civilizations, History Time, Beginning To Now, Historically, Uncharted Mysteries, Dreamoria, Astraway. Link kênh có trong `channel-studio/research/deep_scan/deep.json`.

## Chọn chủ đề tiếp theo
1. Ưu tiên chủ đề vừa có điểm vượt trội cao vừa ít kênh làm.
2. Mỗi chủ đề phải có ít nhất một phát hiện hoặc góc kể từ 2010 trở lại, để kênh có lý do tồn tại ("lost lines", "recovered").
3. Tránh chủ đề dễ thành lịch sử giả ("Nobody can explain", người ngoài hành tinh cổ đại), và chủ đề chính trị hiện tại.
4. Trình bày cho anh dạng bảng: chủ đề · bằng chứng (link, số liệu, ngày tra) · khoảng trống · rủi ro · thời lượng đề xuất.

## Xem nhanh thumbnail đối thủ
Tải ảnh từ `https://i.ytimg.com/vi/<id>/hqdefault.jpg`, ghép thành lưới bằng ffmpeg `hstack/vstack`, rồi xem trực tiếp bằng công cụ Read để rút ra quy luật.
