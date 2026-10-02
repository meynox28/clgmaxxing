import os, json, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TIMETABLE = {
    "Monday": [
        "9:30 CNS",
        "10:25 ML",
        "11:35 Next Gen Lab, Room 206 (till 1:25)",
        "2:15 RM",
        "3:10 ML",
        "4:05 TOC",
    ],
    "Tuesday": [
        "9:30 ML",
        "10:25 CNS",
        "11:35 FCG",
        "1:25 CG Lab, Room 210 (till 3:10)",
        "3:10 TOC",
        "4:05 FCG",
    ],
    "Wednesday": [
        "9:30 ML",
        "10:25 FCG",
        "11:35 TOC",
        "1:25 ML Lab, Room 305 (till 3:10)",
        "3:10 CNS",
    ],
    "Thursday": [
        "9:30 TOC",
        "10:25 FCG",
        "11:35 CNS",
        "12:30 EVS",
        "2:15 NPTEL / MOOC",
    ],
    "Saturday": [
        "9:30 PBL-MAD",
        "11:35 Pre-placement activity",
        "2:15 NSS / Yoga / Workshop / Cultural",
    ],
}

now = datetime.now(ZoneInfo("Asia/Kolkata"))
today = now.strftime("%A")

# Saturday classes only on the 2nd and 4th Saturday of the month
if today == "Saturday":
    saturday_number = (now.day - 1) // 7 + 1
    if saturday_number not in (2, 4):
        raise SystemExit("Off Saturday, nothing to send.")

classes = TIMETABLE.get(today, [])
text = f"**{today}**\n" + "\n".join(classes) if classes else f"No classes today ({today}) 🎉"

req = urllib.request.Request(
    os.environ["WEBHOOK_URL"],
    json.dumps({"content": text}).encode(),
    {"Content-Type": "application/json", "User-Agent": "clgmaxxing"},
)
urllib.request.urlopen(req)
