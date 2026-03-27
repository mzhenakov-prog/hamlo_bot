import requests
import time
import random
import os

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
API = f"https://api.telegram.org/bot{TOKEN}"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def kb():
    return {"keyboard": [["🤬 Хам","🤡 Гопник","🧠 Циник"],["😢 Депрессивный","📝 Поэт","📊 Статистика"],["💢 Оскорбить","🗑 Очистить","❓ Помощь"]],"resize_keyboard":True}

def send(cid, txt, k=None):
    try:
        d = {"chat_id": cid, "text": txt}
        if k:
            d["reply_markup"] = k
        requests.post(f"{API}/sendMessage", json=d)
    except:
        pass

def up(off=None):
    p = {"timeout": 25}
    if off:
        p["offset"] = off
    try:
        r = requests.get(f"{API}/getUpdates", params=p)
        return r.json().get("result", [])
    except:
        return []

def ai(msg, mode):
    h = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    d = {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": f"Ты ХАМЛО {mode}. Отвечай коротко, с матом."}, {"role": "user", "content": msg}], "temperature": 0.9, "max_tokens": 80}
    try:
        r = requests.post(GROQ_URL, json=d, headers=h, timeout=15)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        return None
    except:
        return None

def fall(t, m):
    tl = t.lower()
    if m == "хам":
        if "привет" in tl:
            return "О, ещё один идиот. Чего припёрся?"
        if "как дела" in tl:
            return "Тебе-то какое дело, мудила?"
        return "Чё, язык проглотил?"
    if m == "гопник":
        if "привет" in tl:
            return "Слышь, братан, чё надо?"
        return "Чё сказал, петух?"
    if m == "циник":
        if "привет" in tl:
            return "О, ещё один идиот."
        return "Твоя тупость поражает."
    if m == "депрессивный":
        if "привет" in tl:
            return "Привет... Всё равно все умрём."
        return "Всё бессмысленно..."
    if m == "поэт":
        if "привет" in tl:
            return "Пришёл, идиот, опять / Чего тебе от меня надо?"
        return "Что сказать тебе, идиот? / Сам решай свои проблемы"
    return "Чё?"

def ins():
    return random.choice(["Ты тупой", "Твой мозг как IE", "Ты бесполезный"])

mode = {}
stat = {}
last = 0
print("ХАМЛО AI ЗАПУЩЕН")

while True:
    try:
        updates = up(last+1)
        for u in updates:
            last = u["update_id"]
            if "message" in u:
                m = u["message"]
                cid = m["chat"]["id"]
                uid = m["from"]["id"]
                txt = m.get("text", "")
                if not txt:
                    continue
                print(txt[:50])
                if uid not in mode:
                    mode[uid] = "хам"
                if uid not in stat:
                    stat[uid] = 0
                stat[uid] += 1
                
                if txt in ["🤬 Хам","Хам"]:
                    mode[uid] = "хам"
                    send(cid, "✅ ХАМ", kb())
                elif txt in ["🤡 Гопник","Гопник"]:
                    mode[uid] = "гопник"
                    send(cid, "✅ ГОПНИК", kb())
                elif txt in ["🧠 Циник","Циник"]:
                    mode[uid] = "циник"
                    send(cid, "✅ ЦИНИК", kb())
                elif txt in ["😢 Депрессивный","Депрессивный"]:
                    mode[uid] = "депрессивный"
                    send(cid, "✅ ДЕПРЕССИВНЫЙ", kb())
                elif txt in ["📝 Поэт","Поэт"]:
                    mode[uid] = "поэт"
                    send(cid, "✅ ПОЭТ", kb())
                elif txt in ["📊 Статистика","Статистика"]:
                    send(cid, f"Сообщений: {stat[uid]}", kb())
                elif txt in ["💢 Оскорбить","Оскорбить"]:
                    send(cid, ins(), kb())
                elif txt in ["🗑 Очистить","Очистить"]:
                    send(cid, "🗑 Очищено", kb())
                elif txt in ["❓ Помощь","Помощь"]:
                    send(cid, "ХАМЛО AI\nРежимы: Хам, Гопник, Циник, Депрессивный, Поэт\n@avgustc", kb())
                elif txt == "/start":
                    send(cid, "ХАМЛО AI готов! @avgustc", kb())
                else:
                    cur = mode.get(uid, "хам")
                    a = ai(txt, cur)
                    send(cid, a if a else fall(txt, cur), kb())
        time.sleep(0.3)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
