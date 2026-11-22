# Quét 12 nhóm chủ đề kể chuyện (22/11/2026)

**Cách quét:** script `story_scan.py` (trong skill). Mỗi nhóm tìm 2 từ khóa trên YouTube, chỉ tính video dài từ 8 phút trở lên, lấy 10 kênh có video nhiều view nhất, rồi đo 60 video gần nhất của mỗi kênh.

**Hạn chế:**
- Tìm theo từ khóa nên mỗi nhóm lẫn cả kênh lớn không đúng chủ đề (ví dụ nhóm "space" có Dhruv Rathee và ColdFusion).
- View đã được YouTube làm tròn, ngày đăng là gần đúng.
- Số liệu thô: `story_scan.json`.

## Bảng tổng
| Nhóm | Trung vị view 10 video gần nhất | % video ≥ 3× trung vị kênh | Số kênh có video viral | Thời lượng trung vị (phút) |
|---|---|---|---|---|
| space_missions | 522K | 10% | 4/9 | 22 |
| exploration_survival | 492K | 12% | 4/9 | 29 |
| ancient_myth | 478K | 16% | 9/10 | 54 |
| disasters_engineering | 372K | 16% | 5/9 | 31 |
| business_stories | 328K | 12% | 4/10 | 23 |
| war_history | 252K | 15% | 7/10 | 44 |
| espionage_coldwar | 195K | 16% | 8/10 | 42 |
| history_mysteries | 176K | 10% | 6/10 | 37 |
| biographies | 120K | 19% | 8/10 | 53 |
| heists_scams | 84K | 17% | 6/10 | 38 |
| medieval_empires | 76K | 14% | 6/9 | 47 |
| true_crime | 54K | 11% | 7/10 | 44 |

## Kênh kể chuyện độc lập đáng tham chiếu
Đã loại kênh của hãng truyền hình và kênh phát lại phim.

| Kênh | Sub | Trung vị view 10 video gần nhất | Thể loại |
|---|---|---|---|
| **Yesterday** (dưới 24 tháng tuổi) | 169K | 579K | Lịch sử và khoa học dạng "Most terrifying… / Finally explained / Why did…", 26–41 phút |
| Mustard | 2,4M | 4,7M | Lịch sử quân sự, kỹ thuật |
| Wendigoon | 4,8M | 2,1M | Bí ẩn, chuyện kỳ dị |
| Miniminuteman | 3,5M | 1,7M | Khảo cổ, bác bỏ lịch sử giả, Franklin Expedition |
| BobbyBroccoli | 815K | 1,3M | Câu chuyện kinh doanh, chính trị |
| Mujin | 773K | 1,1M | Bê bối doanh nghiệp |
| Brick Immortar | 403K | 879K | Thảm họa hàng hải |
| Real Time History | 770K | 801K | Chiến tranh |
| Battle Guide | 512K | 682K | Trận đánh |
| Scary Interesting | 2,1M | 651K | Mất tích, sinh tồn |
| Dark Records | 656K | 372K | Thảm họa |
| Adventures Gone Wrong | 140K | 203K | Sinh tồn, thám hiểm |

**Video gần đây của Yesterday:**
- Mariana Trench: 2,8M view
- 9/11 conspiracies: 2,3M
- Arctic mystery: 1,5M
- Korean War: 1,0M
- Survival story: 1,0M
- Titanic: 769K
- Medicine history: 383K

## Chính sách quảng cáo ([Advertiser-friendly content guidelines](https://support.google.com/youtube/answer/6162278?hl=en), đọc ngày 22/11/2026)
- **"Can earn ad revenue"** (bật quảng cáo đầy đủ) gồm nội dung giáo dục và lịch sử:
  - Thi thể không ghê rợn, hoặc thi thể xuất hiện trong sự kiện lịch sử như chiến tranh.
  - Đưa tin về thảm kịch có người chết nhưng không hoặc ít hiển thị cảnh bạo lực. **Trường hợp này loại trừ các sự kiện nhạy cảm như xả súng hàng loạt và khủng bố.**
  - Ngụ ý khoảnh khắc tử vong trong bối cảnh phim tài liệu.
- **"Limited ad earnings"** (quảng cáo hạn chế): thi thể có vết thương rõ ràng, kể cả trong video giáo dục.
- **Hệ quả cho kênh:**
  - Chiến tranh, thảm họa, sinh tồn đều làm được, với điều kiện không có hình ảnh ghê rợn.
  - Tránh chủ đề khủng bố và xả súng hàng loạt.
