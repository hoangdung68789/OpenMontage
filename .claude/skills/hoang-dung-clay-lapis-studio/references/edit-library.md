# Thư viện hiệu ứng dựng (motion kit v2)

Mỗi mục: **dùng khi** · **khóa trong motion_plan.json** · **kết hợp với** · **tránh**. Cơ sở và nguồn: `edit-standard.md`. Thứ tự ưu tiên khi chọn: phục vụ câu chuyện (người xem hiểu nhanh hơn) → giữ chân (có thay đổi) → đẹp.

Quy tắc chung (áp cho mọi mục):
- Mỗi hiệu ứng phải có **nguyên nhân** trong lời kể hoặc trên hình. Không có nguyên nhân thì cắt thẳng hoặc hòa hình.
- **Chuyển động ở nền, chữ đứng yên.** Chữ đáp xuống rồi đứng yên để đọc; máy quay, bụi, hạt film, vệt sáng mới là thứ chuyển động.
- **Lặp lại là dấu hiệu dựng vụng**: cùng một kiểu hiện, cùng một độ cong (ease), cùng một chuyển cảnh liền nhau.

## 1. Bố cục cảnh (loại cảnh, khóa `type`)
| Loại | Dùng khi (chức năng nhịp) | Khóa | Kết hợp với | Tránh |
|---|---|---|---|---|
| `title` | Mở video, mở chương | `text` (bọc `*từ*` để nhấn), `sub`, `src` (ảnh nền), `text_fx`, `letterbox` | letterbox, `land` SFX, push chậm ở nền | Tiêu đề > 9 từ; tiêu đề trôi sau khi đáp |
| `photo` | Bằng chứng bằng ảnh, giới thiệu người/vật | `src`, `credit`, `caption`, `details` [[x%,y%,phóng]], `moves`, `lower` | lower third ở lần đầu nhân vật xuất hiện; rack/punch để chỉ chi tiết | Một ảnh > 7 s chỉ một góc máy |
| `document` | Tài liệu gốc, nhật ký, báo cáo | `src`, `credit`, `highlights` [[x%,y%,w%,h%,giây]] | typewriter quote ngay sau; dip trước | Tô > 3 chỗ trên một trang |
| `map` | Hành trình, vị trí, khoảng cách | `route` [[x,y],…], `places` [[x,y,"TÊN"]], `caption` | stat ngay sau (khoảng cách), whip vào | Nhãn chồng nhau; > 5 địa điểm |
| `stat` | Một con số quyết định câu chuyện | `value`, `label`, `decimals`, `big`, `payoff` | `payoff` (riser→impact) một lần mỗi chương | Hai stat liền nhau; số không có đơn vị |
| `quote` | Lời nhân chứng, câu then chốt | `text`, `by`, `text_fx` (typewriter cho thư, nhật ký) | dip vào, nhạc hạ | Trích > 25 từ (chia đôi) |
| `split` | So sánh trước/sau, hai phía | `srcs` [a,b], `labels` [a,b], `credit` | đường chia mở ra theo nhịp lời | Hai ảnh cùng tông, không thấy khác |
| `triptych` | Ba vật chứng, ba người, liệt kê | `srcs` [a,b,c], `credit` | một whoosh cho cả cụm | Dùng hai lần liền |
| `timeline` | Mốc thời gian, nhảy năm | `items` [{"date":"1943","label":"…"},…] | pop mỗi mốc, wipe vào | > 5 mốc trên một khung |

Phủ thêm lên mọi loại cảnh: `lower` = {title, sub, at} (thanh tên), `letterbox` = true (khung cinema 2.39:1 cho cảnh nặng cảm xúc), `transition` (ép kiểu chuyển cảnh vào cảnh này).

## 2. Máy quay (khóa `moves` của photo, hoặc tự chọn)
| Chuyển động | Dùng khi | Cảm giác | Tránh |
|---|---|---|---|
| `push` (đẩy vào) | Tăng căng thẳng, sắp có tiết lộ | tiến gần, tập trung | Đẩy vào mọi ảnh (thành máy móc) |
| `pull` (kéo ra) | Hé lộ bối cảnh, kết đoạn | cô đơn, quy mô lớn | Kéo ra ở đầu đoạn |
| `panl` / `panr` | Ảnh ngang, đám đông, phong cảnh, đọc dòng chữ | đi theo, khám phá | Lia ngược chiều chuyển động trong ảnh |
| `tilt` | Ảnh dọc, tòa nhà, người đứng | đo chiều cao, uy nghi | Ảnh ngang thấp |
| `punch` (cắt phóng) | Nhấn một chi tiết theo nhịp lời ("look at his hands") | đột ngột, chú ý | > 1 lần trong 10 s |
| `rack` (kéo nét) | Chuyển sự chú ý, mở một cảnh nhớ lại | mơ hồ → rõ | Dùng cho chữ |
| Chiều sâu (parallax) | Tự có ở cảnh `photo` khung đầu | ảnh có không gian | — |
| Rung khung (weave) | Tự có theo thể loại (`weave`) | phim cũ, tư liệu | Mức cao ở thể loại cổ đại |

Tốc độ: phóng 8–14% trên toàn cảnh; một góc máy 5–7,5 s (`shot` của thể loại); ease `sine.inOut` cho máy quay, không dùng `back`/`elastic`.

## 3. Chuyển cảnh (khóa `transition`; tự xoay theo `trans` của thể loại)
| Kiểu | Lý do để dùng | Thời lượng | SFX tự gắn | Tránh |
|---|---|---|---|---|
| `cut` | Mặc định giữa các nhịp cùng mạch | 0 | — | > 1/3 số mối nối |
| `dissolve` | Thời gian trôi, hồi tưởng, dịu xuống | 0,7 s | — | Cảnh có nhịp nhanh |
| `dip` | Kết một ý lớn, chuyển chương, sau câu nặng | 3 khung tối ~40% rồi cắt | — | Hai lần liền |
| `whip` | Nhảy địa điểm, "trong khi đó…" | 0,28–0,3 s, nhòe ngang | whoosh | Cảnh buồn, tĩnh |
| `blurswap` | Đổi góc nhìn cùng chủ đề, nhẹ | 0,2 s | — | — |
| `iris` | Thu về một điểm / mở ra từ một điểm (bản đồ, chi tiết) | 0,5 s | whoosh nhỏ | Dùng như trang trí |
| `wipe` | Sang trang tài liệu, mốc thời gian mới | 0,6 s | whoosh | Hướng quét ngược mạch đọc |
| `flash` | Tiếng nổ, ánh chớp, sự kiện đột ngột | lóe 0,35 s | impact | Không có sự kiện tương ứng |

Kiểm tự động: không 2 mối nối liền nhau cùng kiểu; `cut` + `flash` ≤ 1/3 số mối nối.

## 4. Chữ: hiệu ứng (khóa `text_fx`)
| Kiểu | Dùng khi | Thể loại hợp |
|---|---|---|
| `blurword` | Mặc định cho tiêu đề và phụ đề ý: từng từ rõ dần, cách 67 ms | chiến tranh, cổ đại |
| `greyink` | Câu hỏi, điều bí ẩn: từ xám đậm dần như mực | bí ẩn |
| `letters` | Tên riêng, nhãn kỹ thuật: từng ký tự | thảm họa, sinh tồn |
| `typewriter` | Thư, nhật ký, điện tín, biên bản (tự có tiếng gõ) | mọi thể loại khi trích tài liệu |

Thời lượng: hiện ≥ 0,5 + 0,3 giây/từ; lối ra ngắn hơn lối vào 40–50%. Tiêu đề cao 4–9% khung; chữ nhỏ nhất ≥ 2,6% cạnh ngắn (28 px ở 1080p).

## 5. Chữ: màu
- Màu chữ chính = `ink` (trắng ngà) trên nền tối hoặc có lớp tối (`tscrim`) phía sau. Kiểm tương phản bằng `hyperframes check` (AA, ≥ 3:1 cho chữ lớn).
- Một từ nhấn mỗi dòng: `*từ*` → màu `accent` pha 30% trắng (đủ tương phản). Màu nhấn = điều quan trọng nhất của câu (tên, con số, động từ chính).
- `accent2` cho chi tiết phụ: thanh dưới tiêu đề, phụ đề nhỏ, nhãn năm, dòng nguồn.
- Không dùng quá 3 màu chữ trong một khung. Không tô màu cả câu.

## 6. Bố cục và vùng an toàn
- Vùng an toàn 10%: phụ đề và lower third nằm trong lề 192 px ngang, 108 px dọc (`.safe`).
- Tiêu đề giữa khung; phụ đề ý góc dưới trái; nhãn bản đồ cạnh điểm, không đè tuyến; ghi công góc dưới phải, nhỏ.
- Quy tắc một tiêu điểm: mỗi khung chỉ một chỗ mắt cần nhìn. Có chữ lớn thì nền tối/mờ đi.
- Không đặt chữ lên mặt người hoặc chi tiết đang được kể.

## 7. Hiệu ứng hình và màu (tự theo thể loại, chỉnh bằng `style`)
| Lớp | Khóa `style` | Dùng để |
|---|---|---|
| Màu phim (grade) | `grade` (CSS filter) + `tint` (lớp tông soft-light) | Thống nhất ảnh từ nhiều nguồn thành một thế giới |
| Hạt film | tự có | Ảnh lưu trữ có kết cấu, khung không "chết" |
| Nhấp nháy | `flicker` (0–0,05) | Cảm giác máy chiếu phim cũ |
| Rung khung | `weave` (0–1,2) | Phim tư liệu |
| Bụi bay | tự có | Chuyển động nền liên tục |
| Vệt sáng (light leak) | tự có, nhẹ | Ấm, ký ức |
| Viền tối (vignette) | tự có | Kéo mắt vào giữa |

Lưu ý kỹ thuật: HyperFrames cảnh báo khi > ~40 lớp nặng (blur, radial-gradient, clip-path) trong một composition; khi vượt, tách cảnh ra composition riêng.

## 8. Âm thanh (tự gắn, chỉnh bằng khóa cảnh)
| Lớp | Cách kit làm | Khóa / tệp |
|---|---|---|
| Giọng đọc | Track 0, to nhất | `voice` (đường dẫn), `voice_start` |
| Nhạc nền | Tự hạ còn 0,35 khi có lời (ducking) | `music`, `music_volume`, `voice_regions` [[từ,đến],…] |
| Whoosh | whip, wipe, iris, cụm triptych | `motion-kit/sfx/whoosh*.mp3` |
| Impact | flash, stat `big`, cao trào | `impact-bass-*.mp3` |
| Land | tiêu đề đáp | theo thể loại |
| Pop / ping / chime | điểm bản đồ, mốc thời gian, số | theo thể loại |
| Gõ phím | typewriter | `typing.mp3`, `key-press.mp3` |
| Riser → impact | `payoff: true`, một lần mỗi cao trào | `riser.mp3` |

Đỉnh tiếng rơi sau hình 1 khung; xoay 2–3 bản cùng loại; ≤ 15 SFX/phút; cuối cùng `finish` đưa về −14 LUFS, đỉnh −1 dBTP. Tiếng thêm vào chỉ được lấy từ nguồn CC0, CC BY hoặc Pixabay License và ghi vào `motion-kit/sfx/CREDITS.md`.

## 9. Kết hợp mẫu (một nhịp = một tổ hợp)
| Nhịp | Tổ hợp |
|---|---|
| Hook mở đầu | `title` + letterbox + blurword + land → `photo` punch vào chi tiết + whoosh |
| Giới thiệu nhân vật | `photo` push + `lower` (tên / vai trò) |
| Hành trình | whip → `map` route vẽ dần + pop mỗi địa điểm → `stat` khoảng cách |
| Bằng chứng | dip → `document` + tô 1–2 dòng → `quote` typewriter |
| So sánh | wipe → `split` hai năm |
| Cao trào | `stat` big + payoff (riser→impact) → dip → `quote` ngắn |
| Kết chương | `photo` pull + dissolve + nhạc lên lại |
