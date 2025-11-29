# File: app/__init__.py
# -*- coding: utf-8 -*-
from flask import Flask, render_template

def create_app():
    """
    Flask 앱을 생성하고, 라우트를 등록합니다. (Application Factory)
    """
    app = Flask(__name__)

    # --- [수정] services.py가 사용할 설정값 추가 ---
    app.config["WRONG_FILE"] = "wrong_bank.json"  # services.py가 오답을 저장할 파일명
    app.config["REVIEW_MASTER_THRESHOLD"] = 2    # 오답 복습 완료(삭제) 기준 횟수

    # --- API 라우트(블루프린트) 등록 ---
    # quiz.py에 정의된 /api/... 경로들을 등록합니다.
    from .routes import quiz
    app.register_blueprint(quiz.bp)

    # --- [신규] 요약 페이지 라우트 등록 (이 2줄 추가) ---
    from .routes import summary
    app.register_blueprint(summary.bp)

    # --- [신규] 통계 페이지 라우트 등록 ---
    from .routes import stats
    app.register_blueprint(stats.bp)

    # --- 메인 페이지 라우트 ---
    @app.route('/')
    def home():
        """메인 홈페이지"""
        return render_template('home.html')
    
    @app.route('/quiz')
    def index():
        """퀴즈 페이지"""
        return render_template('index.html')

    return app