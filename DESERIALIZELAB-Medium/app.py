from flask import Flask, request, jsonify
import pickle
import base64

app = Flask(__name__)


@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Deserialization Lab - Load Settings</title>
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
                width: 600px;
                max-width: 90%;
                text-align: center;
            }
            h2 {
                color: #2c3e50;
                margin-bottom: 25px;
            }
            textarea {
                width: 90%;
                height: 120px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: monospace;
                font-size: 13px;
            }
            input[type="submit"] {
                margin-top: 15px;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 15px;
            }
            input[type="submit"]:hover {
                background-color: #2980b9;
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
            <h2>💾 Deserialization Lab - Load Settings</h2>
            <form method="POST" action="/load">
                <textarea name="data" placeholder="base64로 인코딩된 설정 데이터를 입력하세요" required></textarea><br>
                <input type="submit" value="설정 불러오기">
            </form>
            <div class="hint">
                <strong>📌 힌트:</strong> 서버는 전달받은 데이터를 base64 디코딩 후 그대로 역직렬화(pickle.loads)합니다.
            </div>
        </div>
    </body>
    </html>
    '''


@app.route("/load", methods=["POST"])
def load():
    data = request.form.get("data")
    if not data:
        json_body = request.get_json(silent=True) or {}
        data = json_body.get("data")

    if not data:
        return jsonify({"error": "data 파라미터가 필요합니다."}), 400

    try:
        raw = base64.b64decode(data)
        result = pickle.loads(raw)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
