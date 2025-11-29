# File: app/data/bookmarks.py
# -*- coding: utf-8 -*-
"""
북마크 저장 모듈
- 중요한 문제를 북마크하여 저장
"""
import json
import os
from typing import List, Dict, Any

BOOKMARK_FILE = os.path.join(os.path.dirname(__file__), "bookmarks.json")

def load_bookmarks() -> List[Dict[str, Any]]:
    """북마크 목록 로드"""
    if not os.path.exists(BOOKMARK_FILE):
        return []
    try:
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_bookmarks(bookmarks: List[Dict[str, Any]]) -> None:
    """북마크 목록 저장"""
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

def add_bookmark(question: str, answer: str, explain: str) -> bool:
    """북마크 추가 (중복 체크)"""
    bookmarks = load_bookmarks()
    
    # 이미 북마크된 문제인지 확인
    for bm in bookmarks:
        if bm.get("q") == question:
            return False  # 이미 존재
    
    bookmarks.append({
        "q": question,
        "answer": answer,
        "explain": explain
    })
    
    save_bookmarks(bookmarks)
    return True

def remove_bookmark(question: str) -> bool:
    """북마크 제거"""
    bookmarks = load_bookmarks()
    original_len = len(bookmarks)
    
    bookmarks = [bm for bm in bookmarks if bm.get("q") != question]
    
    if len(bookmarks) < original_len:
        save_bookmarks(bookmarks)
        return True
    return False

def clear_bookmarks() -> None:
    """모든 북마크 삭제"""
    save_bookmarks([])
