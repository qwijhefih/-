# -*- coding: utf-8 -*-
import json
import os
from typing import List, Dict
from datetime import datetime, timedelta

STORE = os.path.join(os.path.dirname(__file__), "wrong_store.json")

def load_wrong() -> List[Dict]:
    if not os.path.exists(STORE):
        return []
    try:
        with open(STORE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 형식 안전장치
            out = []
            for it in data:
                q = it.get("q"); opts = it.get("options"); ans = it.get("answer")
                if isinstance(q, str) and isinstance(opts, list) and isinstance(ans, int):
                    out.append({
                        "q": q, "options": opts, "answer": ans,
                        "explain": it.get("explain", ""),
                        "review_count": it.get("review_count", 0),
                        "last_wrong_date": it.get("last_wrong_date", ""),
                        "next_review_date": it.get("next_review_date", "")
                    })
            return out
    except Exception:
        return []

def save_wrong(new_items: List[Dict]):
    """중복 방지: 질문 텍스트 기준으로 set"""
    existing = load_wrong()
    seen = {e["q"]: e for e in existing}
    
    for it in new_items:
        question = it.get("q")
        if question not in seen:
            # 새로운 틀린 문제 추가
            it["review_count"] = 0
            it["last_wrong_date"] = datetime.now().isoformat()
            it["next_review_date"] = calculate_next_review_date(0)
            existing.append(it)
            seen[question] = it
        else:
            # 기존에 있던 문제는 재출제 일정 업데이트
            existing_item = seen[question]
            existing_item["review_count"] += 1
            existing_item["last_wrong_date"] = datetime.now().isoformat()
            existing_item["next_review_date"] = calculate_next_review_date(existing_item["review_count"])
    
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def calculate_next_review_date(review_count: int) -> str:
    """복습 간격 계산 (간격반복학습 알고리즘)"""
    # 1일 -> 3일 -> 7일 -> 14일 -> 30일
    intervals = [1, 3, 7, 14, 30]
    interval = intervals[min(review_count, len(intervals) - 1)]
    next_date = datetime.now() + timedelta(days=interval)
    return next_date.isoformat()

def get_review_questions() -> List[Dict]:
    """오늘 복습해야 할 문제 반환"""
    all_wrong = load_wrong()
    today = datetime.now()
    
    review_questions = []
    for item in all_wrong:
        next_review = item.get("next_review_date", "")
        if next_review:
            try:
                next_date = datetime.fromisoformat(next_review)
                if next_date <= today:
                    review_questions.append(item)
            except:
                # 날짜 파싱 실패 시 복습 대상에 포함
                review_questions.append(item)
    
    return review_questions

def mark_as_correct(question: str) -> bool:
    """문제를 맞췄을 때 다음 복습 일정 업데이트"""
    all_wrong = load_wrong()
    
    for item in all_wrong:
        if item["q"] == question:
            item["review_count"] += 1
            item["next_review_date"] = calculate_next_review_date(item["review_count"])
            
            with open(STORE, "w", encoding="utf-8") as f:
                json.dump(all_wrong, f, ensure_ascii=False, indent=2)
            return True
    
    return False

def remove_mastered_questions() -> int:
    """5회 이상 연속 정답 시 오답 목록에서 제거"""
    all_wrong = load_wrong()
    original_count = len(all_wrong)
    
    # review_count가 5 이상인 문제 제거
    filtered = [item for item in all_wrong if item.get("review_count", 0) < 5]
    
    if len(filtered) < original_count:
        with open(STORE, "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
    
    return original_count - len(filtered)