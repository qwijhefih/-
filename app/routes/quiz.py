# File: app/routes/quiz.py
# -*- coding: utf-8 -*-
import random
import os
import requests 
import json
from flask import Blueprint, jsonify, request
from ..data.theory_bank import THEORY_QUESTIONS
from ..data.code_bank import CODE_QUESTIONS
from ..data.wrong_store import load_wrong, save_wrong, get_review_questions, mark_as_correct, remove_mastered_questions
from ..data.stats_store import add_quiz_result, get_dashboard_stats, reset_stats
from ..data.bookmarks import load_bookmarks, add_bookmark, remove_bookmark, clear_bookmarks
from ..data.question_generator import generate_theory_questions, generate_code_questions, save_generated_questions, batch_generate_questions
from ..data.category_analysis import update_category_stats, get_weakness_analysis, reset_category_stats
from ..data.study_notes import add_note, update_note, delete_note, get_notes_by_category
# from .. import services  # (비활성화 상태)

bp = Blueprint("quiz", __name__)

# -----------------------------------------------------------------
# 퀴즈 API
# -----------------------------------------------------------------

@bp.get("/api/quiz")
def api_quiz():
    """[수정] 총 20문제 (이론 15 + 코드 5)"""
    n = int(request.args.get("n", 20))
    n_code = 5
    n_theory = n - n_code
    
    t_pool = THEORY_QUESTIONS[:]
    random.shuffle(t_pool)
    items_theory = t_pool[:n_theory]

    c_pool = CODE_QUESTIONS[:]
    random.shuffle(c_pool)
    items_code = c_pool[:n_code]

    items = items_theory + items_code
    random.shuffle(items)
    
    return jsonify({"items": items})

@bp.post("/api/submit")
def api_submit():
    """[수정] 줄바꿈, 특수기호([,],;)를 모두 무시하도록 채점 로직 강화"""
    data = request.get_json(force=True) or {}
    items = data.get("items") or []
    score = 0
    wrong = []
    
    for it in items:
        user_ans = str(it.get("user", "")).strip()
        correct_answer_data = it.get("answer")

        # 1. 정답 목록 리스트로 통일
        if not isinstance(correct_answer_data, list):
            correct_answers = [str(correct_answer_data)]
        else:
            correct_answers = [str(ans) for ans in correct_answer_data]

        # 2. 정규화 로직 (공백, 줄바꿈, 특수기호 제거)
        def normalize_text(text):
            text = text.lower()
            text = text.replace(' ', '').replace('\n', '').replace('\r', '')
            text = text.replace('[', '').replace(']', '').replace(',', '').replace(';', '')
            return text

        # 3. 사용자의 답안과 정답 목록을 모두 정규화
        user_normalized = normalize_text(user_ans)
        correct_normalized_list = [normalize_text(ans) for ans in correct_answers]
        
        # 4. 정규화된 목록에 포함되어 있는지 확인
        is_correct = user_normalized in correct_normalized_list
        
        if is_correct:
            score += 1
        else:
            # 1차에서 틀리면 그냥 오답 처리
            wrong.append({
                "q": it.get("q"),
                "options": [], 
                "answer": correct_answers[0], # 대표 답안
                "explain": it.get("explain", ""),
                "user_answer": user_ans # 사용자가 입력한 원본 답안
            })
            
    # 오답 영속 저장
    if wrong:
        save_wrong(wrong)
    
    # 통계 저장 (레벨 정보 반환)
    quiz_type = data.get("quiz_type", "mixed")
    level_info = add_quiz_result(score, len(items), quiz_type)
    
    # 카테고리별 통계 업데이트
    update_category_stats(items)
        
    return jsonify({
        "score": score, 
        "total": len(items), 
        "wrong": wrong,
        "level_info": level_info
    })

# -----------------------------------------------------------------
# 오답노트 API
# -----------------------------------------------------------------

@bp.get("/api/review")
def api_review():
    """오늘 복습해야 할 문제 우선 + 나머지 오답"""
    review_due = get_review_questions()  # 오늘 복습 예정
    all_wrong = load_wrong()
    
    # 복습 예정 문제가 없으면 전체 오답에서
    if not review_due:
        if not all_wrong:
            return api_quiz()
        pool = all_wrong[:]
        random.shuffle(pool)
        return jsonify({"items": pool[:10]})
    
    # 복습 예정 문제 우선 배치
    random.shuffle(review_due)
    remaining = [q for q in all_wrong if q not in review_due]
    random.shuffle(remaining)
    
    combined = review_due + remaining
    return jsonify({"items": combined[:10]})

@bp.post("/api/clear_wrong")
def api_clear_wrong():
    save_wrong([])  # 초기화
    return jsonify({"ok": True})

@bp.post("/api/mark_correct")
def api_mark_correct():
    """문제를 맞췄을 때 호출"""
    data = request.get_json(force=True) or {}
    question = data.get("question")
    
    if not question:
        return jsonify({"ok": False, "message": "문제 정보가 없습니다."}), 400
    
    success = mark_as_correct(question)
    removed = remove_mastered_questions()
    
    return jsonify({
        "ok": success,
        "message": f"{removed}개의 문제가 마스터되어 제거되었습니다." if removed > 0 else "복습 일정이 업데이트되었습니다."
    })

# -----------------------------------------------------------------
# AI 기능 API (설명, 챗봇, 모델 리스트)
# -----------------------------------------------------------------

@bp.post("/api/ai/explain")
def api_ai_explain():
    """AI 문제 해설 (이전과 동일, 수정 없음)"""
    data = request.get_json(force=True) or {}
    q_text = data.get("q")
    q_explain = data.get("explain")
    if not q_text or not q_explain: return jsonify({"error": "No question or explanation provided."}), 400
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return jsonify({"error": "AI API 키가 설정되지 않았습니다."}), 500
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={api_key}"
        prompt = f"""
        당신은 정보처리기사/산업기사 시험 튜터입니다.
        나는 이틀 뒤 시험이라 시간이 없습니다.
        다음 문제와 정답 해설을 보고, **가장 중요한 핵심만 1~2줄로 요약**해서 설명해주세요.
        [문제]:\n{q_text}\n[정답 및 기본 해설]:\n{q_explain}\n[AI의 핵심 요약]:
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() 
        response_data = response.json()
        ai_explanation = response_data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"explanation": ai_explanation})
    except requests.exceptions.HTTPError as http_err:
        print(f"AI API HTTP 오류: {http_err}")
        print(f"응답 내용: {http_err.response.text}")
        error_details = http_err.response.json().get('error', {}).get('message', '알 수 없는 HTTP 오류')
        return jsonify({"error": f"AI API 오류: {error_details}"}), 500
    except Exception as e:
        print(f"AI API 기타 오류: {e}") 
        return jsonify({"error": f"AI 응답 처리 중 오류 발생: {e}"}), 500

@bp.get("/api/ai/listmodels")
def api_ai_list_models():
    """모델 리스트 조회 (이전과 동일, 수정 없음)"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return jsonify({"error": "AI API 키가 설정되지 않았습니다."}), 500
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        headers = { "Content-Type": "application/json" }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return jsonify(response_data)
    except requests.exceptions.HTTPError as http_err:
        print(f"모델 목록 조회 HTTP 오류: {http_err}")
        print(f"응답 내용: {http_err.response.text}")
        error_details = http_err.response.json().get('error', {}).get('message', '알 수 없는 HTTP 오류')
        return jsonify({"error": f"API 오류: {error_details}"}), 500
    except Exception as e:
        print(f"모델 목록 조회 기타 오류: {e}") 
        return jsonify({"error": f"AI 응답 처리 중 오류 발생: {e}"}), 500

# -----------------------------------------------------------------
# [ ✅ 수정 ] AI 챗봇 API (시스템 프롬프트와 대화 기록 분리)
# -----------------------------------------------------------------
@bp.post("/api/ai/chat")
def api_ai_chat():
    """
    [수정] AI 챗봇 API (대화 기록을 포함하여 맥락 유지)
    """
    data = request.get_json(force=True) or {}
    query = data.get("query")
    history = data.get("history", []) # 👈 [신규] 프론트에서 보낸 대화 기록(history)을 받음

    if not query:
        return jsonify({"error": "No query provided."}), 400

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return jsonify({"error": "AI API 키가 설정되지 않았습니다."}), 500

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent?key={api_key}"
        
        # --- [ ✅ 수정된 Payload ] ---
        
        # 1. AI의 역할을 정의하는 시스템 프롬프트
        system_prompt = """
        당신은 '정보처리기사/산업기사' 시험 전문가입니다. 
        학생의 다음 질문에 대해 핵심만 간단하고 명확하게 답변해주세요.
        학생의 이전 질문이나 대화 내용을 기억하고 맥락에 맞게 이어서 대답해주세요.
        """
        
        # 2. Gemini API가 요구하는 'contents' 배열 생성
        contents = []
        
        # 3. 프론트에서 받은 이전 대화 기록(history)을 API 형식에 맞게 추가
        # (Gemini API는 user -> model -> user -> model 순서를 엄격하게 지켜야 함)
        for item in history:
            contents.append({
                "role": item["role"], # "user" 또는 "model"
                "parts": [{"text": item["text"]}]
            })
            
        # 4. 방금 사용자가 입력한 '새 질문'을 마지막에 추가
        contents.append({
            "role": "user",
            "parts": [{"text": query}]
        })

        # 5. 최종 Payload (시스템 프롬프트와 대화 내용을 분리)
        payload = {
            "contents": contents,
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            }
        }
        # --- [ Payload 수정 끝 ] ---
        
        headers = { "Content-Type": "application/json" }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # 4xx, 5xx 에러가 나면 여기서 멈춤
        
        response_data = response.json()
        
        # [수정] Gemini API가 응답을 거부(Safety Rating)했는지 확인
        if not response_data.get('candidates'):
            print(f"AI 챗봇 응답 거부: {response_data}")
            return jsonify({"error": "AI가 응답을 거부했습니다. (안전 설정)"}), 500

        ai_answer = response_data['candidates'][0]['content']['parts'][0]['text']

        return jsonify({"answer": ai_answer})
    
    except requests.exceptions.HTTPError as http_err:
        print(f"AI 챗봇 HTTP 오류: {http_err}")
        print(f"응답 내용: {http_err.response.text}")
        error_details = http_err.response.json().get('error', {}).get('message', '알 수 없는 HTTP 오류')
        return jsonify({"error": f"AI API 오류: {error_details}"}), 500
    
    except Exception as e:
        print(f"AI 챗봇 기타 오류: {e}") 
        return jsonify({"error": f"AI 응답 처리 중 오류 발생: {e}"}), 500

# -----------------------------------------------------------------
# 학습 통계 API
# -----------------------------------------------------------------
@bp.get("/api/stats")
def api_get_stats():
    """학습 통계 조회"""
    return jsonify(get_dashboard_stats())

@bp.post("/api/stats/reset")
def api_reset_stats():
    """학습 통계 초기화"""
    reset_stats()
    return jsonify({"ok": True})

@bp.get("/api/weakness")
def api_get_weakness():
    """카테고리별 약점 분석"""
    return jsonify({"analysis": get_weakness_analysis()})

@bp.post("/api/weakness/reset")
def api_reset_weakness():
    """카테고리별 통계 초기화"""
    reset_category_stats()
    return jsonify({"ok": True})

# -----------------------------------------------------------------
# 북마크 API
# -----------------------------------------------------------------
@bp.get("/api/bookmarks")
def api_get_bookmarks():
    """북마크 목록 조회"""
    return jsonify({"items": load_bookmarks()})

@bp.post("/api/bookmarks/add")
def api_add_bookmark():
    """북마크 추가"""
    data = request.get_json(force=True) or {}
    question = data.get("q")
    answer = data.get("answer")
    explain = data.get("explain", "")
    
    if not question or not answer:
        return jsonify({"error": "문제와 정답은 필수입니다."}), 400
    
    success = add_bookmark(question, answer, explain)
    return jsonify({"ok": success, "message": "이미 북마크된 문제입니다." if not success else "북마크 추가 완료"})

@bp.post("/api/bookmarks/remove")
def api_remove_bookmark():
    """북마크 제거"""
    data = request.get_json(force=True) or {}
    question = data.get("q")
    
    if not question:
        return jsonify({"error": "문제를 지정해주세요."}), 400
    
    success = remove_bookmark(question)
    return jsonify({"ok": success})

@bp.post("/api/bookmarks/clear")
def api_clear_bookmarks():
    """모든 북마크 삭제"""
    clear_bookmarks()
    return jsonify({"ok": True})

@bp.get("/api/bookmarks/quiz")
def api_bookmarks_quiz():
    """북마크된 문제로 퀴즈 생성"""
    bookmarks = load_bookmarks()
    if not bookmarks:
        return jsonify({"items": []})
    
    # 북마크 문제를 주관식 형태로 변환
    items = []
    for bm in bookmarks:
        items.append({
            "q": bm["q"],
            "answer": bm["answer"],
            "explain": bm.get("explain", "")
        })
    
    random.shuffle(items)
    return jsonify({"items": items[:10]})  # 최대 10문제

# -----------------------------------------------------------------
# AI 문제 자동 생성 API
# -----------------------------------------------------------------
@bp.post("/api/generate/theory")
def api_generate_theory():
    """AI로 이론 문제 자동 생성"""
    data = request.get_json(force=True) or {}
    category = data.get("category", "데이터베이스")
    count = int(data.get("count", 5))
    
    try:
        questions = generate_theory_questions(category, count)
        if questions:
            success = save_generated_questions(questions, "theory")
            return jsonify({
                "ok": success,
                "count": len(questions),
                "questions": questions,
                "message": f"{len(questions)}개의 문제가 생성되었습니다." if success else "저장에 실패했습니다."
            })
        else:
            return jsonify({"ok": False, "message": "문제 생성에 실패했습니다."}), 500
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

@bp.post("/api/generate/code")
def api_generate_code():
    """AI로 코드 문제 자동 생성"""
    data = request.get_json(force=True) or {}
    language = data.get("language", "Python")
    count = int(data.get("count", 5))
    
    try:
        questions = generate_code_questions(language, count)
        if questions:
            success = save_generated_questions(questions, "code")
            return jsonify({
                "ok": success,
                "count": len(questions),
                "questions": questions,
                "message": f"{len(questions)}개의 코드 문제가 생성되었습니다." if success else "저장에 실패했습니다."
            })
        else:
            return jsonify({"ok": False, "message": "문제 생성에 실패했습니다."}), 500
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

@bp.post("/api/generate/batch")
def api_generate_batch():
    """여러 카테고리 문제를 한 번에 생성"""
    data = request.get_json(force=True) or {}
    categories = data.get("categories", ["운영체제", "데이터베이스", "네트워크"])
    count_per_category = int(data.get("count_per_category", 3))
    
    try:
        results = batch_generate_questions(categories, count_per_category)
        total = sum(results.values())
        return jsonify({
            "ok": True,
            "results": results,
            "total": total,
            "message": f"총 {total}개의 문제가 생성되었습니다."
        })
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)}), 500

# -----------------------------------------------------------------
# 학습 일지/메모 API
# -----------------------------------------------------------------

@bp.get("/api/notes")
def api_get_notes():
    """메모 목록 조회"""
    category = request.args.get("category")
    notes = get_notes_by_category(category)
    return jsonify({"ok": True, "notes": notes})

@bp.post("/api/notes")
def api_add_note():
    """새 메모 추가"""
    data = request.get_json(force=True) or {}
    title = data.get("title", "무제")
    content = data.get("content", "")
    category = data.get("category", "일반")
    
    if not content:
        return jsonify({"ok": False, "message": "내용을 입력해주세요."}), 400
    
    note = add_note(title, content, category)
    return jsonify({"ok": True, "note": note, "message": "메모가 저장되었습니다."})

@bp.put("/api/notes/<int:note_id>")
def api_update_note(note_id):
    """메모 수정"""
    data = request.get_json(force=True) or {}
    title = data.get("title")
    content = data.get("content")
    category = data.get("category")
    
    success = update_note(note_id, title, content, category)
    
    if success:
        return jsonify({"ok": True, "message": "메모가 수정되었습니다."})
    else:
        return jsonify({"ok": False, "message": "메모를 찾을 수 없습니다."}), 404

@bp.delete("/api/notes/<int:note_id>")
def api_delete_note(note_id):
    """메모 삭제"""
    success = delete_note(note_id)
    
    if success:
        return jsonify({"ok": True, "message": "메모가 삭제되었습니다."})
    else:
        return jsonify({"ok": False, "message": "메모를 찾을 수 없습니다."}), 404