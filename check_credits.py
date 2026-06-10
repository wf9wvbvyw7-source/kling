import os, json, requests
from datetime import datetime

SLACK = os.environ["SLACK_WEBHOOK"]

def get_credits(cookie):
    try:
        r = requests.get(
            "https://kling.ai/api/account/pointAndTicket",
            params={"caver": "2", "scope": "PERSONAL"},
            headers={
                "Cookie": cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Referer": "https://kling.ai/",
            },
            timeout=15
        )
        d = r.json()
        print(json.dumps(d, ensure_ascii=False)[:300])
        for path in [["data","coinBalance"],["data","credits"],["data","point"],["data","balance"]]:
            v = d
            for k in path:
                v = v.get(k) if isinstance(v, dict) else None
            if v is not None:
                return int(v)
        return None
    except Exception as e:
        print(e)
        return None

accounts, i = [], 1
while True:
    name = os.environ.get(f"ACCOUNT_{i}_NAME")
    cookie = os.environ.get(f"ACCOUNT_{i}_COOKIE")
    if not name or not cookie:
        break
    accounts.append({"name": name, "cookie": cookie, "warn": int(os.environ.get(f"ACCOUNT_{i}_WARN", 100))})
    i += 1

now = datetime.now().strftime("%d.%m.%Y %H:%M")
lines, warns = [f"📊 *Kling — {now}*\n"], []

for a in accounts:
    c = get_credits(a["cookie"])
    if c is None:
        lines.append(f"• *{a['name']}*: ❌ помилка")
        warns.append(f"• {a['name']}: не вдалось отримати кредити")
    else:
        emoji = "⚠️" if c < a["warn"] else "✅"
        if c < a["warn"]:
            warns.append(f"• {a['name']}: {c} кред. (поріг: {a['warn']})")
        lines.append(f"• *{a['name']}*: {emoji} {c:,} кредитів")

msg =
