# Phân tích đối thủ @WartimeStories cho kênh ICYFOX (bản 2, 22/11/2026)

Bản này thay `BAO_CAO_v1_cu.md`. Bản cũ gạt đối thủ đi vì "không cùng ngách" rồi kéo về chủ đề cổ đại. Bản này coi kênh anh gửi là **tín hiệu về chủ đề anh muốn làm** và tìm cách làm hợp lệ trong trụ cột P3 (chiến tranh), P1 (bí ẩn) và P2 (sinh tồn).

**Nguồn dữ liệu (tra ngày 22/11/2026)**
- Số liệu: YouTube Data API v3, chạy bằng `scripts/research/yt_api_channel.py`. File: `Wartime_Stories_api.json`, `Wartime_Stories_api.md`, `api_summary.txt`.
- Nội dung: phụ đề tự động của 2 video lấy bằng yt-dlp, lưu ở `subs/` (`UklzcvdHLoM`, `JuwV7lhGEP0`). Video thứ 3 (`QkRRERFPfEM`) bị YouTube trả lỗi HTTP 429 nên chưa lấy được.
- Thumbnail: `thumbs_grid.jpg`, 16 video gần nhất.
- Bình luận: `top_comments.json`, 40 bình luận nổi bật.

## 1. KẾT LUẬN
1. **Đối thủ mạnh nhưng đang đuối.**
   - Hiện có 856K sub và 103,4 triệu view.
   - Trung vị 459K view mỗi video dài. 10 video gần nhất chỉ còn trung bình 225K.
   - Năm 2026 họ đăng gấp khoảng 4 lần (55 video), trong khi trung vị view giảm từ 1,12M (2023) xuống 313K (2026).
2. **Video tổng hợp (compilation) kéo kênh đi xuống.**
   - 14 video "A Compilation of…" có trung vị 261K.
   - Video mới thường từ tháng 8/2026 có trung vị 322K.
   - Họ đang cố lấp lịch bằng cách ghép lại nội dung cũ.
3. **Khoảng trống cho ICYFOX: "chuyện lạ thời chiến CÓ HỒ SƠ THẬT".**
   - Ngay trên kênh của họ, các video dựa trên sự kiện có hồ sơ đạt mức trung vị hoặc cao hơn:
     - Project Blue Book: 1,05M.
     - Phi công Thế chiến 2 đuổi vật thể lạ rồi tử nạn: 552K.
     - Hai thủy thủ biến mất khỏi khinh khí cầu: 496K.
     - Lính Nhật trốn vào đầm lầy: 459K.
     - Tam giác Bermuda: 440K.
   - Mình kể đúng loại chuyện đó, nhưng đi tới cùng: hồ sơ, bản đồ, nguồn trên màn hình, và lời giải tốt nhất hiện có. Đối thủ không làm được việc này, vì họ đọc lời kể không kiểm chứng.
4. **Video đầu đề xuất: "Lady Be Good"**, chiếc B-24 mất tích năm 1943 và được tìm thấy năm 1958 giữa sa mạc Libya. Video thuộc P3 và P2, nguồn chính phủ Mỹ dồi dào (ảnh của USAF và NARA thuộc phạm vi công cộng). Dàn ý và hook 60 giây nằm ở `channel-studio/videos/002-lady-be-good/`.

## 2. CHI TIẾT

### 2.1 Số liệu kênh (YouTube Data API, 22/11/2026)
| Chỉ số | Giá trị |
|---|---|
| Ngày tạo kênh | 14/07/2020 |
| Sub / tổng view / số video | 856.000 / 103.352.590 / 160 (158 video dài, 2 Shorts) |
| Trung vị view video dài | 459.480 |
| Trung bình 10 video dài gần nhất | 224.601 |
| Tỉ lệ video ≥3× trung vị | 10% |
| Số video viral (≥5× trung bình 10 video trước) | 21 |
| Thời lượng trung vị | 38,8 phút |
| Like trên 1.000 view | 33,2 |
| Ngày đăng | Thứ Sáu 80/160, Thứ Bảy 27/160 |
| Nhịp đăng 2026 | 2 video/tháng (tháng 1) tăng dần lên 9 video/tháng (tháng 10) |

**Theo năm** (`api_summary.txt`): 2023 có 15 video, trung vị 1,12M. 2024 có 22 video, trung vị 921K. 2025 có 31 video, trung vị 503K. 2026 có 55 video, trung vị 313K. Tỉ lệ like gần như không đổi (29–40 trên 1.000 view): khán giả cũ vẫn thích, nhưng mỗi video tới được ít người hơn. Đây là tương quan, chưa chứng minh nhân quả.

**10 video nổi bật nhất** (bội số so với trung vị kênh):
| View | ×trung vị | Phút | Tiêu đề |
|---|---|---|---|
| 4,78M | 10,4 | 36 | Animals Aren't Supposed to Talk |
| 3,35M | 7,3 | 46 | Shocking Stories from Soldiers and Drone Operators |
| 2,96M | 6,5 | 36 | Marines and Soldiers Stalked by Creatures in the Woods |
| 2,36M | 5,1 | 29 | These Men Had No Trouble Staying Awake on Watch -- They Were Terrified |
| 2,14M | 4,7 | 48 | Japanese Soldiers Reported Man-Eating Creatures in the Jungle |
| 2,10M | 4,6 | 32 | Terrifying Supernatural Encounters in a War Zone |
| 2,07M | 4,5 | 33 | Army Police Chased By Massive Creature in the 1980s |
| 1,91M | 4,2 | 40 | A Soldier Saw Something in Honduras... |
| 1,88M | 4,1 | 30 | Can Anyone Explain What They Saw? |
| 1,73M | 3,8 | 31 | USN Petty Officer and Others Report Megalodon Sightings |

### 2.2 Công thức tiêu đề
- **Người có thẩm quyền làm chủ ngữ:** Soldiers, Marines, USN Petty Officer, Coastguardsmen, Navy SEAL. Người xem tin lời kể hơn vì người kể là lính.
- **Động từ chứng kiến:** saw, reported, encountered, stalked.
- **Điều không nên xảy ra:** "Aren't Supposed to", "Can Anyone Explain", "Something is Wrong With…".
- Không dùng số, không dùng năm. Câu ngắn, 5–9 từ.
- Câu bỏ lửng "..." xuất hiện ở 4/24 video nổi bật.

### 2.3 Thumbnail (`thumbs_grid.jpg`)
- Nền đen. **Chỉ một màu nhấn xanh ngọc.** Tranh vẽ minh họa kiểu truyện tranh, không dùng ảnh thật.
- 2–5 chữ in hoa rất to, chiếm nửa khung.
- Dải chữ thương hiệu cố định ở đáy: "STRANGE BUT TRUE MILITARY STORIES".
- Nhìn lướt là nhận ra kênh. Học **sự nhất quán**, không học màu hay câu chữ của họ.

### 2.4 Nội dung bên trong (phụ đề 2 video)
**"Animals Aren't Supposed to Talk"** (4,78M, 36 phút, khoảng 5.500 từ, tức khoảng 152 từ/phút):
- **0:00–2:30, mở bằng bối cảnh văn hóa** chứ không dọa: người Navajo, lính truyền tin mật mã Navajo trong Thế chiến 2, rồi truyền thuyết skinwalker. Câu chuyển: "This is the smoke pit and these are their stories about…".
- **2:30–6:00, kể một truyền thuyết có ghi nguồn** (một cuốn sách tuyển truyện của người bản địa, nêu tên người kể) để người xem "hiểu luật chơi" trước.
- **6:00 trở đi, 4–6 lời kể của lính.** Mỗi chuyện đều nêu nguồn: "submitted to the Paranormal Scholar website", "submitted to … the Tales from the Grid Square project".
- **Kết:** cảm ơn, kêu gọi ủng hộ qua Patreon, quảng cáo podcast đối tác.

**"These Men Had No Trouble Staying Awake on Watch"** (2,36M, 29 phút, khoảng 4.900 từ):
- **0:00–1:09:** giới thiệu khái niệm "smoke pit" (nơi lính kể chuyện), rồi nêu tên 3 người kể (lính Canada, lính Mỹ, lính thủy đánh bộ Mỹ).
- **1:09:** vào thẳng lời kể ngôi thứ nhất với chi tiết rất cụ thể: Kandahar, sông Arghandab, 20 xe xếp vòng tròn, ca gác mỗi giờ. Chi tiết kỹ thuật làm người xem tin.
- **Kết:** một chuyện hài nhẹ (bị nghi hút cần sa vì đốt nhang) để xả căng thẳng, rồi kêu gọi đăng ký và ủng hộ.

**Rút ra:**
1. Mở bằng bối cảnh có thật, rồi mới vào chuyện lạ.
2. Chi tiết quân sự cụ thể tạo niềm tin.
3. Ghi nguồn từng chuyện, kể cả với chuyện không kiểm chứng.
4. Cấu trúc tuyển tập 4–6 chuyện, mỗi chuyện 5–8 phút.

### 2.5 Khán giả nói gì (`top_comments.json`)
- Khen phần dựng: diễn viên đóng vai người kể, tranh vẽ, âm thanh. Khen "no cheap horror".
- Cựu binh tự kể chuyện của mình trong bình luận. Kênh trở thành nơi cộng đồng lính tụ lại.
- Người xem từ nhiều nước kể truyền thuyết quê mình: có nhu cầu tìm hiểu "gốc thật" phía sau chuyện lạ.

### 2.6 Xếp vào trụ cột ICYFOX và cách làm hợp lệ
| Loại chuyện của đối thủ | Trụ cột | Cách ICYFOX làm hợp lệ |
|---|---|---|
| Vật thể bay lạ thời chiến (UFO, Blue Book) | P3 + P1 | Chỉ chọn vụ có hồ sơ quân đội hoặc báo chí đương thời (ví dụ foo fighters 1944, "trận Los Angeles" 1942). Kết bằng các giả thuyết có nguồn |
| Lính gặp sinh vật lạ, thú dữ | P3 + P2 | Chọn sự kiện có tư liệu (đảo Ramree 1945). Tách rõ đâu là lời kể, đâu là điều sử gia xác nhận. Không tả cảnh ghê rợn |
| Biến mất, máy bay hay tàu mất tích | P1 + P3 + P2 | Lady Be Good, khinh khí cầu L-8, USS Cyclops, Flight 19. Báo cáo điều tra của Hải quân và Không quân Mỹ thuộc phạm vi công cộng |
| Điềm báo, thiên thần, hồn ma chiến trường | P3 (truyền thuyết) | Kể như **lịch sử của một truyền thuyết**: Thiên thần Mons 1914 bắt nguồn từ truyện ngắn "The Bowmen" của Arthur Machen. Ghi rõ "legend", "claimed" |
| Lời kể lính hiện đại không kiểm chứng | Không làm | Không kiểm chứng được, lại dễ bị xem là reused content nếu lấy từ sách hay web của người khác |

### 2.7 Nên học và không nên học
| Nên học | Không học |
|---|---|
| Video 29–40 phút, khoảng 150 từ/phút | Chuyện "không ai giải thích được" mà không có nguồn |
| Tiêu đề lấy người chứng kiến làm chủ ngữ, kèm động từ chứng kiến | Lời, tranh, nhạc, câu "Strange but true" của họ |
| Mở bằng bối cảnh thật, chi tiết quân sự cụ thể | Đăng dồn dập và video compilation ghép lại (trung vị chỉ 261K) |
| Thumbnail một màu nhấn và dải thương hiệu cố định | Màu xanh ngọc, kiểu tranh của họ |
| Series có tên, playlist theo chủ đề | Lời kể mạng không xác minh |
| Kết hơi nhẹ nhõm, kêu gọi cộng đồng góp chuyện | |

**Lợi thế của họ mình không có:** người dẫn thật, diễn viên lồng tiếng, cộng đồng cựu binh, thương hiệu Bedtime Stories.
**Cách bù:** hồ sơ gốc hiện trên màn hình (giấy tờ NARA, bản đồ hành trình, ảnh USAF), lời giải đến cùng, và hình ảnh dựng kỹ từng video.

## 3. DẪN CHỨNG
- YouTube Data API: `Wartime_Stories_api.json` (fetched_at 22/11/2026).
- Phụ đề: `subs/UklzcvdHLoM.txt`, `subs/JuwV7lhGEP0.txt`.
- Kênh tham chiếu Yesterday: `references/content-pillars.md` (YouTube Data API 22/11/2026). Mariana 2,8M, Bermuda 2,1M, Survival 1,0M, Korean War 1,1M.
- Nguồn kiểm sơ bộ cho video đề xuất, tra 22/11/2026:
  - Lady Be Good: [National Museum of the USAF](https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196178/), [NARA Unwritten Record](https://unwritten-record.blogs.archives.gov/?p=15424), [Air & Space Forces Magazine 02/2014](https://www.airandspaceforces.com/article/0214lady/).
  - Foo fighters: [Smithsonian Air & Space](https://www.smithsonianmag.com/air-space-magazine/what-were-mysterious-foo-fighters-sighted-ww2-night-flyers-180959847/), [History.com](https://www.history.com/articles/wwii-ufos-allied-airmen-orange-lights-foo-fighters).

## 4. BƯỚC TIẾP THEO
- Kế hoạch 12 tuần: `KE_HOACH_90_NGAY.md` (cùng thư mục).
- Video 002 Lady Be Good đang ở cổng duyệt kịch bản: `channel-studio/videos/002-lady-be-good/script_outline.md`.
- Lấy lại phụ đề video `QkRRERFPfEM` khi YouTube hết chặn (lỗi 429).
