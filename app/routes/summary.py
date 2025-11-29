# File: app/routes/summary.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from app.kb import KB  # app 폴더의 kb.py에서 KB 데이터를 가져옵니다.

bp = Blueprint("summary", __name__)

@bp.route('/kb-summary')
def kb_page():
    """
    kb.py의 모든 데이터를 kb_summary.html 템플릿으로 전달합니다.
    """
    return render_template('kb_summary.html', kb_data=KB)