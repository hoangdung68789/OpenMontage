# S001 · Earth's Unsolved #1 · The Bloop (ĐÃ ĐĂNG CÔNG KHAI 24/11/2026 22:45, https://youtu.be/S3lpecq0QUg, thẻ T-048)

Chuỗi Shorts có chủ đề riêng "Earth's Unsolved" (anh chốt 23/11, xem decisions-log). Tập 1: âm thanh "Bloop" mà NOAA thu được năm 1997.

## Trạng thái
- [x] Kiểm dữ kiện từ trang NOAA (bên dưới). Kịch bản `script.md`, QA đạt (`script.qa.md`).
- [x] Tài nguyên: bảng giấy phép ở `CREDITS.md`. Loại phim bạch tuộc (khung cuối ghi "Footage: Ocean Exploration Trust", PD không chắc).
- [x] Lời đọc: clone Qwen3 "chậm + sáng" (`voice/B1–B6.wav`), ghép kèm tiếng Bloop thật ở `build/narration.wav` (59,88 s).
- [x] Dựng 1080×1920 HyperFrames: `build_index.py` → `render/index.html` (lint 0 lỗi, check đạt).
- [x] Render + đo: `render/final.mp4` 1080×1920, 59,9 s, −14,1 LUFS; `render/metrics.txt` static 0%, pct_still 1,7%, đổi hình 5,4 s; C2PA sạch; lưới `render/grid.jpg`. Lần 2 làm tối nền cảnh Nam Cực (chữ chìm trên băng trắng).
- [x] Gói đăng: `package/` (tiêu đề, mô tả có nguồn + ghi công, thẻ, phụ đề en/vi).
- [x] Đăng YouTube công khai ngay (`yt_publish.py upload --now`): video S3lpecq0QUg, `package/UPLOADED.txt`, đọc lại `package/READBACK.txt` (public, processed, phụ đề en+vi).

## Dữ kiện đã kiểm (đọc 23/11/2026)
| Dữ kiện | Nguồn |
|---|---|
| Năm 1997, khi nghe hoạt động núi lửa dưới biển ở nam Thái Bình Dương, các nhà nghiên cứu thu được một âm thanh lạ, mạnh, rất to | NOAA Ocean Facts https://oceanservice.noaa.gov/facts/bloop.html |
| Hydrophone (micro dưới nước) đặt cách nhau hơn 3.219 km (2.000 dặm) trên Thái Bình Dương | Như trên |
| Giả thuyết: diễn tập quân sự bí mật, động cơ tàu, tời tàu cá, mực khổng lồ, cá voi, sinh vật chưa biết | Như trên |
| Năm 2005 tìm ra nguồn khi đặt hydrophone gần Nam Cực hơn: icequake, tức một tảng băng nứt và tách khỏi sông băng Nam Cực | Như trên. PMEL dùng chữ "consistent with icequakes" |
| Đoạn âm thanh công bố đã được tăng tốc 16 lần | PMEL https://pmel.noaa.gov/acoustics/sounds/bloop.html |
| Icequake đủ mạnh để nhiều cảm biến cách xa hơn 5.000 km cùng thu được | Như trên |

Không dùng câu "to hơn cá voi xanh": NOAA không nói điều này.

## Kịch bản nháp (~95 từ, mục tiêu < 60 s)
> In 1997, the Pacific Ocean made a sound no one could explain. [pause]
> NOAA scientists were listening for underwater volcanoes. Microphones spread more than two thousand miles apart picked up the same powerful rumble. It became known as the Bloop.
> Here it is, sped up sixteen times. [pause, phát bloop.wav]
> The theories piled up. A secret military test. A ship's engine. A giant squid. Something unknown to science.
> For years, nobody knew. Then researchers moved their microphones closer to Antarctica, and in 2005 they found the source.
> The Bloop was an icequake: an iceberg cracking and breaking away from an Antarctic glacier.
> The monster was ice.

Chữ hook 3 giây đầu: "THE OCEAN MADE A SOUND NO ONE COULD EXPLAIN".

## Phân cảnh dự kiến (mọi cảnh đều chuyển động)
1. Biển sâu (sứa Marianas, NOAA PD) + chữ hook.
2. Bản đồ Thái Bình Dương: vòng sóng âm lan ra, nhãn "> 3,200 km apart" (không vẽ vị trí hydrophone cụ thể vì chưa có nguồn).
3. Phổ tần PMEL, vạch chạy theo tiếng Bloop thật.
4. Giả thuyết hiện lần lượt trên phim biển sâu (Bathynomus, NOAA PD).
5. Nam Cực: ảnh Landsat đẩy máy, băng trôi (NASA PD), sông băng vỡ (Margerie, CC BY 2.0, cần ghi công).
6. Kết: "The monster was ice." + thẻ "EARTH'S UNSOLVED #1".

Không dùng ảnh hay phim AI. Mô tả ghi 1 dòng "Sources: NOAA, NASA" và ghi công CC BY cho phim Margerie (luật không nhãn AI, luật mô tả gọn).
