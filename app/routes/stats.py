# File: app/routes/stats.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

bp = Blueprint("stats", __name__)

@bp.route('/stats')
def stats_page():
    """
    학습 통계 대시보드 페이지
    """
    return render_template('stats.html')
