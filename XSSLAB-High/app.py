from flask import Flask, request, make_response
import re

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

# 필터: <script>...</script> 블록과 큰따옴표/작은따옴표로 감싼 onXXX="..." 이벤트
# 핸들러만 제거한다. 따옴표 없는 이벤트 핸들러(onerror=alert(1) 처럼 공백/따옴표가
# 없는 형태)는 이 정규식에 걸리지 않는다 - 그게 이 문제의 우회 포인트다.
SCRIPT_TAG = re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL)
QUOTED_EVENT_HANDLER = re.compile(r"""on[a-zA-Z]+\s*=\s*(["']).*?\1""", re.IGNORECASE)


def sanitize(raw: str) -> str:
    cleaned = SCRIPT_TAG.sub("", raw)
    cleaned = QUOTED_EVENT_HANDLER.sub("", cleaned)
    return cleaned


PAGE_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>XSS Lab - High (Filter Bypass)</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                display: flex;
                justify-content: center;
                padding-top: 60px;
            }}
            .box {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 480px;
            }}
            h1 {{ font-size: 20px; color: #333; }}
            textarea {{ width: 100%; height: 60px; }}
            input[type="submit"] {{
                margin-top: 10px;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .comment-box {{
                margin-top: 20px;
                padding: 12px;
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>📝 방명록</h1>
            <p>이 방명록은 <code>&lt;script&gt;</code> 태그와 따옴표로 감싼 이벤트 핸들러를 필터링합니다.</p>
            <form method="GET">
                <textarea name="comment" placeholder="댓글을 입력하세요"></textarea><br>
                <input type="submit" value="등록">
            </form>
            <div class="comment-box">{comment}</div>
            <p style="margin-top:14px; font-size:13px; color:#888;">💡 이 필터, 따옴표가 없는 속성값도 검사할까요?</p>
        </div>
    </body>
    </html>
"""


@app.route("/")
def index():
    comment = request.args.get("comment", "")
    resp = make_response(PAGE_TEMPLATE.format(comment=sanitize(comment)))
    # 매 방문마다 FLAG 쿠키를 새로 심는다 (XSSLAB-Cookie와 동일한 패턴).
    resp.set_cookie("FLAG", FLAG)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
