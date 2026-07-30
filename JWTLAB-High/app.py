import os
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "keys")

with open(os.path.join(KEYS_DIR, "default.key"), "rb") as f:
    DEFAULT_KEY = f.read()


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>JWT Lab - High (kid Injection)</title>
        <style>
            body {
                background-color: #f4f6f8;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                width: 660px;
                max-width: 90%;
            }
            h2 { color: #2c3e50; margin-bottom: 15px; }
            .output {
                margin-top: 20px;
                text-align: left;
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                font-family: monospace;
                white-space: pre-wrap;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔑 JWT Lab - High (kid Injection)</h2>
            <p>이 서비스는 로그인 시 <code>HS256</code>으로 서명된 JWT를 발급합니다. 토큰 헤더의
            <code>kid</code>(key id) 값으로 서버가 어떤 서명 키 파일을 쓸지 결정합니다.</p>
            <p><code>/admin</code>은 <code>role: admin</code> 클레임을 가진 유효한 토큰만 flag를 반환합니다.</p>
            <div class="output">POST /login
Content-Type: application/json

{"username": "guest"}</div>
            <div class="output">GET /admin
Authorization: Bearer &lt;token&gt;</div>
            <p style="margin-top:14px; font-size:13px; color:#888;">💡 <code>kid</code> 값, 서버가 파일 경로로 그대로 쓴다면 어떤 값들을 넣어볼 수 있을까요?</p>
        </div>
    </body>
    </html>
    """


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "guest")

    token = jwt.encode(
        {"username": username, "role": "user"},
        DEFAULT_KEY,
        algorithm="HS256",
        headers={"kid": "default.key"},
    )
    return jsonify({"token": token})


@app.route("/admin")
def admin():
    auth = request.headers.get("Authorization", "")
    token = auth[7:] if auth.startswith("Bearer ") else auth

    if not token:
        return jsonify({"error": "missing token"}), 401

    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401

    # 취약점: 헤더의 kid 값을 검증 없이 그대로 키 파일 경로에 이어붙인다.
    # kid가 "../app.py" 같은 상대 경로면 keys/ 디렉터리를 벗어나 임의 파일을
    # 서명 검증 키로 읽어버린다 (디렉터리 탈출을 통한 키 오라클).
    kid = header.get("kid", "default.key")
    key_path = os.path.normpath(os.path.join(KEYS_DIR, kid))

    try:
        with open(key_path, "rb") as f:
            verify_key = f.read()
    except OSError:
        return jsonify({"error": "unknown key id"}), 401

    try:
        payload = jwt.decode(token, key=verify_key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401

    if payload.get("role") != "admin":
        return jsonify({"error": "forbidden - admin role required"}), 403

    return jsonify({"message": f"welcome, {payload.get('username')}", "flag": FLAG})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
