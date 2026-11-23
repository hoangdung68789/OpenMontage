# Báo cáo lời đọc 002 (clone Algenib: Qwen3-TTS 1.7B Base, mẫu S0.1, nghỉ ×1,6, chậm + sáng; anh chọn 23/11)

- Tổng độ dài thật: **29:26** (kịch bản ước tính 27:29).
- Đoạn cần nghe lại (khớp < 90% hoặc thiếu): S1.1.
- Khớp = whisper small.en so với kịch bản. Whisper ghi số bằng chữ số ("12th", "1943") nên đoạn nhiều số sẽ bị tính lệch dù đọc đúng.

| Đoạn | Độ dài thật | Kịch bản | LUFS | Khớp % | Chỗ lệch (máy nghe) |
|---|---|---|---|---|---|
| S0.1 | 73.6 s | 71 s | -23.1 | 95.3 | delete: 'an' -> ''; delete: 'a' -> ''; replace: 'four hundred and forty' -> '440'; replace: 'be good' -> 'b goode'; replace: 'fifteen' -> '15' |
| S1.1 | 60.0 s | 57 s | -23.0 | 88.4 | delete: 'to' -> ''; replace: 'four hundred' -> '400'; replace: 'soluch' -> 'saluch'; replace: 'soluch' -> 'saluch'; replace: 'thirty four' -> '34'; replace: 'soluch' -> 'saluch'; replace: 'forty one twenty four three oh  |
| S1.2 | 73.6 s | 62 s | -23.1 | 95.6 | replace: 'd p' -> 'dp'; replace: 'woravka' -> 'worafka'; replace: 'lamotte' -> 'lamott'; replace: 'eighteenth' -> '18th'; replace: 'seventeen' -> '17' |
| S1.3 | 26.4 s | 27 s | -23.2 | 94.4 | replace: 'be good' -> 'b goode'; replace: 'fourth' -> '4th' |
| S2.1 | 46.0 s | 46 s | -22.6 | 92.0 | replace: 'fourth twenty five' -> '4th 25'; replace: 'twelve' -> '12'; replace: 'thirteen' -> '13'; replace: 'be good' -> 'b goode'; replace: 'soluch' -> 'solusz' |
| S2.2 | 35.7 s | 35 s | -23.1 | 98.5 | replace: 'soluch' -> 'soluc' |
| S2.3 | 45.1 s | 43 s | -23.2 | 95.4 | replace: 'be good' -> 'b goode'; replace: 'be good' -> 'b goode' |
| S2.4 | 30.8 s | 27 s | -22.8 | 100.0 |  |
| S3.1 | 57.8 s | 55 s | -23.1 | 99.5 | delete: 'a' -> '' |
| S3.2 | 57.3 s | 52 s | -22.6 | 93.1 | replace: 'be good' -> 'b goode'; replace: 'one hundred and fifty' -> '150'; replace: 'three hundred and thirty' -> '330' |
| S3.3 | 56.7 s | 57 s | -23.3 | 95.1 | delete: 'a' -> ''; replace: 'three hundred and thirty' -> '330'; replace: 'one hundred and fifty' -> '150' |
| S3.4 | 46.4 s | 48 s | -23.0 | 96.9 | replace: 'be good' -> 'b goode'; replace: 'ahead' -> 'head' |
| S4.1 | 51.0 s | 50 s | -23.3 | 98.5 | replace: 'on to' -> 'onto' |
| S4.2 | 59.4 s | 52 s | -22.6 | 96.2 | replace: 'be' -> 'b'; replace: 'plain' -> 'plane'; replace: 'the' -> 'and'; replace: 'woravka' -> 'wirafka' |
| S4.3 | 38.2 s | 34 s | -22.8 | 100.0 |  |
| S4.4 | 67.2 s | 56 s | -23.0 | 98.2 | delete: 'a' -> ''; replace: 'north west' -> 'northwest' |
| S5.1 | 63.0 s | 63 s | -23.2 | 96.1 | replace: 'north west' -> 'northwest'; replace: 'thirty five' -> '35'; replace: 'weighted' -> 'waded'; replace: 'sixteen' -> '16' |
| S5.2 | 67.4 s | 67 s | -22.9 | 95.1 | replace: 'north west' -> 'northwest'; replace: 'four hundred and forty' -> '440'; replace: 'south east' -> 'southeast'; replace: 'writing' -> 'riding' |
| S5.3 | 48.6 s | 47 s | -22.2 | 98.9 | replace: 'calanscio' -> 'calanchio' |
| S5.4 | 66.3 s | 59 s | -23.0 | 92.2 | replace: 'ninth' -> '9th'; replace: 'shelley' -> 'shelly'; replace: 'shelley' -> 'shelly'; replace: 'hays lamotte' -> 'hayes lamott'; replace: 'eighty' -> '80'; replace: 'seventy eight' -> '78'; replace: 'eighty five' -> |
| S5.5 | 53.3 s | 44 s | -23.1 | 95.2 | replace: 'be good' -> 'b goode'; delete: 'the twelfth of' -> ''; insert: '' -> '12th' |
| S5.6 | 58.0 s | 61 s | -22.8 | 99.2 | replace: 'seventeen' -> '17' |
| S5.7 | 48.4 s | 48 s | -22.6 | 94.2 | replace: 'shelley' -> 'shelly'; replace: 'moore' -> 'more'; replace: 'north west' -> 'northwest'; replace: 'be good' -> 'b goode' |
| S6.1 | 59.4 s | 58 s | -22.7 | 95.6 | replace: 'fifteen' -> '15'; replace: 'nineteen fifties' -> '1950s'; replace: 'south east' -> 'southeast'; replace: 'd'arcy' -> 'dirarchy' |
| S6.2 | 71.4 s | 65 s | -23.2 | 96.2 | replace: 'd'arcy' -> 'darcy'; replace: 'd p hays'' -> 'dp hayes'; delete: 'it' -> ''; replace: 'fourth' -> '4th' |
| S6.3 | 72.9 s | 65 s | -23.4 | 94.2 | replace: 'wheelus' -> 'wheelis'; replace: 'wheelus' -> 'wheelis'; replace: 'seventeenth' -> '17th'; replace: 'four hundred and fifty' -> '450'; replace: 'sixteen' -> '16'; replace: 'second' -> '2nd' |
| S6.4 | 56.3 s | 44 s | -22.7 | 93.5 | replace: 'eleventh' -> '11th'; replace: 'hays lamotte' -> 'hayes lamott'; replace: 'eighty one' -> '81'; replace: 'seventeen' -> '17' |
| S6.5 | 76.7 s | 68 s | -23.5 | 94.8 | replace: 'twelfth' -> '12th'; replace: 'seventeenth' -> '17th'; replace: 'forces' -> 'force's'; replace: 'thirty seven' -> '37'; replace: 'twenty six' -> '26'; replace: 'twelve' -> '12' |
| S7.1 | 64.8 s | 57 s | -23.0 | 95.5 | replace: 'forces' -> 'force's'; delete: 'a' -> ''; delete: 'a' -> ''; delete: 'a' -> ''; replace: 'be good a' -> 'b goode' |
| S7.2 | 63.0 s | 67 s | -23.1 | 95.8 | replace: 'be' -> 'b'; delete: 'a' -> ''; replace: 'wheelus' -> 'wheelis'; delete: 'a' -> ''; replace: 'fifty one' -> '51'; replace: 'lamotte' -> 'lamott' |
| S7.3 | 71.5 s | 64 s | -22.7 | 98.0 | replace: 'fourth' -> '4th'; replace: 'icyfox' -> 'icy fox' |
