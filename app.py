from flask import Flask, request, render_template
from urllib.request import urlopen
from bs4 import BeautifulSoup
import openai 

app = Flask(__name__) 

# 기본 루트 경로에 대한 라우트 설정
@app.route('/', methods=['GET', 'POST'])



def index():
    if request.method == 'POST':
        # HTML 폼에서 'text' 필드에서 데이터를 가져옵니다.
        input_url = request.form['url']
        
        # url 입력받아 기사 본문 크롤링
        html = urlopen(input_url)
        bs = BeautifulSoup(html.read(), 'html.parser')

        text = bs.find('article', {'id':'dic_area'}).get_text()
        text = text.split('기자 = ')[-1]
        
        # 챗GPT
        openai.api_key = ''
        messages=[]
        content = f"'{text}'를 간략히 요약해줘"
        
        # 질문 저장
        messages.append({"role":"user", "content":content})
        
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, stream=True)
        
        summary=''
        
        for item in completion:
            if 'content' in item.choices[0].delta:
                summary+=item.choices[0].delta.content
                print(item.choices[0].delta.content)
            else:
                break
        
        return render_template('index.html', summary=summary)
    return render_template('index.html')

    

if __name__ == '__main__':
    app.run(debug=True)
