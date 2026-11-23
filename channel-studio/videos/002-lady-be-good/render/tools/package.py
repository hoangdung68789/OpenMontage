"""Gói đăng 002: title.txt, description.md, tags.txt, hashtags.txt, i18n.json (theo references/publish-package.md).
Chạy: PYTHONUTF8=1 python channel-studio/videos/002-lady-be-good/render/tools/package.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from beats import BEATS, MUSIC, PHOTOS  # noqa: E402

ROOT = HERE.parents[4]
PKG = HERE.parents[1] / "package"
TL = json.loads((HERE.parent / "timeline.json").read_text(encoding="utf-8"))
MAN = {x["file"]: x for x in json.loads((ROOT / "projects/lady-be-good/assets/images/commons/_manifest.json").read_text(encoding="utf-8"))}

TITLE = "The Bomber the Desert Swallowed: Lady Be Good"
ALT = ["Lady Be Good: The WWII Bomber Found in the Sahara 15 Years Later",
       "Nine Men, One Bomber, and the Desert That Hid Them"]
SUMMARY = ("In 1958, oil prospectors flying over the Libyan Desert spotted an American B-24 bomber lying on the open sand, "
           "hundreds of miles from where anyone thought it could be. Lady Be Good had vanished on her first mission in April 1943 "
           "with nine men aboard. This is how she got there, what her crew did next, and what the searchers found, "
           "told from U.S. Air Force, National Archives and Air & Space Forces Magazine records.")
CH_NAMES = ["Intro: a bomber where none should be", "The new crew", "Naples, 4 April 1943", "Flying past home",
            "Into the dark", "The diary", "Found", "What the desert kept"]
SOURCES = [
    ("National Museum of the U.S. Air Force, \"Lady Be Good\" fact sheet", "https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196178/"),
    ("U.S. National Archives, The Unwritten Record, \"Lost and Found: The Story of 'Lady Be Good' and Her Crew\"", "https://unwritten-record.blogs.archives.gov/?p=15424"),
    ("Air & Space Forces Magazine, \"Lady Be Good\" (February 2014)", "https://www.airandspaceforces.com/article/0214lady/"),
    ("Shaw Air Force Base, \"The first, last and only flight of Lady Be Good\"", "https://www.shaw.af.mil/News/Article-Display/Article/214791/the-first-last-and-only-flight-of-lady-be-good/"),
    ("Wikipedia, \"Lady Be Good (aircraft)\"", "https://en.wikipedia.org/wiki/Lady_Be_Good_(aircraft)"),
]
ACCESSED = "November 22, 2026"
TAGS = ["Lady Be Good", "B-24 Liberator", "WWII mystery", "Libyan Desert", "lost bomber", "World War 2 history",
        "376th Bomb Group", "Sahara", "aviation mystery", "survival story", "Operation Climax", "history documentary",
        "unsolved mysteries", "WW2 aviation"]
HASH = ["#history", "#ww2", "#mystery"]


def mmss(t):
    t = int(t)
    return f"{t // 3600}:{t // 60 % 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def used_photos():
    keys = set()
    for _, beats in BEATS.items() if isinstance(BEATS, dict) else []:
        for _, p in beats:
            if p.get("k") == "photo":
                keys.add(p["img"])
    return [k for k in PHOTOS if k in keys] or list(PHOTOS)


def tail():
    """Phần không dịch: chương, nguồn, ghi công (giữ tiếng Anh ở mọi bản dịch để ghi công CC BY luôn hiện)."""
    out = ["CHAPTERS"]
    for c, name in zip(TL["chapters"], CH_NAMES):
        out.append(f"{mmss(0 if c['num'] == 0 else c['start'])} {name}")
    # anh chốt 23/11: mô tả không liệt kê nguồn, ghi công ảnh public domain hay cách làm video (vẫn lưu ở render/tools)
    lic = {MAN[PHOTOS[k]["file"]]["license"] for k in used_photos()}
    assert lic == {"Public domain"}, lic  # ảnh public domain không bắt buộc ghi công; ảnh CC BY thì phải thêm lại dòng ghi công
    names = ", ".join(f"\"{t.removesuffix('.mp3').replace('_', ' ')}\"" for t in dict.fromkeys(m[0] for m in MUSIC))
    # anh chốt 23/11: chỉ 1 dòng nguồn tổng hợp (tên, không link); bỏ Wikipedia vì không phải nguồn gốc
    out += ["", "Sources: " + ", ".join(dict.fromkeys(n.split(",")[0].split(" \"")[0] for n, _ in SOURCES if "Wikipedia" not in n)) + "."]
    out += [f"Music: {names} by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0 "
            "(http://creativecommons.org/licenses/by/4.0/)",  # giấy phép CC BY bắt buộc ghi công nhạc
            "", " ".join(HASH)]
    return "\n".join(out)


I18N = {
    "vi": ("Chiếc oanh tạc cơ bị sa mạc nuốt chửng: Lady Be Good",
           "Năm 1958, nhóm thăm dò dầu bay qua sa mạc Libya phát hiện một chiếc oanh tạc cơ B-24 của Mỹ nằm trên cát, cách xa mọi nơi người ta nghĩ nó có thể ở. Lady Be Good mất tích trong phi vụ đầu tiên vào tháng 4/1943 cùng 9 người. Đây là câu chuyện vì sao nó ở đó, tổ bay đã làm gì và đội tìm kiếm đã thấy gì, theo hồ sơ Không quân Mỹ, Cục Lưu trữ Quốc gia Mỹ và tạp chí Air & Space Forces."),
    "es": ("El bombardero que se tragó el desierto: Lady Be Good",
           "En 1958, unos prospectores de petróleo que sobrevolaban el desierto de Libia vieron un bombardero estadounidense B-24 sobre la arena, a cientos de millas de donde nadie creía que pudiera estar. Lady Be Good desapareció en su primera misión en abril de 1943 con nueve hombres a bordo. Así llegó allí, esto hizo su tripulación y esto encontraron los equipos de búsqueda, según registros de la Fuerza Aérea de EE. UU., los Archivos Nacionales y Air & Space Forces Magazine."),
    "pt-BR": ("O bombardeiro que o deserto engoliu: Lady Be Good",
              "Em 1958, prospectores de petróleo sobrevoando o deserto da Líbia avistaram um bombardeiro americano B-24 na areia, a centenas de milhas de onde alguém imaginaria. O Lady Be Good desapareceu em sua primeira missão, em abril de 1943, com nove homens a bordo. Veja como ele chegou lá, o que a tripulação fez e o que as buscas encontraram, segundo registros da Força Aérea dos EUA, do Arquivo Nacional e da Air & Space Forces Magazine."),
    "hi": ("रेगिस्तान में गुम बमवर्षक: लेडी बी गुड",
           "1958 में लीबिया के रेगिस्तान के ऊपर उड़ रहे तेल खोजकर्ताओं ने रेत पर पड़ा एक अमेरिकी B-24 बमवर्षक देखा, जहाँ उसके होने की किसी को उम्मीद नहीं थी। लेडी बी गुड अप्रैल 1943 में अपने पहले मिशन पर नौ लोगों के साथ लापता हो गया था। यह कहानी है कि वह वहाँ कैसे पहुँचा, चालक दल ने आगे क्या किया और खोज दलों को क्या मिला — अमेरिकी वायुसेना, नेशनल आर्काइव्स और Air & Space Forces Magazine के रिकॉर्ड के आधार पर।"),
    "id": ("Pengebom yang Ditelan Gurun: Lady Be Good",
           "Pada 1958, para pencari minyak yang terbang di atas Gurun Libya melihat sebuah pengebom B-24 Amerika tergeletak di pasir, ratusan mil dari tempat yang dikira siapa pun. Lady Be Good hilang dalam misi pertamanya pada April 1943 dengan sembilan awak. Inilah bagaimana pesawat itu sampai di sana, apa yang dilakukan awaknya, dan apa yang ditemukan tim pencari, berdasarkan catatan Angkatan Udara AS, Arsip Nasional AS, dan Air & Space Forces Magazine."),
    "fr": ("Le bombardier avalé par le désert : Lady Be Good",
           "En 1958, des prospecteurs pétroliers survolant le désert libyen aperçoivent un bombardier américain B-24 posé sur le sable, à des centaines de kilomètres de l'endroit où on l'imaginait. Lady Be Good avait disparu lors de sa première mission en avril 1943 avec neuf hommes à bord. Voici comment il est arrivé là, ce qu'a fait l'équipage et ce qu'ont trouvé les recherches, d'après les archives de l'US Air Force, des Archives nationales américaines et d'Air & Space Forces Magazine."),
    "de": ("Der Bomber, den die Wüste verschluckte: Lady Be Good",
           "1958 entdeckten Ölsucher über der Libyschen Wüste einen amerikanischen B-24-Bomber im offenen Sand, Hunderte Meilen von dort, wo man ihn vermutet hätte. Die Lady Be Good war im April 1943 auf ihrem ersten Einsatz mit neun Mann an Bord verschwunden. So kam sie dorthin, das tat ihre Besatzung, und das fanden die Suchtrupps – nach Unterlagen der US Air Force, des US-Nationalarchivs und des Air & Space Forces Magazine."),
    "ja": ("砂漠に呑まれた爆撃機：レディ・ビー・グッド",
           "1958年、リビア砂漠の上空を飛んでいた石油探査隊が、砂の上に横たわるアメリカのB-24爆撃機を発見しました。誰も想像しなかった場所でした。レディ・ビー・グッドは1943年4月、初任務で9人の搭乗員とともに消息を絶っていました。なぜそこにあったのか、搭乗員は何をしたのか、捜索隊は何を見つけたのかを、米空軍・米国国立公文書館・Air & Space Forces Magazineの記録からたどります。"),
    "ko": ("사막이 삼킨 폭격기: 레이디 비 굿",
           "1958년, 리비아 사막 상공을 비행하던 석유 탐사대가 모래 위에 놓인 미군 B-24 폭격기를 발견했습니다. 아무도 예상하지 못한 곳이었습니다. 레이디 비 굿은 1943년 4월 첫 임무에서 승무원 9명과 함께 실종됐습니다. 폭격기가 어떻게 그곳에 갔는지, 승무원들은 무엇을 했는지, 수색대는 무엇을 찾았는지 미 공군, 미 국립문서보관소, Air & Space Forces Magazine 기록으로 따라갑니다."),
    "ar": ("القاذفة التي ابتلعتها الصحراء: ليدي بي غود",
           "في عام 1958، رصد منقبون عن النفط يحلّقون فوق الصحراء الليبية قاذفة أمريكية من طراز B-24 ملقاة على الرمال، على بعد مئات الأميال من أي مكان توقّعه أحد. اختفت ليدي بي غود في مهمتها الأولى في أبريل 1943 وعلى متنها تسعة رجال. هذه قصة كيف وصلت إلى هناك، وماذا فعل طاقمها، وماذا وجدت فرق البحث، استنادًا إلى سجلات سلاح الجو الأمريكي والأرشيف الوطني الأمريكي ومجلة Air & Space Forces."),
}

PKG.mkdir(parents=True, exist_ok=True)
t = tail()
desc = SUMMARY + "\n\n" + t
assert len(TITLE) <= 70 and len(desc.encode("utf-8")) < 5000, (len(TITLE), len(desc.encode("utf-8")))
(PKG / "title.txt").write_text(TITLE + "\n", encoding="utf-8")  # yt_publish.py đọc cả file làm tiêu đề
(PKG / "title_alt.txt").write_text("\n".join(ALT) + "\n", encoding="utf-8")
(PKG / "description.md").write_text(desc + "\n", encoding="utf-8")
(PKG / "tags.txt").write_text(", ".join(TAGS) + "\n", encoding="utf-8")
(PKG / "hashtags.txt").write_text(" ".join(HASH) + "\n", encoding="utf-8")
i18n = {}
for lang, (ti, su) in I18N.items():
    d = su + "\n\n" + t
    assert len(ti) <= 100 and len(d.encode("utf-8")) < 5000, (lang, len(d.encode("utf-8")))
    i18n[lang] = {"title": ti, "description": d}
(PKG / "i18n.json").write_text(json.dumps(i18n, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(desc.encode("utf-8")), "byte mô tả;", len(used_photos()), "ảnh;", len(i18n), "bản dịch")
