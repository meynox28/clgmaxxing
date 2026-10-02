import os, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TIMETABLE = {
    "Monday": [
        ("9:30", "CNS","CNS"),
        "10:25 ML",
        ("10:25", "ML", "ML"),
        ("11:35", "NEXTGEN", "Next Gen Lab, Room 206 (till 1:25)"),
        ("2:15", "RM", "RM"),
        ("3:10", "ML", "ML"),
        ("4:05", "TOC", "TOC"),
    ],
    "Tuesday": [
        ("9:30", "ML", "ML"),
        ("10:25", "CNS", "CNS"),
        ("11:35", "FCG", "FCG"),
        ("1:25", "CGLAB", "CG Lab, Room 210 (till 3:10)"),
        ("3:10", "TOC", "TOC"),
        ("4:05", "FCG", "FCG"),

    ],
    "Wednesday": [
        ("9:30", "ML", "ML"),
        ("10:25", "FCG","FCG"),
        ("11:35", "TOC","TOC")
        ("1:25", "ML Lab", "ML Lab, Room 305 (till 3:10)"),
        ("3:10", "CNS", "CNS"),
    ],
    "Thursday": [
        ("9:30", "TOC", "TOC"),
        ("10:25" ,"FCG","FCG"),
        ("11:35", "CNS", "CNS"),
        ("12:30", "EVS", "EVS"),
    ],
    "Saturday": [
        ("9:30", "PBL-MAD", "PBL-MAD"),
    ],
}
STICKERS = {
    "ML": "Cute Cartoon Valentine_ My Reaction!.jpeg",
    "CNS": "#pov_ io in matamatica#il mio gatto#io la mattina.jpeg",
    "TOC": "#barbie #Ai #fyp #sticker #meme.jpeg",
    "FCG": "10062799164863793.jpeg",
    "PBL-MAD": "325877723060680300.jpeg",
    "RM": "Idea sticker whatsapp 🫧🫧🫧.jpeg",
    "Next Gen Lab, Room 206 (till 1:25)": "25825397860260120.jpeg",
    "CG Lab, Room 210 (till 3:10)": "pookie 🎀.jpeg",
    "ML Lab, Room 305 (till 3:10)": "accha bhosdi.jpeg",
}

now = datetime.now(ZoneInfo("Asia/Kolkata"))
today = now.strftime("%A")

if today == "Saturday" and ((now.day - 1) // 7 + 1) not in (2, 4):
    raise SystemExit("Off Saturday, nothing to send.")

classes = TIMETABLE.get(today, [])
embeds, files = [], {}

for time, code, label in classes:
    embed = {"title": f"{time}  {label}", "color": 0x5865F2}
    filename = STICKERS.get(code)
    path = os.path.join("stickers", filename) if filename else None
    if path and os.path.exists(path):
        embed["thumbnail"] = {"url": f"attachment://{filename}"}
        if filename not in files:  # attach each file only once
            files[filename] = open(path, "rb")
    embeds.append(embed)

if not embeds:
    embeds = [{"title": "No classes today 🎉", "color": 0x57F287}]

r = requests.post(
    os.environ["WEBHOOK_URL"],
    data={"payload_json": json.dumps({"content": f"**{today}**", "embeds": embeds})},
    files={f"file{i}": (name, fh) for i, (name, fh) in enumerate(files.items())} or None,
    headers={"User-Agent": "timetable-bot"},
)
r.raise_for_status()
