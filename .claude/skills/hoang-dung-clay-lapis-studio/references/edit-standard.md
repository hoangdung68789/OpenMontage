# Quy trình edit video đạt chuẩn: nghiên cứu (23/11/2026)

Anh yêu cầu: "trước khi làm hãy tìm hiểu rõ một quy trình edit video đạt chuẩn là gì, thế nào là đạt, toàn bộ cấu trúc và thành phần, cách dùng và cách kết hợp; đừng bị ràng buộc bởi chủ đề hay quy tắc nào".
Nguồn chia 3 loại:
- **[N]** nguồn ngành: blog của hãng phần mềm, trường dạy làm phim. Thường là kinh nghiệm thực hành, không phải tiêu chuẩn chính thức.
- **[Đ]** số đo trên phim thật: tài liệu kỹ năng của repo `hyperframes` mà anh đã gắn (`skills/hyperframes/references/*.md`, `skills/media-use/references/*.md`).
- **[K]** số đo trên kênh của anh và đối thủ: `channel-studio/research/2026-11-23-motion/`.

## 1. Bộ khung chuẩn của hậu kỳ (post-production)
| # | Công đoạn | Làm gì | Ra gì | Khi nào coi là xong |
|---|---|---|---|---|
| 1 | **Ingest và tổ chức** | Gom và đặt tên mọi tư liệu (giọng, ảnh, video, nhạc, hiệu ứng âm thanh), ghi nguồn và giấy phép | Thư mục tư liệu, bảng ghi công | Không còn file nào không rõ nguồn |
| 2 | **Assembly** | Ráp tư liệu tốt nhất theo thứ tự kịch bản [N] | Bản ráp thô | Có đủ từ đầu đến cuối |
| 3 | **Rough cut** | Tìm câu chuyện và nhịp [N] | Bản dựng thô | Mạch kể chạy, không thiếu đoạn |
| 4 | **Fine cut** | Canh từng cú cắt, đặt chính xác thời điểm và thời lượng từng cảnh [N] | Bản dựng tinh | Từng cắt có lý do |
| 5 | **Picture lock** | Đóng băng thời gian: không thêm, bớt, xê dịch cảnh [N] | Bản khóa hình, file timeline | Màu, âm thanh, đồ họa làm song song trên bản này |
| 6 | **Đồ họa động, VFX** | Chữ, bản đồ, sơ đồ, hiệu ứng | Lớp đồ họa | Đúng lời, đúng lúc, đọc được |
| 7 | **Màu** | Hiệu chỉnh (sửa) trước, tạo màu (look) sau [N] | Bản chỉnh màu | Các cảnh liền nhau khớp sáng, tương phản, độ bão hòa |
| 8 | **Âm thanh** | Làm sạch lời → nhạc nền → hiệu ứng âm thanh → không khí → trộn [N] | Bản trộn | Lời luôn rõ, đạt chuẩn độ lớn |
| 9 | **Xuất file và QC** | Kiểm kỹ thuật và kiểm cảm nhận [N] | File giao, báo cáo QC | Không còn lỗi P0 |
| 10 | **Giao** | Tiêu đề, mô tả, thumbnail, phụ đề, chương | Gói đăng | Đăng được |

**Điều cốt lõi:** khóa hình trước, rồi mới làm màu, âm thanh và đồ họa. Xê dịch một cảnh sau khi khóa là phải chỉnh lại cả âm thanh lẫn hiệu ứng [N]. Với video làm bằng code (HyperFrames), "khóa hình" là **khóa thời lượng từng cảnh theo giọng đọc thật**.

## 2. Thành phần của một video kể chuyện, cách dùng và cách kết hợp
### 2.1 Nhịp và cấu trúc
- **Hook:** cảnh đầu phải có nội dung ngay (`first_frame_empty` là lỗi, vì khung đầu cũng là thumbnail trên mạng xã hội) [Đ].
- **Thay đổi đọc được** (cắt, khung mới, chữ hiện, đường vẽ): đối thủ dùng ảnh tĩnh đổi hình mỗi 3,6–10,7 giây; ICYFOX 002 mất 16,7–25,7 giây [K]. Quá 3 giây không có gì đổi là "dead stretch" [Đ].
- **Đừng cắt cho có:** cảnh minh họa chỉ giúp giữ chân khi nó minh họa đúng điều lời đang nói. Cắt quá nhiều có thể làm giảm giữ chân [N, một thử nghiệm đơn lẻ].
- **Mỗi kiểu xử lý hình chỉ tươi khoảng 6 giây.** Kéo dài một đoạn bằng cách giữ hình hoặc đổi cách xử lý, không bằng cách làm tween chậm lại [Đ].
- **Pattern interrupt** (đổi khung, nhịp, âm thanh, kiểu đồ họa, địa điểm): các nguồn khuyên từ 10–20 giây đến 2–3 phút một lần, số liệu chưa kiểm chứng độc lập [N].

### 2.2 Máy quay (camera) [Đ]
- **Đẩy, kéo, lia, phóng (Ken Burns):** tween `scale` và `x`/`y` trên lớp bọc, không tween trực tiếp lên ảnh hay video.
- Máy quay hoặc màu tràn dùng ease hai đầu (`power2.inOut`). Thứ xuất hiện đáp xuống bằng đuôi dài (`expo.out`, `power4.out`). Phóng xuyên qua hoặc rời đi thì tăng tốc (`power3.in`). Dùng cùng một `power2.out` 0,5 giây cho mọi thứ thì trông như máy làm.
- Một cú di chuyển nhanh dài 0,3–0,6 giây, kèm nhòe chuyển động.
- Cú đẩy chậm trên nhịp nhạc êm: từ 1,0 lên 1,08.
- **Punch-in** (phóng gấp) là cú cắt bên trong cảnh. **Kéo nét** (focus rack): nét chuyển từ gần ra xa.
- Thứ thật sự chuyển động liên tục: video chạy, thế giới 3D quay, sân khấu nền xoay chậm 3–5 độ mỗi giây.

### 2.3 Chuyển cảnh [N + Đ]
- **Cắt thẳng** là mặc định, nên cắt khi hình đang chuyển động.
- **Hòa hình (dissolve):** thời gian trôi, chuyển nhẹ.
- **Wipe:** đổi địa điểm.
- **Whip pan:** năng lượng; nhòe ngang 0,13–0,3 giây, thứ mới đến hơi nhòe rồi nét lại trong 0,13 giây.
- **Match cut:** nối hai cảnh có cùng hình dạng, hướng chuyển động hoặc âm thanh.
- **J-cut, L-cut:** âm thanh đi trước hoặc đi sau hình.
- **Đo trên phim thật [Đ]:**
  - Một phim dùng 3–5 kiểu chuyển cảnh, mỗi kiểu phải có lý do trên hình.
  - Tối đa 1/3 số mối nối giữa các nhịp là cắt thẳng.
  - "Hai thế giới không bao giờ hòa vào nhau."
  - Dip cut: hình cũ tối đi khoảng 40% trong 3 khung rồi cắt, để cú cắt đọc như có chủ đích.
  - Iris mở hình tròn trong 0,15 giây. Một vật trên hình phóng to thành cả thế giới mới. Màu nền tràn thay đổi trong 0,4 giây.
- **Sai lầm phổ biến:** dùng hiệu ứng chuyển cảnh hào nhoáng chỉ vì nó đẹp [N].

### 2.4 Chữ: hiệu ứng, màu, bố cục [N + Đ]
- **Thứ bậc chữ** tạo bằng cỡ, độ đậm, màu, vị trí, tương phản, thời điểm và chuyển động. Nên dùng một họ chữ với nhiều độ đậm [N].
- **Vùng an toàn:** chữ cách mép khoảng 10%, vùng hành động khoảng 5% [N].
- **Cỡ:**
  - Tiêu đề 4–9% chiều cao khung. Dòng phụ 2,5–4%.
  - Chữ dưới 2,6% cạnh ngắn của khung là quá nhỏ [Đ].
- **Màu:**
  - Tương phản sáng tối là cơ bản. Nền rối thì dùng tấm lót hoặc lớp tối [N].
  - Chỉ một từ được tô màu nhấn, và từ đó phải mang ý nghĩa [Đ].
- **Chữ hiện ra [Đ]:** đổi kiểu trong cùng một phim, không phải lúc nào cũng mờ dần rồi trượt lên. Các kiểu đo được:
  - Từng từ nhòe 6 px rồi nét, cách nhau 0,067 giây.
  - Từng từ từ xám sang màu mực.
  - Cả dòng nhòe 8 px rồi nét.
  - Tên người hiện từng chữ cái, cách nhau 0,1 giây.
  - Một từ quay như máy đánh bạc.
- **Chữ đã đáp thì đứng yên tuyệt đối** [Đ]. Chuyển động chuyển sang máy quay hoặc nền. Tiêu đề cứ trôi hay phóng to mãi là dấu hiệu phim do máy làm.
- **Thời gian giữ chữ:** 0,5 giây cộng 0,3 giây mỗi từ. Rời đi nhanh hơn lúc vào 40–50%. Từ cách nhau 60–120 ms, chữ cái cách nhau 1 khung [Đ].
- **Lower third** (dòng tên dưới màn hình) [N]: thấp và nhỏ hơn tiêu đề, không che chủ thể, không dán sát mép, hiệu ứng không lấn át chữ.

### 2.5 Bố cục
- Một khung chỉ có một điểm nhìn chính [Đ, review.md]. Chủ thể phải tách khỏi nền.
- Kiểu bố cục hay dùng:
  - Toàn khung.
  - Ảnh in trên bàn có bóng đổ (kiểu hồ sơ).
  - Chia đôi để so sánh.
  - Ba ảnh (triptych).
  - Dòng thời gian.
  - Thẻ số liệu.
  - Bản đồ có nhãn.
  - Khung cinema (letterbox) cho khoảnh khắc lớn.
- **Kiểm ở bề rộng điện thoại** (360 px): chữ nào cũng phải đọc được [Đ].

### 2.6 Hiệu ứng hình và màu
- **Màu:** hiệu chỉnh (phơi sáng, cân trắng, khớp cảnh) trước, tạo look sau. LUT chỉ là điểm khởi đầu. Phim tài liệu thường giữ màu gần mắt nhìn [N].
- **Kết cấu (texture):**
  - Hạt film, viền tối (vignette), vệt sáng lọt (light leak), nhấp nháy phim cũ, rung khung nhẹ (gate weave).
  - Giữ ở 15–25% độ mờ. Ở 5% sẽ mất khi nén [Đ].
  - Gradient tuyến tính toàn màn trên nền tối bị vỡ dải khi nén H.264, nên dùng gradient tròn [Đ].
- **Có sẵn trong repo của anh:**
  - LUT: `teal-orange-blockbuster`, `bleach-bypass`, `film-fade`.
  - Lệnh `media-treatment` cho các kiểu xử lý: phim cũ, retro, camcorder.

### 2.7 Âm thanh [N + Đ]
- **Thứ tự:** lời trước (xương sống của bản trộn), nhạc nằm dưới, hiệu ứng điểm xuyết, không khí nằm thấp.
- **Ducking:** hạ nhạc khi có lời, xuống khoảng 0,3–0,4 [Đ] hoặc dùng tự động.
- **Hiệu ứng âm thanh:** ít và chính xác, mỗi tiếng có nguyên nhân trên hình [Đ]:
  - Whoosh cho cú cắt hoặc vật lớn chuyển động nhanh.
  - Pop cho số hay huy hiệu đáp xuống.
  - Tiếng gõ phím cho chữ hiện từng ký tự.
  - Riser dồn vào impact chỉ dùng **một lần** cho cao trào.
  - Xoay vòng 2–3 bản thu của cùng một tiếng (một whoosh lặp mãi là dấu hiệu máy làm).
  - Đặt đỉnh âm **sau** hình 1 khung.
  - Hiệu ứng cao hơn nhạc nền 3–6 dB.
- **Độ lớn:**
  - Cả bản trộn khoảng −14 LUFS (một số nguồn ghi −13 đến −15), đỉnh thật không quá −1 dBTP.
  - YouTube chỉ hạ tiếng quá to, không nâng tiếng nhỏ, và không sửa được bản trộn lệch [N].
  - Lời khoảng −18 đến −16 LUFS ngắn hạn [N].
  - Phần lớn năng lượng dưới 150 Hz thì loa điện thoại gần như không phát ra [Đ].

### 2.8 Thế nào là "đạt"
| Lớp | Đạt khi | Đo bằng |
|---|---|---|
| Kỹ thuật hình | Không khung trống, không vỡ dải, không giật, không chữ bị che | `npx hyperframes lint` + `check` |
| Chuyển động | Đứng yên ≤ 2%, không đoạn đứng yên ≥ 4 giây, phần gần như không đổi ≤ 25%; không "dead stretch" > 3 giây | `motion_metrics.py`, `check` |
| Chữ | Đủ giờ đọc (`line_unread`), cỡ ≥ 2,6%, tương phản WCAG AA, đọc được ở 360 px | `check`, `snapshot --review` |
| Nhịp và chuyển cảnh | 3–5 kiểu chuyển cảnh có lý do, tối đa 1/3 cắt thẳng, không hai mối nối liền nhau cùng kiểu | `icyfox_motion.py validate` |
| Âm thanh | Có tiếng; −14 ±1 LUFS; đỉnh thật ≤ −1 dBTP; hiệu ứng ≤ 15 tiếng/phút, mỗi tiếng có nguyên nhân | `finish` (loudnorm + đo) |
| Cảm nhận | Người lạ chỉ xem hình (che lời) vẫn hiểu mạch; không còn lỗi P0 | `REVIEW.md` theo P0/P1/P2 [Đ] |

**Dấu hiệu video do máy làm (tránh)** [Đ]:
- Mọi thứ mờ dần rồi trượt lên.
- Mọi cảnh vào cùng một kiểu.
- Tiêu đề cứ trôi hoặc phóng sau khi đã đáp.
- Lặp vòng "thở", "nổi" để giả chuyển động.
- Cùng một tiếng whoosh cho mọi cú cắt.
- Cùng một ease cho tất cả.

## 3. Nguồn đã đọc (tra 23/11/2026)
- Quy trình hậu kỳ:
  - [Vimeo: post-production workflow](https://vimeo.com/blog/post/post-production-workflow)
  - [Adobe: post production](https://www.adobe.com/creativecloud/video/discover/post-production.html)
  - [No Film School](https://nofilmschool.com/what-is-post-production)
  - [Videomaker](https://www.videomaker.com/?p=72001450)
  - [Boris FX](https://borisfx.com/blog/all-you-need-to-know-about-video-post-production/)
- Nhịp và giữ chân:
  - [PremiumBeat: cutting documentary](https://www.premiumbeat.com/blog/video-editing-tips-cutting-documentary/)
  - [AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8)
  - [Opus: B-roll test](https://www.opus.pro/blog/does-b-roll-increase-watch-time)
- Âm thanh:
  - [Descript: sound design](https://www.descript.com/blog/article/how-to-sound-design-a-youtube-video)
  - [Epidemic Sound: volume](https://epidemicsound.com/blog/how-to-get-the-volume-right-in-your-videos)
  - [Frame.io: audio mixing](https://blog.frame.io/2021/08/16/premiere-pro-audio-mixing-basics/)
- Chữ:
  - [School of Motion](https://www.schoolofmotion.com/blog/title-design-tips-after-effects-tips-for-video-editors)
  - [LibreTexts: titles and graphics](https://human.libretexts.org/Courses/City_College_of_San_Francisco/Video_Production_Handbook_I/16%3A_The_Finishing_Process/16.03%3A_Fixing_Titles_and_Graphics)
  - [Frame.io: lower thirds](https://blog.frame.io/?p=3992)
  - [Graduate School: typography](https://www.graduateschool.edu/learn/premiere-pro/typography-motion-design)
- Màu:
  - [Vimeo: grading vs correction](https://vimeo.com/blog/post/color-grading-vs-color-correction-explained)
  - [StudioBinder](https://www.studiobinder.com/blog/color-grading-vs-color-correction-process/)
- Chuyển cảnh:
  - [Adobe: types of film transitions](https://www.adobe.com/creativecloud/video/discover/types-of-film-transitions.html)
  - [Adobe: match cut](https://www.adobe.com/creativecloud/video/discover/match-cut.html)
- Số đo trên phim thật [Đ]:
  - `hyperframes/skills/hyperframes/references/`: `film.md`, `motion.md`, `look.md`, `sound.md`, `review.md`, `format.md`
  - `hyperframes/skills/media-use/references/`: `mixing.md`, `grading.md`, `sfx.md`
