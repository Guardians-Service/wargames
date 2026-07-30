from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

conn = sqlite3.connect(":memory:", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
cur.executemany(
    "INSERT INTO users (id, username) VALUES (?, ?)",
    [(1, "guest"), (2, "alice"), (3, "bob"), (4, "carol"), (5, "dave")],
)
cur.execute("CREATE TABLE secrets (flag TEXT)")
cur.execute("INSERT INTO secrets (flag) VALUES (?)", (FLAG,))
conn.commit()


@app.route("/")
def index():
    return '''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>Blind SQL Injection Lab - High</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .box {
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 420px;
                }
                h1 { text-align: center; color: #333; font-size: 20px; }
                code {
                    background-color: #eee;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: monospace;
                }
                .output {
                    margin-top: 15px;
                    background-color: #f0f0f0;
                    padding: 12px;
                    border-radius: 5px;
                    font-family: monospace;
                    font-size: 13px;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div class="box">
                <h1>🔎 User Existence Checker</h1>
                <p>이 서비스는 <code>id</code> 값을 가진 유저가 존재하는지만 <code>true</code>/<code>false</code>로 알려줍니다.</p>
                <div class="output">GET /api/check?id=1
&#8594; {"exists": true}

GET /api/check?id=999
&#8594; {"exists": false}</div>
                <p style="margin-top:14px; font-size:13px; color:#888;">💡 <code>id</code>가 꼭 숫자 하나여야만 유효한 요청일까요?</p>
            </div>
        </body>
        </html>
    '''


@app.route("/api/check")
def check():
    user_id = request.args.get("id", "")
    query = f"SELECT id, username FROM users WHERE id = {user_id}"
    print("[DEBUG]", query)
    try:
        result = conn.execute(query).fetchone()
    except sqlite3.Error:
        # 에러 메시지를 절대 노출하지 않는다 - 참/거짓 신호만 준다 (블라인드).
        return jsonify({"exists": False})
    return jsonify({"exists": result is not None})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
