# -*- coding: utf-8 -*-
"""
학습 통계 저장 모듈
- 퀴즈 결과를 저장하고 통계를 분석
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

STATS_FILE = os.path.join(os.path.dirname(__file__), "stats_store.json")

# 레벨 시스템 설정
LEVEL_CONFIG = [
    {"level": 1, "name": "입문자", "min_xp": 0, "color": "gray"},
    {"level": 2, "name": "초보자", "min_xp": 100, "color": "blue"},
    {"level": 3, "name": "학습자", "min_xp": 300, "color": "green"},
    {"level": 4, "name": "숙련자", "min_xp": 700, "color": "yellow"},
    {"level": 5, "name": "전문가", "min_xp": 1500, "color": "orange"},
    {"level": 6, "name": "마스터", "min_xp": 3000, "color": "red"},
    {"level": 7, "name": "그랜드마스터", "min_xp": 5000, "color": "purple"},
]

def calculate_xp(score: int, total: int, quiz_type: str = "mixed") -> int:
    """경험치 계산"""
    base_xp = score * 5  # 정답 1개당 5XP
    
    # 퀴즈 타입별 보너스
    bonus = 1.0
    if quiz_type == "mock_exam":
        bonus = 1.5  # 모의고사 50% 보너스
    elif quiz_type == "review":
        bonus = 1.2  # 복습 20% 보너스
    
    # 정확도 보너스
    accuracy = (score / total) * 100 if total > 0 else 0
    if accuracy >= 90:
        bonus += 0.5
    elif accuracy >= 80:
        bonus += 0.3
    elif accuracy >= 70:
        bonus += 0.1
    
    return int(base_xp * bonus)

def get_level_info(xp: int) -> Dict[str, Any]:
    """현재 XP로 레벨 정보 계산"""
    current_level = LEVEL_CONFIG[0]
    next_level = LEVEL_CONFIG[1] if len(LEVEL_CONFIG) > 1 else None
    
    for i, level in enumerate(LEVEL_CONFIG):
        if xp >= level["min_xp"]:
            current_level = level
            next_level = LEVEL_CONFIG[i + 1] if i + 1 < len(LEVEL_CONFIG) else None
    
    # 다음 레벨까지 필요한 XP
    xp_to_next = 0
    progress_percent = 100
    
    if next_level:
        xp_to_next = next_level["min_xp"] - xp
        current_level_xp = current_level["min_xp"]
        next_level_xp = next_level["min_xp"]
        progress = xp - current_level_xp
        total_needed = next_level_xp - current_level_xp
        progress_percent = int((progress / total_needed) * 100) if total_needed > 0 else 0
    
    return {
        "level": current_level["level"],
        "name": current_level["name"],
        "color": current_level["color"],
        "xp": xp,
        "xp_to_next": xp_to_next,
        "progress_percent": progress_percent,
        "next_level": next_level["name"] if next_level else "MAX",
        "is_max_level": next_level is None
    }

def load_stats() -> Dict[str, Any]:
    """통계 데이터 로드"""
    if not os.path.exists(STATS_FILE):
        return {
            "total_quizzes": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "xp": 0,
            "history": [],
            "category_stats": {}
        }
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # XP 필드가 없으면 추가
            if "xp" not in data:
                data["xp"] = 0
            return data
    except Exception:
        return {
            "total_quizzes": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "xp": 0,
            "history": [],
            "category_stats": {}
        }

def save_stats(stats: Dict[str, Any]) -> None:
    """통계 데이터 저장"""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def add_quiz_result(score: int, total: int, quiz_type: str = "mixed") -> Dict[str, Any]:
    """퀴즈 결과 추가 (경험치 및 레벨 포함)"""
    stats = load_stats()
    
    # 경험치 계산
    earned_xp = calculate_xp(score, total, quiz_type)
    stats["xp"] = stats.get("xp", 0) + earned_xp
    
    # 전체 통계 업데이트
    stats["total_quizzes"] += 1
    stats["total_questions"] += total
    stats["correct_answers"] += score
    
    # 이력 추가
    stats["history"].append({
        "date": datetime.now().isoformat(),
        "score": score,
        "total": total,
        "type": quiz_type,
        "accuracy": round((score / total) * 100, 1) if total > 0 else 0,
        "earned_xp": earned_xp
    })
    
    # 최근 20개만 유지
    if len(stats["history"]) > 20:
        stats["history"] = stats["history"][-20:]
    
    save_stats(stats)
    
    # 레벨 정보 반환
    return get_level_info(stats["xp"])

def get_dashboard_stats() -> Dict[str, Any]:
    """대시보드용 통계 계산"""
    stats = load_stats()
    
    total_accuracy = 0
    if stats["total_questions"] > 0:
        total_accuracy = round((stats["correct_answers"] / stats["total_questions"]) * 100, 1)
    
    # 최근 5회 평균
    recent_accuracy = 0
    if stats["history"]:
        recent = stats["history"][-5:]
        recent_accuracy = round(sum(h["accuracy"] for h in recent) / len(recent), 1)
    
    # 레벨 정보
    level_info = get_level_info(stats.get("xp", 0))
    
    return {
        "total_quizzes": stats["total_quizzes"],
        "total_questions": stats["total_questions"],
        "correct_answers": stats["correct_answers"],
        "total_accuracy": total_accuracy,
        "recent_accuracy": recent_accuracy,
        "history": stats["history"][-10:],  # 최근 10개만
        "level_info": level_info
    }

def reset_stats() -> None:
    """통계 초기화"""
    save_stats({
        "total_quizzes": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "xp": 0,
        "history": [],
        "category_stats": {}
    })
