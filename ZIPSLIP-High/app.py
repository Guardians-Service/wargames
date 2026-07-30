import json
import os
import uuid
import zipfile

from flask import Flask, jsonify, request

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(BASE_DIR, "themes")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")

os.makedirs(THEMES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"debug": False}, f)


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Zip Slip Lab - High</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                display: flex;
                justify-content: center;
                padding-top: 60px;
            }
            .box {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 480px;
            }
            h1 { font-size: 20px; color: #333; }
            code { background-color: #eee; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎨 테마 패키지 업로드</h1>
            <p>프로필 테마로 쓸 zip 패키지를 업로드하세요. 서버가 압축을 풀어 적용합니다.</p>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="theme" accept=".zip" required>
                <button type="submit">업로드</button>
            </form>
            <p style="margin-top:16px;">확인용: <code>GET /debug</code> (디버그 모드일 때만 정보를 보여줍니다)</p>
            <p style="margin-top:14px; font-size:13px; color:#888;">💡 zip 안 파일들의 경로, 서버가 정말 업로드 폴더 안으로만 제한하고 있을까요?</p>
        </div>
    </body>
    </html>
    """


@app.route("/upload", methods=["POST"])
def upload():
    uploaded = request.files.get("theme")
    if uploaded is None or uploaded.filename == "":
        return jsonify({"error": "no file uploaded"}), 400

    upload_id = uuid.uuid4().hex
    extract_dir = os.path.join(THEMES_DIR, upload_id)
    os.makedirs(extract_dir, exist_ok=True)

    zip_path = os.path.join(extract_dir, "package.zip")
    uploaded.save(zip_path)

    try:
        with zipfile.ZipFile(zip_path) as zf:
            # 취약점: zipfile의 안전한 extract()/extractall()을 쓰지 않고, 멤버 이름을
            # 직접 os.path.join으로 이어붙여 파일을 쓴다. extractall()은 엔트리 이름의
            # ".." 세그먼트를 걸러내지만, 이렇게 직접 경로를 조립하면 그 방어가 전혀
            # 적용되지 않아 엔트리 이름에 "../"가 들어 있으면 extract_dir 밖으로
            # 파일을 쓸 수 있다 (Zip Slip).
            for member in zf.infolist():
                if member.is_dir():
                    continue
                dest_path = os.path.join(extract_dir, member.filename)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with zf.open(member) as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())
    except zipfile.BadZipFile:
        return jsonify({"error": "invalid zip file"}), 400

    return jsonify({"message": "테마 적용됨", "theme_id": upload_id})


@app.route("/debug")
def debug():
    # 매 요청마다 파일을 새로 읽는다 - 캐시하지 않으므로 zip slip으로 덮어쓴 값이
    # 재시작 없이 바로 반영된다.
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        config = {"debug": False}

    if not config.get("debug"):
        return jsonify({"error": "debug mode is off"}), 403

    return jsonify({"debug": True, "flag": FLAG})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
