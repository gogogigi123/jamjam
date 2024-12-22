from flask import Flask, request, jsonify
import http.client
import json

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def home():
    return '''
        <h1>Instagram 스토리 다운로드</h1>
        <form action="/stories" method="post">
            Instagram 사용자 이름: <input type="text" name="username" required>
            <button type="submit">검색</button>
        </form>
    '''

# 스토리 데이터 조회
@app.route('/stories', methods=['POST'])
def get_stories():
    username = request.form['username']  # 사용자가 입력한 사용자 이름
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "aa02a54f05msh915f33bc92a0831p14978bjsn060cd1f86f30", # RapidAPI 키를 여기에 입력
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    conn.request("GET", f"/v1/stories?username_or_id_or_url={username}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))

    # 스토리 데이터 추출
    stories = response_json.get("data", {}).get("items", [])
    if not stories:
        return "<p>스토리가 없습니다.</p>"

    # HTML로 스토리 출력
    story_html = '<h2>사용자 스토리</h2>'
    for story in stories:
        story_url = story.get("image_versions", {}).get("items", [{}])[0].get("url")
        story_html += f'<p><img src="{story_url}" alt="스토리 이미지" width="200"></p>'
    return story_html

if __name__ == "__main__":
    app.run(debug=True)
