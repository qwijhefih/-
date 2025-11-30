# File: app/data/question_generator.py
# -*- coding: utf-8 -*-
"""
AI 기반 문제 자동 생성 모듈
- Gemini API를 사용하여 정보처리산업기사 문제를 자동 생성
"""
import os
import json
import requests
from typing import List, Dict, Any

def generate_theory_questions(category: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    이론 문제 자동 생성
    
    Args:
        category: 문제 카테고리 (예: "운영체제", "데이터베이스", "네트워크" 등)
        count: 생성할 문제 개수
    
    Returns:
        생성된 문제 리스트
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={api_key}"
    
    prompt = f"""
당신은 정보처리산업기사 시험 문제 출제 전문가입니다.
'{category}' 카테고리에 대한 주관식 단답형 문제를 {count}개 생성해주세요.

**중요 규칙:**
1. 실제 시험에 나올 법한 난이도로 출제
2. 각 문제는 명확한 정답이 있어야 함
3. 정답은 가능한 모든 표현을 배열로 제공 (예: ["TCP", "Transmission Control Protocol"])
4. 해설은 핵심만 1-2줄로 간결하게
5. 난이도(difficulty)는 "기초", "중급", "고급" 중 하나로 지정
6. 카테고리(category)는 "{category}"로 고정

**출력 형식 (JSON):**
```json
[
  {{
    "q": "문제 내용",
    "answer": ["정답1", "정답2"],
    "explain": "핵심 해설",
    "difficulty": "기초|중급|고급",
    "category": "{category}"
  }}
]
```

**중요:** 반드시 JSON 배열 형식으로만 출력하고, 다른 텍스트는 포함하지 마세요.
"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        
        ai_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # JSON 추출 (```json ... ``` 제거)
        ai_text = ai_text.strip()
        if ai_text.startswith("```json"):
            ai_text = ai_text[7:]
        if ai_text.startswith("```"):
            ai_text = ai_text[3:]
        if ai_text.endswith("```"):
            ai_text = ai_text[:-3]
        ai_text = ai_text.strip()
        
        questions = json.loads(ai_text)
        return questions
        
    except Exception as e:
        print(f"문제 생성 실패: {e}")
        return []


def generate_code_questions(language: str, count: int = 5) -> List[Dict[str, Any]]:
    """
    코드 문제 자동 생성
    
    Args:
        language: 프로그래밍 언어 (예: "Python", "Java", "C")
        count: 생성할 문제 개수
    
    Returns:
        생성된 코드 문제 리스트
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={api_key}"
    
    prompt = f"""
당신은 정보처리산업기사 실기 시험 코드 문제 출제 전문가입니다.
'{language}' 언어로 작성된 코드의 출력 결과를 맞추는 주관식 문제를 {count}개 생성해주세요.

**중요 규칙:**
1. 실제 시험에 나올 법한 난이도 (중급 수준)
2. 코드는 짧고 명확하게 (10줄 이내)
3. 출력 결과가 명확해야 함
4. 정답은 가능한 모든 표현을 배열로 제공
5. 해설은 코드 동작 원리를 간결하게 설명
6. 난이도(difficulty)는 "기초", "중급", "고급" 중 하나로 지정
7. 카테고리(category)는 "코딩"으로 고정

**출력 형식 (JSON):**
```json
[
  {{
    "q": "[코드] 다음 {language} 코드의 출력 결과는?\\n\\n코드 내용",
    "answer": ["정답1", "정답2"],
    "explain": "핵심 해설",
    "difficulty": "기초|중급|고급",
    "category": "코딩",
    "language": "{language}"
  }}
]
```

**중요:** 반드시 JSON 배열 형식으로만 출력하고, 다른 텍스트는 포함하지 마세요.
"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        
        ai_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # JSON 추출
        ai_text = ai_text.strip()
        if ai_text.startswith("```json"):
            ai_text = ai_text[7:]
        if ai_text.startswith("```"):
            ai_text = ai_text[3:]
        if ai_text.endswith("```"):
            ai_text = ai_text[:-3]
        ai_text = ai_text.strip()
        
        questions = json.loads(ai_text)
        return questions
        
    except Exception as e:
        print(f"코드 문제 생성 실패: {e}")
        return []


def save_generated_questions(questions: List[Dict[str, Any]], question_type: str = "theory") -> bool:
    """
    생성된 문제를 파일에 저장
    
    Args:
        questions: 저장할 문제 리스트
        question_type: "theory" 또는 "code"
    
    Returns:
        저장 성공 여부
    """
    if question_type == "theory":
        file_path = os.path.join(os.path.dirname(__file__), "theory_bank.py")
    else:
        file_path = os.path.join(os.path.dirname(__file__), "code_bank.py")
    
    try:
        # 기존 파일 읽기
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 새 문제를 Python 코드 형식으로 변환
        new_questions_code = "    # --- AI 자동 생성 문제 ---\n"
        for q in questions:
            new_questions_code += "    {\n"
            new_questions_code += f'        "q": {repr(q["q"])},\n'
            new_questions_code += f'        "answer": {repr(q["answer"])},\n'
            new_questions_code += f'        "explain": {repr(q.get("explain", ""))}\n'
            new_questions_code += "    },\n"
        
        # 마지막 ]를 찾아서 그 앞에 삽입
        last_bracket_idx = content.rfind("]")
        if last_bracket_idx != -1:
            new_content = content[:last_bracket_idx] + new_questions_code + content[last_bracket_idx:]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"문제 저장 실패: {e}")
        return False


def batch_generate_questions(categories: List[str], count_per_category: int = 3) -> Dict[str, int]:
    """
    여러 카테고리에 대해 한 번에 문제 생성
    
    Args:
        categories: 카테고리 리스트
        count_per_category: 카테고리당 생성할 문제 개수
    
    Returns:
        카테고리별 생성된 문제 개수
    """
    results = {}
    
    for category in categories:
        print(f"'{category}' 카테고리 문제 생성 중...")
        questions = generate_theory_questions(category, count_per_category)
        
        if questions:
            success = save_generated_questions(questions, "theory")
            if success:
                results[category] = len(questions)
                print(f"✅ {category}: {len(questions)}개 문제 생성 완료")
            else:
                results[category] = 0
                print(f"❌ {category}: 저장 실패")
        else:
            results[category] = 0
            print(f"❌ {category}: 생성 실패")
    
    return results
