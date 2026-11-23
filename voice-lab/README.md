# voice-lab — VoiceStudio + OmniVoice trên máy anh Dũng

Cài 23/11/2026 theo yêu cầu anh: "cài repo vào OpenMontage ... Dùng repo voice studio để clone lại voice mà tôi đã chốt".

| Thư mục | Là gì | Giấy phép |
|---|---|---|
| `VoiceStudio/` (submodule, debpalash/VoiceStudio) | Ứng dụng giọng nói chạy trên máy; dùng phần backend Python + engine | Mã AGPL-3.0 |
| `OmniVoice/` (submodule, k2-fsa/OmniVoice) | Mã model OmniVoice | Mã Apache-2.0; **trọng số CC-BY-NC, cấm dùng thương mại** |
| `clone-algenib/` | Script clone giọng Algenib bằng engine VoxCPM2 của VoiceStudio | Trọng số `openbmb/VoxCPM2` Apache-2.0 |

## Vì sao dùng VoxCPM2, không dùng OmniVoice

- Trang model `k2-fsa/OmniVoice`: "The pre-trained model is licensed under the CC-BY-NC". VoiceStudio cũng ghi `commercial_use: false` (`VoiceStudio/backend/config/model_licenses.json`).
- Kênh ICYFOX bật kiếm tiền nên chỉ dùng engine có trọng số cho phép thương mại. Trong danh sách engine của VoiceStudio, VoxCPM2 (Apache-2.0) clone được giọng và chạy CUDA trên Windows.

## Cài lại từ đầu (máy mới)

```bash
git submodule update --init voice-lab/VoiceStudio voice-lab/OmniVoice
cd voice-lab/VoiceStudio && uv sync --frozen --group cuda && uv pip install "voxcpm>=2.0.3"
```

Không chạy lệnh cài `irm ... | iex` trên trang VoiceStudio (tải và chạy ngay script từ mạng).

## Clone giọng

```bash
# 1. Mẫu giọng ~15 s + lời đọc khớp (đã có sẵn algenib_ref.txt; file .wav không đẩy git)
python voice-lab/clone-algenib/make_ref.py <S0.1.wav của 002> voice-lab/clone-algenib
# 2. Đọc một đoạn kịch bản bằng giọng clone
voice-lab/VoiceStudio/.venv/Scripts/python.exe voice-lab/clone-algenib/clone_voxcpm2.py <script.json> <mã đoạn>
```

Lần đầu tải trọng số VoxCPM2 (vài GB) vào bộ nhớ đệm Hugging Face.

## Luật dùng

- Một video chỉ dùng một model giọng. Video 002 đã đọc bằng Gemini 3.1 Algenib nên giữ nguyên.
- Giọng clone chỉ dùng cho video mới, khi anh nghe và chốt bản mẫu.
- Điều khoản Gemini API cấm "replicate any component of the Services". Việc clone giọng Algenib có thể bị coi là sao chép một thành phần [Chưa xác minh]. Chưa đăng giọng clone lên kênh khi chưa rõ điểm này.
