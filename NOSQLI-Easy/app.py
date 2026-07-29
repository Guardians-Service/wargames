from flask import Flask, request, jsonify
import mongomock

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

client = mongomock.MongoClient()
db = client["labdb"]
users = db["users"]

users.insert_one({"username": "admin", "password": "S3cr3t_Adm1n_Pw!", "secret": FLAG})
users.insert_one({"username": "guest", "password": "guest123", "secret": "nothing to see here"})


@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NoSQL Injection Lab - Easy</title>
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
            <h2>🔐 NoSQL Injection Lab - Easy</h2>
            <p>이 서비스는 JSON body로 로그인 정보를 받는 API 로그인 기능을 제공합니다.</p>
            <div class="output">POST /login
Content-Type: application/json

{"username": "guest", "password": "guest123"}</div>
            <div class="hint">
                <strong>📌 힌트:</strong> 서버는 요청받은 값을 그대로 MongoDB 쿼리에 사용합니다. 예:
                <div class="output">curl -X POST http://localhost:8000/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "guest", "password": "guest123"}'</div>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    query = {"username": username, "password": password}
    print("[DEBUG]", query)
    user = users.find_one(query)

    if user:
        return jsonify({
            "result": "success",
            "username": user["username"],
            "secret": user["secret"],
        })

    return jsonify({"result": "fail", "message": "invalid username or password"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
