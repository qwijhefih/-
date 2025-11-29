# File: app/data/category_analysis.py
# -*- coding: utf-8 -*-
"""
카테고리별 통계 분석 모듈
"""
import json
import os
from typing import Dict, Any, List
from collections import defaultdict

CATEGORY_STATS_FILE = os.path.join(os.path.dirname(__file__), "category_stats.json")

# 문제 카테고리 매핑
CATEGORY_KEYWORDS = {
    "운영체제": ["운영체제", "프로세스", "스케줄링", "메모리", "페이지", "교착상태", "CPU"],
    "데이터베이스": ["데이터베이스", "SQL", "DDL", "DML", "DCL", "트랜잭션", "정규화", "릴레이션", "Join"],
    "네트워크": ["네트워크", "OSI", "TCP", "UDP", "IP", "프로토콜", "라우팅"],
    "소프트웨어공학": ["소프트웨어", "UML", "테스트", "설계", "개발", "애자일", "폭포수"],
    "보안": ["보안", "암호화", "해킹", "SQL Injection", "XSS", "방화벽", "IDS", "IPS"],
    "코딩": ["[코드]", "Python", "Java", "C언어", "출력"],
}

def detect_category(question_text: str) -> str:
    """문제 텍스트에서 카테고리 감지"""
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in question_text.lower():
                return category
    return "기타"

def load_category_stats() -> Dict[str, Any]:
    """카테고리별 통계 로드"""
    if not os.path.exists(CATEGORY_STATS_FILE):
        return {cat: {"total": 0, "correct": 0} for cat in CATEGORY_KEYWORDS.keys()}
    try:
        with open(CATEGORY_STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {cat: {"total": 0, "correct": 0} for cat in CATEGORY_KEYWORDS.keys()}

def save_category_stats(stats: Dict[str, Any]) -> None:
    """카테고리별 통계 저장"""
    with open(CATEGORY_STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def update_category_stats(questions: List[Dict[str, Any]]) -> None:
    """퀴즈 결과로 카테고리별 통계 업데이트"""
    stats = load_category_stats()
    
    for q in questions:
        category = detect_category(q.get("q", ""))
        
        if category not in stats:
            stats[category] = {"total": 0, "correct": 0}
        
        stats[category]["total"] += 1
        
        # 정답 여부 확인
        user_answer = str(q.get("user", "")).strip().lower()
        correct_answers = q.get("answer", [])
        if not isinstance(correct_answers, list):
            correct_answers = [str(correct_answers)]
        
        # 정규화
        def normalize(text):
            return text.lower().replace(' ', '').replace('\n', '').replace('\r', '').replace('[', '').replace(']', '').replace(',', '')
        
        user_normalized = normalize(user_answer)
        is_correct = user_normalized in [normalize(str(ans)) for ans in correct_answers]
        
        if is_correct:
            stats[category]["correct"] += 1
    
    save_category_stats(stats)

def get_weakness_analysis() -> List[Dict[str, Any]]:
    """약점 분석 결과 반환"""
    stats = load_category_stats()
    analysis = []
    
    for category, data in stats.items():
        total = data.get("total", 0)
        correct = data.get("correct", 0)
        
        if total > 0:
            accuracy = round((correct / total) * 100, 1)
            analysis.append({
                "category": category,
                "total": total,
                "correct": correct,
                "accuracy": accuracy,
                "weakness_level": "높음" if accuracy < 60 else "중간" if accuracy < 80 else "낮음"
            })
    
    # 정확도 낮은 순으로 정렬
    analysis.sort(key=lambda x: x["accuracy"])
    
    return analysis

def reset_category_stats() -> None:
    """카테고리별 통계 초기화"""
    stats = {cat: {"total": 0, "correct": 0} for cat in CATEGORY_KEYWORDS.keys()}
    save_category_stats(stats)
