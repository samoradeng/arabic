#!/usr/bin/env python3
"""
Jordanian Arabic Interactive Practice Tool
Spaced repetition flashcards, quizzes, conjugation drills, and conversation practice.
"""

import json
import random
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- Vocabulary Database ---

VOCAB_BY_DAY = {
    1: [
        ("مرحبا", "mar7aba", "Hello"),
        ("أهلا وسهلا", "ahla w sahla", "Welcome"),
        ("كيفك؟", "keefak?", "How are you? (m)"),
        ("الحمد لله", "il-7amdu lillah", "Thank God / Fine"),
        ("تمام", "tamaam", "Good / Perfect"),
        ("شو اسمك؟", "shu ismak?", "What's your name? (m)"),
        ("اسمي", "ismi", "My name is"),
        ("تشرفنا", "tsharrafna", "Pleased to meet you"),
        ("من وين إنت؟", "min wein inte?", "Where are you from?"),
        ("أنا من", "ana min", "I'm from"),
        ("صباح الخير", "9abaa7 il-kheir", "Good morning"),
        ("صباح النور", "9abaa7 in-noor", "Good morning (response)"),
        ("مساء الخير", "masa2 il-kheir", "Good evening"),
        ("مع السلامة", "ma3 is-salaame", "Goodbye"),
        ("يعطيك العافية", "ya36eek il-3aafye", "May God give you strength"),
        ("بحكي شوي عربي", "ba7ki shwayy 3arabi", "I speak a little Arabic"),
        ("بتعلم عربي", "bat3allam 3arabi", "I'm learning Arabic"),
        ("إن شاء الله", "inshaallah", "God willing"),
        ("والله", "wallah", "I swear / Really"),
        ("يلا", "yalla", "Let's go / Come on"),
        ("طيب", "6ayyib", "OK / Good"),
        ("يعني", "ya3ni", "It means / Like"),
    ],
    2: [
        ("عيلة", "3eile", "family"),
        ("أب / بابا", "ab / baaba", "father / dad"),
        ("أم / ماما", "umm / maama", "mother / mom"),
        ("أخ", "akh", "brother"),
        ("أخت", "ukht", "sister"),
        ("إبن", "ibin", "son"),
        ("بنت", "bint", "daughter / girl"),
        ("زوج", "zooj", "husband"),
        ("زوجة", "zooje", "wife"),
        ("كبير", "kbeer", "big"),
        ("صغير", "z-gheer", "small"),
        ("طويل", "6aweel", "tall / long"),
        ("حلو", "7ilu", "sweet / pretty"),
        ("منيح", "mnee7", "good"),
        ("عندي", "3indi", "I have"),
        ("ما عندي", "maa 3indi", "I don't have"),
        ("كتير", "kteer", "very / a lot"),
        ("شوي", "shwayy", "a little"),
        ("هاد", "haad", "this (m)"),
        ("بس", "bass", "but / only"),
        ("كمان", "kamaan", "also / too"),
    ],
    3: [
        ("واحد", "waa7ad", "one"),
        ("اثنين", "ithnein", "two"),
        ("ثلاثة", "thalathe", "three"),
        ("أربعة", "arba3a", "four"),
        ("خمسة", "khamse", "five"),
        ("عشرة", "3ashara", "ten"),
        ("عشرين", "3ishreen", "twenty"),
        ("مية", "miyye", "hundred"),
        ("اليوم", "il-yoom", "today"),
        ("بكرة", "bukra", "tomorrow"),
        ("إمبارح", "imbaarih", "yesterday"),
        ("الساعة", "is-saa3a", "the hour / clock"),
        ("و نص", "w nu99", "and half"),
        ("و ربع", "w rub3", "quarter past"),
        ("هلأ / هسا", "halla2 / hassa", "now"),
        ("بعدين", "ba3dein", "later"),
        ("إمتى؟", "imta?", "When?"),
        ("الجمعة", "ij-jum3a", "Friday"),
        ("كل يوم", "kull yoom", "every day"),
    ],
    4: [
        ("بروح", "baroo7", "I go"),
        ("باكل", "baakul", "I eat"),
        ("بشرب", "bashrab", "I drink"),
        ("بنام", "banaam", "I sleep"),
        ("بشتغل", "bashtaghil", "I work"),
        ("بحكي", "ba7ki", "I speak"),
        ("بفهم", "bafham", "I understand"),
        ("بعرف", "ba3rif", "I know"),
        ("بحب", "ba7ibb", "I love/like"),
        ("بشوف", "bashoof", "I see"),
        ("بقوم من النوم", "ba2oom min in-noom", "I wake up"),
        ("بطلع من البيت", "ba6la3 min il-beit", "I leave the house"),
        ("شو؟", "shu?", "What?"),
        ("مين؟", "meen?", "Who?"),
        ("وين؟", "wein?", "Where?"),
        ("ليش؟", "leish?", "Why?"),
        ("كيف؟", "keef?", "How?"),
        ("قديش؟", "2addeish?", "How much?"),
        ("ما بعرف", "maa ba3rif", "I don't know"),
        ("ما بفهم", "maa bafham", "I don't understand"),
    ],
    5: [
        ("أكل", "akil", "food"),
        ("خبز", "khubz", "bread"),
        ("رز", "ruzz", "rice"),
        ("لحمة", "la7me", "meat"),
        ("دجاج", "djaaj", "chicken"),
        ("منسف", "mansaf", "mansaf (national dish)"),
        ("شاي", "shaay", "tea"),
        ("قهوة", "2ahwe", "coffee"),
        ("ميّ", "mayy", "water"),
        ("بدي", "biddi", "I want"),
        ("ممكن", "mumkin", "Can I / possible"),
        ("لو سمحت", "law sama7t", "please / excuse me"),
        ("الحساب", "il-7saab", "the bill"),
        ("زاكي", "zaaki", "delicious"),
        ("تسلم إيديك", "tislam ideik", "Bless your hands"),
        ("صحتين", "9a7tein", "Bon appétit"),
        ("بدون", "bidoon", "without"),
        ("شو بتنصحني؟", "shu bitinsa7ni?", "What do you recommend?"),
    ],
    6: [
        ("يمين", "yameen", "right"),
        ("شمال", "shmaal", "left"),
        ("دغري", "dughri", "straight"),
        ("قريب", "2areeb", "near"),
        ("بعيد", "b3eed", "far"),
        ("هون", "hoon", "here"),
        ("لف يمين", "liff yameen", "turn right"),
        ("روح دغري", "roo7 dughri", "go straight"),
        ("تاكسي", "taksi", "taxi"),
        ("باص", "baa9", "bus"),
        ("شارع", "shaari3", "street"),
        ("مطعم", "ma63am", "restaurant"),
        ("صيدلية", "9aidaliyye", "pharmacy"),
        ("فندق", "fundu2", "hotel"),
        ("مطار", "ma6aar", "airport"),
        ("وقف هون", "wa22if hoon", "stop here"),
        ("غالي", "ghaali", "expensive"),
        ("قديش بدك؟", "2addeish biddak?", "How much do you want?"),
    ],
    8: [
        ("رحت", "ru7t", "I went"),
        ("إجيت", "ijeet", "I came"),
        ("أكلت", "akalt", "I ate"),
        ("شربت", "shribt", "I drank"),
        ("شفت", "shuft", "I saw"),
        ("حكيت", "7akeet", "I spoke/said"),
        ("اشتغلت", "ishtazhalt", "I worked"),
        ("اشتريت", "ishtareit", "I bought"),
        ("كان", "kaan", "was (he)"),
        ("كنت", "kunt", "was (I)"),
        ("إمبارح", "imbaarih", "yesterday"),
        ("الأسبوع الماضي", "il-usboo3 il-maa9i", "last week"),
        ("لما", "lamma", "when (past)"),
        ("وبعدين", "w ba3dein", "and then"),
        ("لأنه", "la2innu", "because"),
        ("من زمان", "min zamaan", "long time ago"),
    ],
    9: [
        ("سوق", "soo2", "market"),
        ("فلوس", "floos", "money"),
        ("دينار", "deenaar", "dinar"),
        ("غالي", "ghaali", "expensive"),
        ("رخيص", "rkhee9", "cheap"),
        ("أكبر", "akbar", "bigger"),
        ("أصغر", "azghar", "smaller"),
        ("أرخص", "arkha9", "cheaper"),
        ("أحسن", "a7san", "better"),
        ("بدور على", "badawwir 3ala", "I'm looking for"),
        ("آخر سعر", "aakhir si3r", "final price"),
        ("بأخده", "baakhdu", "I'll take it"),
        ("أحمر", "a7mar", "red"),
        ("أزرق", "azra2", "blue"),
        ("أبيض", "abya9", "white"),
        ("أسود", "aswad", "black"),
    ],
    10: [
        ("برأيي", "bira2yi", "in my opinion"),
        ("بفضل", "bfa99il", "I prefer"),
        ("صح", "9a7", "correct"),
        ("أكيد", "akeed", "of course"),
        ("معك حق", "ma3ak 7a22", "you're right"),
        ("مش بالضرورة", "mish bi9-9aroora", "not necessarily"),
        ("عادي", "3aadi", "normal / no big deal"),
        ("لازم", "laazim", "must / should"),
        ("مش لازم", "mish laazim", "not necessary"),
        ("على حسب", "3ala 7asab", "it depends"),
        ("يا ريت", "ya reit", "I wish"),
        ("الصراحة", "i9-9araa7a", "honestly"),
    ],
    12: [
        ("راس", "raas", "head"),
        ("عين", "3ein", "eye"),
        ("بطن", "ba6n", "stomach"),
        ("ظهر", "6ahur", "back"),
        ("بوجعني", "biwja3ni", "it hurts me"),
        ("صداع", "9udaa3", "headache"),
        ("حرارة", "7araara", "fever"),
        ("دوا", "dawa", "medicine"),
        ("حبوب", "7uboob", "pills"),
        ("مستشفى", "mustashfa", "hospital"),
        ("دكتور", "duktoor", "doctor"),
        ("ساعدوني", "saa3idooni", "help me"),
        ("حساسية", "7asaasiyye", "allergy"),
    ],
    13: [
        ("رح أروح", "ra7 aroo7", "I will go"),
        ("رح آكل", "ra7 aakul", "I will eat"),
        ("مش رح", "mish ra7", "won't"),
        ("الأسبوع الجاي", "il-usboo3 ij-jaay", "next week"),
        ("قريبا", "2areeban", "soon"),
        ("بدك تيجي؟", "biddak tiiji?", "Do you want to come?"),
        ("فاضي", "faa9i", "free (available)"),
        ("مشغول", "mashghool", "busy"),
        ("نتلاقى", "nitlaa2a", "we meet"),
        ("إن شاء الله مرة تانية", "inshaallah marra taanye", "another time, God willing"),
        ("بشوفك", "bshoofak", "I'll see you"),
    ],
    15: [
        ("إذا", "idha", "if (real)"),
        ("لو", "law", "if (hypothetical)"),
        ("يا ريت", "ya reit", "I wish"),
        ("بقدر", "ba2dar", "I can"),
        ("ما بقدر", "maa ba2dar", "I can't"),
        ("المفروض", "il-mafroo9", "supposed to / should"),
        ("حتى لو", "7atta law", "even if"),
    ],
    16: [
        ("يا زلمة", "ya zalame", "dude"),
        ("يا عمي", "ya 3ammi", "uncle / bro"),
        ("زي الزفت", "zay iz-zift", "terrible (lit: like tar)"),
        ("مية بالمية", "miyye bil-miyye", "100% / absolutely"),
        ("ما إلي خلق", "maa ili khul2", "I can't be bothered"),
        ("دمه خفيف", "dammu khafeef", "funny/likeable person"),
        ("فش", "fish", "there isn't"),
        ("خلص", "khala9", "done / enough"),
        ("مش معقول", "mish ma32ool", "unbelievable"),
        ("تكرم عينك", "tikram 3einak", "of course / gladly"),
        ("على راسي", "3ala raasi", "with pleasure"),
    ],
    20: [
        ("تفضل", "tfa99al", "please (come in/sit/eat)"),
        ("البيت بيتك", "il-beit beitak", "make yourself at home"),
        ("ما قصرت", "maa 2a99art", "you've been too kind"),
        ("بسم الله", "bismillah", "in the name of God"),
        ("ما شاء الله", "mashaallah", "God has willed it (admiration)"),
        ("الله يرحمه", "allah yir7amu", "God rest his soul"),
        ("الله يشفيه", "allah yishfeeh", "God heal him"),
        ("مبروك", "mabrook", "congratulations"),
        ("الله يبارك فيك", "allah ybaarik feek", "God bless you"),
        ("حرام عليك", "7araam 3aleik", "shame on you"),
    ],
}

CONJUGATION_DRILLS = {
    "راح - to go (present)": {
        "أنا": "بروح",
        "إنتَ": "بتروح",
        "إنتِ": "بتروحي",
        "هو": "بروح",
        "هي": "بتروح",
        "إحنا": "بنروح",
        "إنتو": "بتروحو",
        "هم": "بروحو",
    },
    "راح - to go (past)": {
        "أنا": "رحت",
        "إنتَ": "رحت",
        "إنتِ": "رحتي",
        "هو": "راح",
        "هي": "راحت",
        "إحنا": "رحنا",
        "إنتو": "رحتو",
        "هم": "راحو",
    },
    "أكل - to eat (present)": {
        "أنا": "باكل",
        "إنتَ": "بتاكل",
        "إنتِ": "بتاكلي",
        "هو": "بوكل",
        "هي": "بتاكل",
        "إحنا": "بناكل",
        "إنتو": "بتاكلو",
        "هم": "بوكلو",
    },
    "أكل - to eat (past)": {
        "أنا": "أكلت",
        "إنتَ": "أكلت",
        "إنتِ": "أكلتي",
        "هو": "أكل",
        "هي": "أكلت",
        "إحنا": "أكلنا",
        "إنتو": "أكلتو",
        "هم": "أكلو",
    },
    "كان - was (past)": {
        "أنا": "كنت",
        "إنتَ": "كنت",
        "إنتِ": "كنتي",
        "هو": "كان",
        "هي": "كانت",
        "إحنا": "كنا",
        "إنتو": "كنتو",
        "هم": "كانو",
    },
    "حكى - to speak (present)": {
        "أنا": "بحكي",
        "إنتَ": "بتحكي",
        "إنتِ": "بتحكي",
        "هو": "بحكي",
        "هي": "بتحكي",
        "إحنا": "بنحكي",
        "إنتو": "بتحكو",
        "هم": "بحكو",
    },
    "شاف - to see (past)": {
        "أنا": "شفت",
        "إنتَ": "شفت",
        "إنتِ": "شفتي",
        "هو": "شاف",
        "هي": "شافت",
        "إحنا": "شفنا",
        "إنتو": "شفتو",
        "هم": "شافو",
    },
}

CONVERSATION_SCENARIOS = [
    {
        "title": "Meeting Someone New",
        "prompt_en": "You meet a Jordanian at a coffee shop. Introduce yourself, ask their name, where they're from, and what they do.",
        "sample_lines": [
            ("You", "مرحبا! كيفك؟"),
            ("Them", "أهلا! الحمد لله. وإنت؟"),
            ("You", "تمام، الحمد لله. شو اسمك؟"),
            ("Them", "اسمي سامي. وإنت؟"),
            ("You", "اسمي ___. تشرفنا."),
            ("Them", "أهلا وسهلا. من وين إنت؟"),
        ],
    },
    {
        "title": "Ordering at a Restaurant",
        "prompt_en": "You're at a Jordanian restaurant. Order food, ask about dishes, and pay.",
        "sample_lines": [
            ("Waiter", "أهلا وسهلا! تفضل اقعد."),
            ("You", "شكرا. شو بتنصحني؟"),
            ("Waiter", "المنسف زاكي كتير اليوم."),
            ("You", "طيب، بدي منسف ولبن. لو سمحت."),
            ("Waiter", "تمام. تشرب شي؟"),
            ("You", "شاي بالميرمية."),
        ],
    },
    {
        "title": "Getting a Taxi",
        "prompt_en": "Negotiate with a taxi driver to go downtown. Ask for the meter or negotiate a price.",
        "sample_lines": [
            ("You", "تاكسي! على وسط البلد."),
            ("Driver", "يلا اطلع. خمس دنانير."),
            ("You", "كتير! شغل العداد."),
            ("Driver", "ما في عداد. أربعة."),
            ("You", "ثلاثة."),
            ("Driver", "طيب يلا."),
        ],
    },
    {
        "title": "Pharmacy Visit",
        "prompt_en": "You have a headache and a cold. Go to the pharmacy and get medicine.",
        "sample_lines": [
            ("You", "يعطيك العافية. بدي دوا لصداع ورشح."),
            ("Pharmacist", "عندك حرارة؟"),
            ("You", "شوي. مش كتير."),
            ("Pharmacist", "خد هاي الحبوب. حبة كل ثمان ساعات."),
            ("You", "قبل الأكل ولا بعده؟"),
            ("Pharmacist", "بعد الأكل. وشرب ميّ كتير."),
        ],
    },
    {
        "title": "Making Plans with a Friend",
        "prompt_en": "Call a friend and plan to meet this weekend.",
        "sample_lines": [
            ("You", "آلو! كيفك؟ شو بتسوي يوم السبت؟"),
            ("Friend", "فاضي إن شاء الله. ليش؟"),
            ("You", "يلا نتغدى سوا؟ في مطعم جديد."),
            ("Friend", "يلا! وين هو؟"),
            ("You", "بوسط البلد. نتلاقى الساعة وحدة؟"),
            ("Friend", "ماشي! بشوفك."),
        ],
    },
]

# --- Progress Tracking ---

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), ".progress.json")


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"scores": {}, "review_dates": {}, "streak": 0, "last_date": None}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def update_streak(progress):
    today = datetime.now().strftime("%Y-%m-%d")
    if progress.get("last_date") == today:
        return
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if progress.get("last_date") == yesterday:
        progress["streak"] = progress.get("streak", 0) + 1
    elif progress.get("last_date") != today:
        progress["streak"] = 1
    progress["last_date"] = today


# --- UI Helpers ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_score(correct, total):
    pct = int(correct / total * 100) if total > 0 else 0
    bar_len = 30
    filled = int(bar_len * correct / total) if total > 0 else 0
    bar = "#" * filled + "-" * (bar_len - filled)
    print(f"\n  Score: {correct}/{total} ({pct}%)")
    print(f"  [{bar}]")
    if pct >= 90:
        print("  Excellent! Ready to move on.")
    elif pct >= 70:
        print("  Good job! Review the ones you missed.")
    else:
        print("  Keep practicing! Try again soon.")
    print()


def get_all_vocab():
    """Get all vocabulary items across all days."""
    all_vocab = []
    for day, items in VOCAB_BY_DAY.items():
        for item in items:
            all_vocab.append((day, *item))
    return all_vocab


# --- Practice Modes ---

def flashcard_review(day=None):
    """Spaced repetition flashcard review."""
    print_header("Flashcard Review")

    if day:
        if day not in VOCAB_BY_DAY:
            print(f"  No vocabulary for Day {day}.")
            return
        vocab = [(day, *item) for item in VOCAB_BY_DAY[day]]
        print(f"  Reviewing Day {day} vocabulary ({len(vocab)} words)\n")
    else:
        vocab = get_all_vocab()
        random.shuffle(vocab)
        vocab = vocab[:20]  # limit to 20 for general review
        print(f"  General review — 20 random words\n")

    progress = load_progress()
    correct = 0
    total = len(vocab)

    for i, (d, arabic, translit, english) in enumerate(vocab):
        print(f"  Card {i+1}/{total}")
        print(f"  Arabic: {arabic}")
        input("  [Press Enter to reveal]")
        print(f"  Transliteration: {translit}")
        print(f"  Meaning: {english}")
        print()

        while True:
            rating = input("  Did you know it? (y/n/s to skip): ").strip().lower()
            if rating in ("y", "n", "s"):
                break

        if rating == "y":
            correct += 1
            key = arabic
            progress["scores"][key] = progress.get("scores", {}).get(key, 0) + 1
        elif rating == "n":
            key = arabic
            progress["scores"][key] = max(0, progress.get("scores", {}).get(key, 0) - 1)
        print()

    print_score(correct, total)
    update_streak(progress)
    save_progress(progress)


def translation_quiz(day=None):
    """English to Arabic translation quiz."""
    print_header("Translation Quiz (English -> Arabic)")

    if day:
        if day not in VOCAB_BY_DAY:
            print(f"  No vocabulary for Day {day}.")
            return
        vocab = list(VOCAB_BY_DAY[day])
        print(f"  Day {day} — {len(vocab)} questions\n")
    else:
        all_v = get_all_vocab()
        random.shuffle(all_v)
        vocab = [(a, t, e) for (_, a, t, e) in all_v[:15]]
        print(f"  General quiz — 15 questions\n")

    correct = 0
    total = len(vocab)
    missed = []

    for i, (arabic, translit, english) in enumerate(vocab):
        print(f"  {i+1}/{total}. What is '{english}' in Arabic?")
        answer = input("  Your answer (Arabic or transliteration): ").strip()

        if answer == arabic or answer.lower() == translit.lower().rstrip("?"):
            print("  Correct!\n")
            correct += 1
        else:
            print(f"  Answer: {arabic} ({translit})")
            missed.append((english, arabic, translit))
            print()

    print_score(correct, total)

    if missed:
        print("  Words to review:")
        for eng, ar, tr in missed:
            print(f"    {eng} = {ar} ({tr})")
        print()


def reverse_quiz(day=None):
    """Arabic to English translation quiz."""
    print_header("Reverse Quiz (Arabic -> English)")

    if day:
        if day not in VOCAB_BY_DAY:
            print(f"  No vocabulary for Day {day}.")
            return
        vocab = list(VOCAB_BY_DAY[day])
        print(f"  Day {day} — {len(vocab)} questions\n")
    else:
        all_v = get_all_vocab()
        random.shuffle(all_v)
        vocab = [(a, t, e) for (_, a, t, e) in all_v[:15]]
        print(f"  General quiz — 15 questions\n")

    correct = 0
    total = len(vocab)

    for i, (arabic, translit, english) in enumerate(vocab):
        print(f"  {i+1}/{total}. What does '{arabic}' ({translit}) mean?")
        answer = input("  Your answer: ").strip().lower()

        # Check if answer contains any key word from the meaning
        eng_words = set(english.lower().replace("/", " ").replace("(", "").replace(")", "").split())
        ans_words = set(answer.split())
        if ans_words & eng_words or answer == english.lower():
            print("  Correct!\n")
            correct += 1
        else:
            print(f"  Answer: {english}")
            print()

    print_score(correct, total)


def conjugation_drill():
    """Verb conjugation practice."""
    print_header("Conjugation Drill")

    verbs = list(CONJUGATION_DRILLS.keys())
    print("  Available verbs:")
    for i, v in enumerate(verbs, 1):
        print(f"    {i}. {v}")
    print(f"    {len(verbs)+1}. Random mix")

    choice = input(f"\n  Choose (1-{len(verbs)+1}): ").strip()

    try:
        idx = int(choice) - 1
        if idx == len(verbs):
            # Random mix
            verb_name = random.choice(verbs)
        else:
            verb_name = verbs[idx]
    except (ValueError, IndexError):
        verb_name = random.choice(verbs)

    forms = CONJUGATION_DRILLS[verb_name]
    print(f"\n  Conjugate: {verb_name}\n")

    pronouns = list(forms.keys())
    random.shuffle(pronouns)

    correct = 0
    total = len(pronouns)

    for pronoun in pronouns:
        expected = forms[pronoun]
        answer = input(f"  {pronoun}: ").strip()

        if answer == expected:
            print("  Correct!\n")
            correct += 1
        else:
            print(f"  Answer: {expected}\n")

    print_score(correct, total)


def conversation_practice():
    """Interactive conversation scenario practice."""
    print_header("Conversation Practice")

    print("  Scenarios:")
    for i, scenario in enumerate(CONVERSATION_SCENARIOS, 1):
        print(f"    {i}. {scenario['title']}")

    choice = input(f"\n  Choose (1-{len(CONVERSATION_SCENARIOS)}): ").strip()

    try:
        idx = int(choice) - 1
        scenario = CONVERSATION_SCENARIOS[idx]
    except (ValueError, IndexError):
        scenario = random.choice(CONVERSATION_SCENARIOS)

    print(f"\n  Scenario: {scenario['title']}")
    print(f"  Task: {scenario['prompt_en']}\n")
    print("  Sample dialogue (study this, then try on your own):\n")

    for speaker, line in scenario["sample_lines"]:
        print(f"    {speaker}: {line}")

    print("\n  " + "-" * 50)
    print("  Now try continuing the conversation!")
    print("  Type your Arabic responses. Type 'done' to finish.\n")

    turn = 0
    while True:
        response = input("  You: ").strip()
        if response.lower() in ("done", "quit", "exit", "خلص"):
            break
        turn += 1
        if turn < len(scenario["sample_lines"]):
            next_speaker, next_line = scenario["sample_lines"][min(turn, len(scenario["sample_lines"])-1)]
            if next_speaker != "You":
                print(f"  {next_speaker}: {next_line}")

    print(f"\n  Practice complete! You wrote {turn} responses.\n")


def daily_review():
    """Review material from a specific day."""
    print_header("Daily Review")

    available_days = sorted(VOCAB_BY_DAY.keys())
    print("  Available days:", ", ".join(str(d) for d in available_days))
    day_input = input("  Which day to review? ").strip()

    try:
        day = int(day_input)
    except ValueError:
        print("  Invalid day number.")
        return

    print(f"\n  Starting Day {day} review...\n")
    print("  Phase 1: Flashcards")
    flashcard_review(day)

    cont = input("  Continue to quiz? (y/n): ").strip().lower()
    if cont == "y":
        print("\n  Phase 2: Translation Quiz")
        translation_quiz(day)

    cont = input("  Continue to reverse quiz? (y/n): ").strip().lower()
    if cont == "y":
        print("\n  Phase 3: Reverse Quiz")
        reverse_quiz(day)


def week_review():
    """Review all vocabulary from a specific week."""
    print_header("Week Review")
    print("  1. Week 1 (Days 1-6)")
    print("  2. Week 2 (Days 8-13)")
    print("  3. Week 3 (Days 15-20)")
    print("  4. All weeks")

    choice = input("\n  Choose: ").strip()

    week_days = {
        "1": [1, 2, 3, 4, 5, 6],
        "2": [8, 9, 10, 12, 13],
        "3": [15, 16, 20],
        "4": list(VOCAB_BY_DAY.keys()),
    }

    days = week_days.get(choice, week_days["4"])
    vocab = []
    for d in days:
        if d in VOCAB_BY_DAY:
            vocab.extend(VOCAB_BY_DAY[d])

    random.shuffle(vocab)
    vocab = vocab[:25]

    print(f"\n  Quiz: {len(vocab)} words from selected days\n")

    correct = 0
    for i, (arabic, translit, english) in enumerate(vocab):
        print(f"  {i+1}/{len(vocab)}. What does '{arabic}' mean?")
        answer = input("  Answer: ").strip().lower()

        eng_words = set(english.lower().replace("/", " ").replace("(", "").replace(")", "").split())
        ans_words = set(answer.split())
        if ans_words & eng_words or answer == english.lower():
            print("  Correct!\n")
            correct += 1
        else:
            print(f"  Answer: {english} ({translit})\n")

    print_score(correct, len(vocab))


def show_stats():
    """Show learning statistics."""
    print_header("Your Progress")

    progress = load_progress()
    scores = progress.get("scores", {})
    streak = progress.get("streak", 0)

    total_words = len(get_all_vocab())
    known_words = sum(1 for v in scores.values() if v >= 2)
    learning_words = sum(1 for v in scores.values() if 0 < v < 2)

    print(f"  Current streak: {streak} days")
    print(f"  Words mastered (2+ correct): {known_words}/{total_words}")
    print(f"  Words learning: {learning_words}")
    print(f"  Words not started: {total_words - known_words - learning_words}")
    print()

    if known_words == 0:
        print("  Start with flashcard review to begin tracking progress!")
    elif known_words < total_words * 0.3:
        print("  Keep going! Focus on daily flashcard reviews.")
    elif known_words < total_words * 0.7:
        print("  Great progress! You're building a solid foundation.")
    else:
        print("  Amazing! You know most of the vocabulary!")
    print()


# --- Main Menu ---

def main():
    clear_screen()
    progress = load_progress()
    update_streak(progress)
    save_progress(progress)

    while True:
        print_header("Jordanian Arabic Practice Tool")
        print(f"  Streak: {progress.get('streak', 0)} days\n")
        print("  1. Flashcard Review (spaced repetition)")
        print("  2. Translation Quiz (English -> Arabic)")
        print("  3. Reverse Quiz (Arabic -> English)")
        print("  4. Conjugation Drill")
        print("  5. Conversation Practice")
        print("  6. Daily Review (specific day)")
        print("  7. Week Review")
        print("  8. View Progress")
        print("  9. Exit")

        choice = input("\n  Choose (1-9): ").strip()

        if choice == "1":
            flashcard_review()
        elif choice == "2":
            translation_quiz()
        elif choice == "3":
            reverse_quiz()
        elif choice == "4":
            conjugation_drill()
        elif choice == "5":
            conversation_practice()
        elif choice == "6":
            daily_review()
        elif choice == "7":
            week_review()
        elif choice == "8":
            show_stats()
        elif choice == "9":
            print("\n  !مع السلامة — ma3 is-salaame")
            print("  Keep practicing every day!\n")
            break
        else:
            print("  Invalid choice. Try again.")

        input("\n  Press Enter to continue...")
        clear_screen()


if __name__ == "__main__":
    main()
