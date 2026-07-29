from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET = "letmein"

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()


@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>JWT Lab - Medium</title>
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
                width: 640px;
                max-width: 90%;
            }
            h2 {
                color: #2c3e50;
                margin-bottom: 15px;
            }
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
            .hint {
                margin-top: 20px;
                font-size: 14px;
                color: #777;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔑 JWT Lab - Medium</h2>
            <p><code>/login</code>으로 로그인하면 <code>role: user</code> 권한의 JWT를 발급받습니다.</p>
            <p><code>/admin</code>은 <code>role: admin</code> 클레임을 가진 토큰만 flag를 반환합니다.</p>
            <div class="output">POST /login
Content-Type: application/json

{"username": "guest"}</div>
            <div class="output">GET /admin
Authorization: Bearer &lt;token&gt;</div>
            <div class="hint">
                <strong>📌 힌트:</strong> 로그인으로는 절대 admin 권한 토큰을 받을 수 없습니다.
                <br>curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "guest"}'
                <br>curl http://localhost:8000/admin -H "Authorization: Bearer &lt;token&gt;"
            </div>
        </div>
    </body>
    </html>
    '''


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "guest")

    token = jwt.encode({"username": username, "role": "user"}, SECRET, algorithm="HS256")
    return jsonify({"token": token})


@app.route("/admin")
def admin():
    auth = request.headers.get("Authorization", "")
    token = auth[7:] if auth.startswith("Bearer ") else auth

    if not token:
        return jsonify({"error": "missing token"}), 401

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"error": "invalid token"}), 401

    if payload.get("role") != "admin":
        return jsonify({"error": "forbidden - admin role required"}), 403

    return jsonify({"message": f"welcome, {payload.get('username')}", "flag": FLAG})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
