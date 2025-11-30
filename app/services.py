# File: app/services.py
# -*- coding: utf-8 -*-
"""
[레거시 코드] 객관식 퀴즈 서비스 모듈
- 현재 사용되지 않음 (quiz.py에서 직접 data 모듈 사용)
- 향후 객관식 퀴즈 모드 추가 시 활용 가능
- 삭제하지 않고 보관
"""
import json, os, random, csv
from datetime import datetime
from typing import Dict, Any, List, Tuple
from flask import current_app
from .kb import KB, GLOSSARY

def _wrong_path() -> str:
    return current_app.config.get("WRONG_FILE", "wrong_bank.json")

def load_wrong() -> Dict[str, Any]:
    p = _wrong_path()
    if not os.path.exists(p): return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def save_wrong(bank: Dict[str, Any]) -> None:
    with open(_wrong_path(), "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

def flat_items(exclude_cat: str | None = None) -> List[str]:
    out: List[str] = []
    for c in KB:
        if exclude_cat and c["name"] == exclude_cat: continue
        out.extend(c["items"])
    return out

def make_mc_question() -> Dict[str, Any]:
    cat = random.choice(KB)
    correct = random.choice(cat["items"])
    distract = random.sample(flat_items(exclude_cat=cat["name"]), k=3)
    options = [correct] + distract
    random.shuffle(options)
    answer = options.index(correct)
    return {
        "q": f"다음 중 '<b>{cat['name']}</b>'에 속하는 것은?",
        "options": options,
        "answer": answer,  # 0-based (프론트가 그대로 씀)
        "explain": f"암기어 <b>{cat['mnemonic']}</b> — {', '.join(cat['items'])}",
    }

def make_quiz(n: int) -> List[Dict[str, Any]]:
    qs, seen = [], set()
    while len(qs) < n:
        it = make_mc_question()
        key = (it["q"], tuple(it["options"]))
        if key in seen: continue
        seen.add(key); qs.append(it)
    return qs

def explain_for(text: str) -> str:
    g = GLOSSARY.get(text)
    if not g: return "핵심 묶음을 전체로 암기!"
    items = next((c["items"] for c in KB if c["name"] == g["category"]), [])
    return f"암기어 <b>{g['mnemonic']}</b> — {', '.join(items)}"

def build_review_items(n: int) -> List[Dict[str, Any]]:
    bank = load_wrong()
    entries = list(bank.values()); random.shuffle(entries)
    entries = entries[:n]
    items = []
    all_opts = flat_items()
    for e in entries:
        q = e["question"]
        correct = e["options"][e["answer"]]
        distract = random.sample([x for x in all_opts if x != correct], k=3)
        options = [correct] + distract
        random.shuffle(options)
        items.append({
            "q": q,
            "options": options,
            "answer": options.index(correct),
            "explain": explain_for(correct)
        })
    return items

def register_wrong(it: Dict[str, Any], user_idx: int) -> None:
    bank = load_wrong()
    key = it["q"].strip()
    now = datetime.now().isoformat(timespec="seconds")
    entry = bank.get(key)
    if entry is None:
        bank[key] = {
            "question": key,
            "options": it["options"],
            "answer": it["answer"],
            "last_user": user_idx,
            "times_wrong": 1,
            "review_streak": 0,
            "last_ts": now,
        }
    else:
        entry["times_wrong"] = int(entry.get("times_wrong", 0)) + 1
        entry["last_user"] = user_idx
        entry["review_streak"] = 0
        entry["last_ts"] = now
        bank[key] = entry
    save_wrong(bank)

def apply_review_results(results: List[Dict[str, Any]]) -> Tuple[int, int]:
    bank = load_wrong()
    removed = 0
    for r in results:
        key = (r.get("q") or "").strip()
        if key not in bank: continue
        entry = bank[key]
        if r.get("correct"):
            entry["review_streak"] = int(entry.get("review_streak", 0)) + 1
            if entry["review_streak"] >= int(current_app.config["REVIEW_MASTER_THRESHOLD"]):
                del bank[key]; removed += 1; continue
        else:
            entry["review_streak"] = 0
            entry["times_wrong"] = int(entry.get("times_wrong", 0)) + 1
        entry["last_ts"] = datetime.now().isoformat(timespec="seconds")
        bank[key] = entry
    save_wrong(bank)
    return removed, len(bank)

def export_wrong_csv(path: str) -> str:
    bank = load_wrong()
    if not bank: raise RuntimeError("오답이 없습니다.")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["question","options","answer","last_user","times_wrong","review_streak","last_ts"])
        for e in bank.values():
            w.writerow([e["question"], " | ".join(e["options"]), e["answer"], e["last_user"],
                        e["times_wrong"], e["review_streak"], e["last_ts"]])
    return path
