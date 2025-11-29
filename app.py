# File: app.py
# -*- coding: utf-8 -*-
from app import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

app = create_app()

if __name__ == "__main__":
    # .env의 PORT가 있으면 사용, 없으면 5000
    import os
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
