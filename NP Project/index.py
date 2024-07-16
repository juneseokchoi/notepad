from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

'''
NP project
    ㄴ closing_list
    ㄴ enabling_list
        ㄴ chapter1
        ㄴ chapter2
        ㄴ ...
    ㄴ templates
        ㄴ main.html
    ㄴ index.py

'''



app= Flask(__name__)

#파일 경로 설정
enabling_list_path = os.path.join(os.getcwd(), 'enabling_list')

#screen 보여주기
def show_screen(path):
    '''contents : [
    {name : chapter_name1, content_file[file1, file2]},
    {name : chapter_name2, content_file[file3, file4, file5]}
    ]
    '''
    contents = []
    #enabling_list 읽기
    for chapter_name in os.listdir(path):
        chapter = {'name': chapter_name, 'content_file': []}
        chapter_path = os.path.join(path, chapter_name)

        # enabling_list 내 폴더 및 파일 읽기
        if os.path.isdir(chapter_path):
            for file_name in os.listdir(chapter_path):
                if file_name.endswith('.html'):
                    content_path = os.path.join(chapter_path,file_name)
                    with open(content_path,'r', encoding='utf-8') as f:
                        file_content = f.read()
                    chapter['content_file'].append(file_content)
        
        #{name : chapter_name1, content_file[file1, file2]} 추가
        contents.append(chapter)
    return contents


@app.route('/')
def index():
    contents=show_screen(enabling_list_path)
    return render_template('index.html',contents=contents)

'''
@app.route('/create_chapter/', methods=['POST'])
def create_chapter():
    
    return render_template('index.html',chapters=chapters)
'''

@app.route('/create-content/', methods=['POST'])
def create_content():
    # 데이터 받기
    title = request.form.get('content-title')
    chapter = request.form.get('chapter-title')
    content_value = ''
    # 시간 초기화
    now = datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')

    # id 생성
    id_file= open('data/last_id.txt','r+')
    id = int(id_file.read().strip())
    id = id + 1

    id_file.seek(0)
    id_file.write(str(id))
    id_file.truncate()
    id_file.close()

    # content 양식에 데이터 추가
    content = render_template('content_struct.html', content_title=title, time=time, id=id, content_value=content_value)

    # enabling_list에 추가
    f = open(f'enabling_list/{chapter}/id_{id}.html', 'w', encoding='utf-8')
    f.write(content)
    print(content)
    
    return redirect(url_for('index'))

@app.route("/save/", methods=['POST'])
def save():
    #데이터 받기
    #id 초기화
    id = request.form.get('id')

    #content 초기화
    content_value = request.form.get('content')

    # 저장시간 초기화
    now = datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')

    #content title 초기화
    content_title = request.form.get('content-title')

    #chapter title 초기화
    chapter = request.form.get('chapter')

    #파일 생성  타이틀도 들고와야함...
    f = open(f'enabling_list/{chapter}/id_{id}.html','w', encoding='utf-8')
    f.write(render_template('content_struct.html', content_title=content_title, time=time, id=id, content_value=content_value))

    return redirect(url_for('index'))

@app.route("/delete/", methods=['POST'])
def delete():
    #데이터 받기
    #id 초기화
    id = request.form.get('id')

    #chapter title 초기화
    chapter = request.form.get('chapter')
    
    #content 삭제
    os.remove(f'enabling_list/{chapter}/id_{id}.html')

    return redirect(url_for('index'))

app.run(port=8000,debug=True)
