# File: app/data/study_notes.py
# -*- coding: utf-8 -*-
"""
학습 일지/메모 저장 모듈
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

NOTES_FILE = os.path.join(os.path.dirname(__file__), "study_notes.json")

def load_notes() -> List[Dict[str, Any]]:
    """메모 목록 로드"""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_notes(notes: List[Dict[str, Any]]) -> None:
    """메모 목록 저장"""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def add_note(title: str, content: str, category: str = "일반") -> Dict[str, Any]:
    """새 메모 추가"""
    notes = load_notes()
    
    note = {
        "id": len(notes) + 1,
        "title": title,
        "content": content,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    notes.append(note)
    save_notes(notes)
    
    return note

def update_note(note_id: int, title: str = None, content: str = None, category: str = None) -> bool:
    """메모 수정"""
    notes = load_notes()
    
    for note in notes:
        if note["id"] == note_id:
            if title:
                note["title"] = title
            if content:
                note["content"] = content
            if category:
                note["category"] = category
            note["updated_at"] = datetime.now().isoformat()
            save_notes(notes)
            return True
    
    return False

def delete_note(note_id: int) -> bool:
    """메모 삭제"""
    notes = load_notes()
    original_len = len(notes)
    
    notes = [n for n in notes if n["id"] != note_id]
    
    if len(notes) < original_len:
        save_notes(notes)
        return True
    
    return False

def get_notes_by_category(category: str = None) -> List[Dict[str, Any]]:
    """카테고리별 메모 조회"""
    notes = load_notes()
    
    if category:
        notes = [n for n in notes if n.get("category") == category]
    
    # 최신순 정렬
    notes.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    
    return notes
