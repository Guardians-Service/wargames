from flask import Flask, request
import requests

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()


@app.route("/")
def index():
    url = request.args.get("url", "")
    result = ""
    error = ""

    if url:
        try:
            resp = requests.get(url, timeout=3)
            result = resp.text[:1000]
        except Exception as e:
            error = str(e)

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SSRF Lab - URL Preview</title>
        <style>
            body {{
                background-color: #f4f6f8;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                width: 600px;
                max-width: 90%;
                text-align: center;
            }}
            h2 {{
                color: #2c3e50;
                margin-bottom: 25px;
            }}
            input[type="text"] {{
                padding: 10px;
                width: 60%;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 15px;
            }}
            input[type="submit"] {{
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 15px;
                margin-left: 10px;
            }}
            input[type="submit"]:hover {{
                background-color: #2980b9;
            }}
            .output {{
                margin-top: 30px;
                text-align: left;
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                font-family: monospace;
                white-space: pre-wrap;
                color: #333;
                max-height: 300px;
                overflow-y: auto;
            }}
            .error {{
                margin-top: 30px;
                text-align: left;
                background-color: #fdecea;
                color: #b71c1c;
                padding: 15px;
                border-radius: 5px;
                font-family: monospace;
                white-space: pre-wrap;
            }}
            .hint {{
                margin-top: 20px;
                font-size: 14px;
                color: #777;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔗 SSRF Lab - URL Preview</h2>
            <form method="GET" action="/">
                <input type="text" name="url" placeholder="예: https://example.com" required>
                <input type="submit" value="미리보기">
            </form>
            <div class="hint">
                <strong>📌 힌트:</strong> 서버가 대신 요청을 보내주는 서비스입니다. URL 검증이 전혀 없습니다.
            </div>
            {'<div class="output">' + result + '</div>' if result else ''}
            {'<div class="error">' + error + '</div>' if error else ''}
        </div>
    </body>
    </html>
    '''


@app.route("/internal/flag")
def internal_flag():
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return "Forbidden: this endpoint is only reachable from localhost.", 403
    return f"FLAG: {FLAG}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
