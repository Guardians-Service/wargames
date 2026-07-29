from flask import Flask, request, make_response, redirect

app = Flask(__name__)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

USERS = {
    1: {
        "username": "admin",
        "bio": f"저는 이 서비스의 관리자입니다. 저의 개인 메모: {FLAG}",
    },
    2: {
        "username": "guest",
        "bio": "안녕하세요! 그냥 평범한 게스트 계정입니다. 특별한 건 없어요.",
    },
}


@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>IDOR Lab - Easy</title>
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
            .login-container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 320px;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
                color: #333;
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            .hint {
                margin-top: 15px;
                font-size: 13px;
                color: #777;
                background-color: #f7f7f7;
                padding: 10px;
                border-radius: 5px;
            }
            .footer {
                text-align: center;
                margin-top: 15px;
                font-size: 12px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>내 프로필</h1>
            <form action="/login" method="GET">
                <label>Username</label>
                <input type="text" name="username" value="guest" required>
                <label>Password</label>
                <input type="password" name="password" value="guest" required>
                <input type="submit" value="Login">
            </form>
            <div class="hint">💡 테스트 계정: <code>guest</code> / <code>guest</code></div>
            <div class="footer">IDOR Lab - Easy</div>
        </div>
    </body>
    </html>
    '''


@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    if username == "guest" and password == "guest":
        resp = make_response(redirect("/profile"))
        resp.set_cookie("uid", "2")
        return resp

    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login Failed</title>
        </head>
        <body style="text-align:center;font-family:sans-serif;padding-top:50px;">
            <h3>❌ Login failed</h3>
            <p>Please <a href="/">try again</a>.</p>
        </body>
        </html>
    '''


@app.route("/profile")
def profile():
    cookie_uid = request.cookies.get("uid")
    if not cookie_uid:
        return redirect("/")

    requested_id = request.args.get("id", cookie_uid)

    try:
        requested_id = int(requested_id)
    except ValueError:
        return "<h3>❌ Invalid id</h3>", 400

    user = USERS.get(requested_id)
    if not user:
        return "<h3>❌ User not found</h3>", 404

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>내 프로필</title>
        <style>
            body {{
                background-color: #f0f4f8;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .profile-box {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                width: 420px;
            }}
            h2 {{
                color: #2c3e50;
            }}
            .field {{
                margin-top: 10px;
                padding: 10px;
                background-color: #f7f7f7;
                border-radius: 5px;
                word-wrap: break-word;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="profile-box">
            <h2>👤 프로필 (id={requested_id})</h2>
            <div class="field"><strong>Username:</strong> {user['username']}</div>
            <div class="field"><strong>Bio:</strong> {user['bio']}</div>
            <div class="footer">현재 조회 중인 id: {requested_id} (쿠키 uid={cookie_uid})</div>
        </div>
    </body>
    </html>
    '''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
