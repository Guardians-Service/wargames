from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Forensics Lab - Layered Evidence (High)</title>
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
                background-color: #ffffff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                width: 650px;
                max-width: 90%;
            }
            h2 { color: #2c3e50; margin-bottom: 15px; }
            p { font-size: 15px; color: #555; line-height: 1.6; }
            a.download-btn {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .box {
                background-color: #f9f9f9;
                padding: 15px;
                border-left: 5px solid #3498db;
                margin-top: 30px;
                border-radius: 5px;
            }
            code { background-color: #eee; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🕵️ Forensics Lab - Layered Evidence</h2>
            <p>압수한 서버에서 <code>evidence.bin</code> 파일 하나를 확보했습니다.
            확장자는 의미가 없습니다 - 실제 파일 종류는 바이트를 직접 확인해야 합니다.</p>
            <p><a class="download-btn" href="/evidence.bin" download>📦 evidence.bin 다운로드</a></p>
            <div class="box">
                <p><strong>📌 목표:</strong> 파일 안에 여러 겹으로 인코딩된 <code>FLAG{{...}}</code>를 복원하세요.</p>
                <p><strong>💡 힌트:</strong> <code>file evidence.bin</code>로 실제 포맷부터 확인해보세요. 한 겹씩 벗겨내야 합니다.</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/evidence.bin")
def evidence():
    return send_file("evidence.bin", mimetype="application/octet-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
