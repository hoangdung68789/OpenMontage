# Đề xuất video thử số 1: Gilgamesh (chờ duyệt, 22/11/2026)

Quy trình: OpenMontage `animated-explainer`. Bước nghiên cứu đã xong.
Bản nghiên cứu: `/home/user/OpenMontage/projects/gilgamesh-pilot/artifacts/research_brief.json`

## 1. Nghiên cứu nói gì (tóm tắt)

- **Có nhu cầu, nhưng đã đông người làm.** Đã có nhiều video Gilgamesh đạt từ 1 triệu view:
  - TED-Ed 4,4M (5 phút)
  - The Histocrat 3,6M (132 phút)
  - CrashCourse 3,1M
  - Deep Dive History 1,28M (111 phút)
- **Khoảng trống.** Các bản kể hiện có đều coi văn bản là đã hoàn chỉnh. Thực tế văn bản vẫn đang được bổ sung:
  - 2014: mảnh Tablet V thêm khoảng 20 dòng, có khỉ trong Rừng Bá Hương và Enkidu hối hận vì phá rừng.
  - 2021: "Dream Tablet" bị cướp được trả về Iraq.
  - 2023: AI "Fragmentarium" của LMU ghép thêm 20 mảnh, bổ sung chi tiết cho hơn 100 dòng.
- **Ngộ nhận lan rộng.** Video thuyết âm mưu "Mỹ đánh Iraq để tìm mộ Gilgamesh" đạt 2,0M và 1,7M view. Thực tế năm 2003 chỉ phát hiện một dị thường từ trường, chưa hề đào lên.

## 2. Mood board

- Tham chiếu tông: *Fall of Civilizations*, ảnh di vật thật, nhịp kể chậm và có trọng lượng. Không theo kiểu "người ngoài hành tinh cổ đại".
- Hình mẫu: [Phù điêu "Hero mastering a lion", Louvre AO19862](https://commons.wikimedia.org/wiki/File:Hero_lion_Dur-Sharrukin_Louvre_AO19862.jpg) (Public domain)
- Bảng màu "Clay & Lapis":

  | Vai trò | Màu | Mã |
  |---|---|---|
  | Nền | Đen nhựa đường | `#1B1714` |
  | Chính | Đất nung | `#B5734A` |
  | Nhấn | Lapis | `#1F4E8C` |
  | Điểm sáng | Vàng | `#C9A54C` |

- Chữ: tiêu đề kiểu serif cổ điển, nhãn dùng sans gọn.
- Nhạc: ambient trầm, dàn dây và trống khung nhẹ, năng lượng thấp đến vừa.

## 3. Ba concept

| | **A. The Lost Lines** (đề xuất) | B. The Complete Epic | C. Slightly Wrong |
|---|---|---|---|
| Tiêu đề YouTube | The Epic of Gilgamesh, Complete: With the Lines We Only Just Found | The Complete Epic of Gilgamesh | Everything You Know About Gilgamesh Is Slightly Wrong |
| Hook (≤20 từ) | "Humanity's oldest epic is still missing pages. Looted tablets and an AI just gave some back." | "A king who was two-thirds god, a wild man made from clay, and one question: can anyone escape death?" | "Not the oldest story. Not simply copied by the Bible. And no, his tomb was never found." |
| Cấu trúc | Hành trình: kể trọn Tablet I → XI, xen các đoạn "dòng vừa tìm lại" và câu chuyện ai đã tìm ra chúng | Kể chuyện liền mạch, nhịp chậm, thuần cốt truyện | Phá ngộ nhận, 4 ngộ nhận |
| Thời lượng | 45 phút | 45 phút (sau này làm bản 2 giờ) | 30 phút |
| Vì sao hiệu quả | Lấp khoảng trống chưa ai làm, dựa trên 3 phát hiện 2014, 2021, 2023 | Định dạng "kể trọn" có điểm vượt trội cao nhất trong số liệu quét (trung vị 1,20) | Bám vào 2 video thuyết âm mưu đạt 2,0M và 1,7M view, có kiểm chứng (Lead Stories 2023) |
| Rủi ro | Nghiên cứu nặng hơn | Trùng với nhiều bản kể đã có | Ngắn hơn nên tích ít giờ xem hơn |

Có thể ghép, ví dụ hook của C cho phần mở của A.

## 4. Công cụ dựng: có 2 lựa chọn, cần anh chọn

Kiểm tra trên máy ngày 22/11/2026: HyperFrames **có sẵn**, Remotion **chưa cài** (cần `npm install`), ffmpeg có sẵn.

| | HyperFrames (đề xuất) | Remotion |
|---|---|---|
| Hợp với video này | Dựng bằng HTML và GSAP. Có kho khoảng 450 khối dựng sẵn (bản đồ, chữ động, chuyển cảnh). Hợp với bản đồ Lưỡng Hà động và hiệu ứng "dòng chữ hình nêm phát sáng" cho các dòng mới tìm lại | Bộ cảnh React dựng sẵn (thẻ chữ, thẻ số liệu, ảnh chuyển động kiểu Ken Burns) |
| Đánh đổi | Render 45 phút bằng trình duyệt không giao diện sẽ lâu trên máy này | Phải cài thêm. Cảnh dựng sẵn dễ ra "khuôn mẫu", mà khuôn mẫu là rủi ro chính sách nội dung rập khuôn của YouTube |

Phụ đề phát dưới dạng file .srt riêng, không in chữ lên hình, nên không cần tính năng phụ đề từng từ (vốn chỉ Remotion có).

**Cách dựng:** đề xuất **Atelier**, nghĩa là tự thiết kế hệ hình riêng cho video, không dùng cảnh mẫu có sẵn. Tốn công hơn, nhưng tạo được nhận diện riêng cho kênh và giảm rủi ro bị xem là nội dung rập khuôn.

## 5. Giọng đọc, hình ảnh, nhạc

| Hạng mục | Kế hoạch | Trạng thái |
|---|---|---|
| Giọng | `gemini_tts`, model `gemini-3.8-flash-tts`. Nghe thử 3 giọng, mỗi giọng 60 giây. Dự phòng: Piper chạy trên máy | Chờ khóa Gemini. Piper chưa cài |
| Hình | Ảnh di vật và địa danh từ Wikimedia (chỉ dùng Public domain, CC BY, CC BY-SA; ghi công đầy đủ), bản đồ động tự dựng, thẻ trích dẫn chữ hình nêm | Host đã mở, đã thử tìm "Gilgamesh relief": trả về ảnh kèm giấy phép |
| Không dùng | Ảnh của British Museum (giấy phép CC BY-NC-SA cấm mục đích thương mại), ảnh AI giả cảnh thật | |
| Minh họa cảnh truyện (tùy chọn) | Ảnh do Gemini tạo theo phong cách phù điêu Assyria, không giống thật | Chưa tra giá |
| Nhạc | `pixabay_music` (không cần khóa) | Host đã mở. Chưa xác minh khả năng bị Content ID nhận nhầm bản quyền |
| Phụ đề 11 ngôn ngữ | Tôi tự dịch | 0 USD |

## 6. Chi phí ước tính (bản Standard)

| Hạng mục | Cách tính | USD |
|---|---|---|
| Giọng đọc 45 phút | 2.700 giây × 25 token = 67.500 token × 9 USD/1M (giá 2026), hoặc 18 USD/1M (giá từ 01/01/2027) | 0,61 / 1,22 |
| Dự phòng đọc lại (+50%) | | 0,30 / 0,61 |
| Ảnh, nhạc, render, dịch | Nguồn miễn phí, chạy trên máy | 0 |
| **Tổng** | | **≈ 0,9–1,8** |

Trần ngân sách đề xuất: 5 USD.

Các phương án khác:
- **Miễn phí:** giọng Gemini gói miễn phí (hạn mức chưa rõ) hoặc Piper. Khoảng 0 USD.
- **Cao cấp:** thêm minh họa Gemini, cộng 1 bản đọc bằng người thật để so sánh. Chưa có giá.

## 7. Cần anh duyệt

```
Concept: A / B / C / ghép (ghi rõ)
Công cụ dựng: HyperFrames (đề xuất) / Remotion (cài thêm)
Cách dựng: Atelier (đề xuất) / dùng cảnh mẫu
Phương án: Standard (đề xuất) / Miễn phí
→ duyệt / duyệt kèm sửa / từ chối
```
