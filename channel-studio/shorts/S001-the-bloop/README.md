# S001 · Earth's Unsolved #1 · The Bloop (đang làm, tạm dừng 23/11/2026 theo lời anh)

Chuỗi Shorts có chủ đề riêng "Earth's Unsolved" (anh chốt 23/11, xem decisions-log). Tập 1: âm thanh "Bloop" mà NOAA thu được năm 1997.

## Trạng thái
- [x] Kiểm dữ kiện từ trang NOAA (bên dưới).
- [x] Tìm tài nguyên: danh sách ở `assets_candidates.json` (giấy phép, tác giả, link Commons).
- [ ] Tải đủ phim. Đã tải: bloop.wav, phổ tần bloop.jpg (PMEL), ảnh Nam Cực (NASA Landsat, trang NOAA Ocean Facts), v0 Bathynomus. Còn 6 phim chưa tải. Bản tải nằm ở thư mục tạm, sẽ mất khi máy dọn; tải lại theo link trong `assets_candidates.json`.
- [ ] Lời đọc: clone Qwen3 "chậm + sáng" (`OpenMontage/voice-lab/clone-algenib/clone_algenib.py --engine qwen3 --gap-scale 1.6 --slow-bright --chunk`).
- [ ] Dựng 1080×1920 bằng HyperFrames. Đạt `motion_metrics.py` (đứng yên ≤ 2%, đổi hình 5–8 s). Chạy `c2pa_check.py`.
- [ ] Gói đăng, đăng theo lịch Shorts (từ 01/12).

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
