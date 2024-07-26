from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import shutil
import natsort
import threading
import webbrowser

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

#파일 절대 경로 설정
enabling_list_path = os.path.join(os.getcwd(), 'enabling_list')
closing_list_path = os.path.join(os.getcwd(), 'closing_list')

# 브라우저 자동 오픈
def open_browser():
        # 지정된 시간(예: 1초) 후 브라우저를 엽니다.
        threading.Timer(1, webbrowser.open, args=['http://127.0.0.1:8000']).start()


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
            files_name = os.listdir(chapter_path)
            files_name = natsort.natsorted(files_name)
            for file_name in files_name:
                
                if file_name.endswith('.html'):
                    content_path = os.path.join(chapter_path,file_name)
                    with open(content_path,'r', encoding='utf-8') as f:
                        file_content = f.read()
                    chapter['content_file'].append(file_content)
        
        #{name : chapter_name1, content_file[file1, file2]} 추가
        contents.append(chapter)

    return contents

def move_old_files(src_dir_path, dst_dir_path):
    # 현재 시간
    now = datetime.now()

    # src_folder 내의 파일을 모두 읽음
    for filename in os.listdir(src_dir_path):
        file_path = os.path.join(src_dir_path, filename)

        # 파일인지 확인
        if os.path.isfile(file_path):
            file = open(file_path, 'r', encoding='utf-8')
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # closing_time 추출
            closing_time_tag = soup.find('small', class_='closing_time')
            if closing_time_tag:
                
                #공백제거 및 추출
                closing_time_str = closing_time_tag.text.strip()
                if closing_time_str:
                    closing_time = datetime.strptime(closing_time_str, '%Y-%m-%d %H:%M:%S')

                    # closing_time이 3일 이상 지났는지 확인 timedelta(days=3) timedelta(seconds=5)
                    if now - closing_time > timedelta(days=3):
                        # 파일을 dst_folder로 이동
                        file.close()
                        shutil.move(file_path, os.path.join(dst_dir_path, filename))





@app.route('/')
def index():
    src_dir_path = enabling_list_path
    dst_dir_path = closing_list_path
    '''혹시몰라 놔둠
    src_chapter_path = []
    dst_chapter_path = []

    for chapter_name in os.listdir(src_dir_path):
        src_chapter_path.append(os.path.join(src_dir_path, chapter_name))
        dst_chapter_path.append(os.path.join(dst_dir_path, chapter_name))

    print(f"src_chapter_path is {src_chapter_path[1]}")
    print(f"dst_chapter_path is {dst_chapter_path[1]}")

    for
    move_old_files(src_chapter_path[1],dst_chapter_path[1])
    '''
        

    #enabling_list에 있는 폴더에서 종결된거만 closing_list로 이동하기
    for root, dirs, files in os.walk(src_dir_path):

        # enabling_list의 상대경로 구하기
        rel_path = os.path.relpath(root, src_dir_path)

        # 목적지 위치 초기화
        dest_path = os.path.join(dst_dir_path, rel_path)

        # chapter(디렉토리) 없으면 생성
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        # 3일 지난거 이동
        move_old_files(root,dest_path)
        
    contents=show_screen(enabling_list_path)
    return render_template('index.html',contents=contents)

'''
@app.route('/create_chapter/', methods=['POST'])
def create_chapter():
    
    return render_template('index.html',chapters=chapters)
'''

@app.route('/create/', methods=['POST'])
def create_content():
    # 데이터 받기
    title = request.form.get('content-title')
    chapter = request.form.get('chapter-title')
    content_value = ''
    # 시간 초기화
    now = datetime.now()
    modified_time = now.strftime('%Y-%m-%d %H:%M:%S')

    # id 생성
    id_file= open('data/last_id.txt','r+')
    id = int(id_file.read().strip())
    id = id + 1

    id_file.seek(0)
    id_file.write(str(id))
    id_file.truncate()
    id_file.close()

    #mode 설정
    mode = 'blue'

    # content 양식에 데이터 추가
    content = render_template('content_struct.html', content_title=title, modified_time=modified_time, id=id, mode=mode,content_value=content_value)

    # enabling_list에 추가
    f = open(f'enabling_list/{chapter}/id_{id}.html', 'w', encoding='utf-8')
    f.write(content)
    
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
    modified_time = now.strftime('%Y-%m-%d %H:%M:%S')

    #content title 초기화
    content_title = request.form.get('content-title')

    #chapter title 초기화
    chapter = request.form.get('chapter')

    #mode 설정
    mode = 'blue'

    #파일 생성
    f = open(f'enabling_list/{chapter}/id_{id}.html','w', encoding='utf-8')
    f.write(render_template('content_struct.html', content_title=content_title, modified_time=modified_time, id=id, mode = mode,content_value=content_value))

    return redirect(url_for('index'))

@app.route("/close/", methods=['POST'])
def close():
    #데이터 받기
    #id 초기화
    id = request.form.get('id')

    #content 초기화
    content_value = request.form.get('content')

    #modified time 초기화
    modified_time = request.form.get('modified_time')
    
    # closing_time 체크
    # closing_time 초기화
    closing_time = request.form.get('closing_time')
    if (closing_time == ''):
        now = datetime.now()
        closing_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #mode 설정
        mode = 'red'
    else :
        closing_time = ''
        #mode 설정
        mode = 'blue'

    #content title 초기화
    content_title = request.form.get('content-title')

    #chapter title 초기화
    chapter = request.form.get('chapter')

    #파일 생성
    f = open(f'enabling_list/{chapter}/id_{id}.html','w', encoding='utf-8')
    f.write(render_template('content_struct.html', content_title=content_title, modified_time=modified_time, closing_time=closing_time, id=id, mode=mode,content_value=content_value))

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

def file_search(path, target):
    '''contents : [
    {name : chapter_name1, content_file : [file1, file2]},
    {name : chapter_name2, content_file : [file3, file4, file5]}
    ]
    '''
    contents= []
    
    return contents

@app.route("/search/", methods=['POST'])
def search():
    #데이터 받기
    #target 초기화
    target = request.form.get('target')

    # 서칭
    enabling_contents = []
    closing_contents = []
    '''contents : [
    {name : chapter_name1, content_file : [file1, file2]},
    {name : chapter_name2, content_file : [file3, file4, file5]}
    ]
    '''

    #enabling_list 읽기
    for chapter_name in os.listdir(enabling_list_path):
        chapter = {'name': chapter_name, 'content_file': []}
        chapter_path = os.path.join(enabling_list_path, chapter_name)

        # enabling_list 내 폴더 및 파일 읽기
        if os.path.isdir(chapter_path):
            enabling_files_name = os.listdir(chapter_path)
            enabling_files_name = natsort.natsorted(enabling_files_name)
            for file_name in enabling_files_name:
                if file_name.endswith('.html'):
                    content_path = os.path.join(chapter_path,file_name)

                    #target 검색
                    with open(content_path,'r', encoding='utf-8') as f:
                        file_content = f.read()
                    if target in file_content:
                        chapter['content_file'].append(file_content)
        enabling_contents.append(chapter)
    
    #closing_list 읽기
    for chapter_name in os.listdir(closing_list_path):
        chapter = {'name': chapter_name, 'content_file': []}
        chapter_path = os.path.join(closing_list_path, chapter_name)

        # closing_list 내 폴더 및 파일 읽기
        if os.path.isdir(chapter_path):
            closing_files_name = os.listdir(chapter_path)
            closing_files_name = natsort.natsorted(closing_files_name)
            for file_name in closing_files_name:
                if file_name.endswith('.html'):
                    content_path = os.path.join(chapter_path,file_name)

                    #target 검색
                    with open(content_path,'r', encoding='utf-8') as f:
                        file_content = f.read()
                    if target in file_content:
                        chapter['content_file'].append(file_content)
        closing_contents.append(chapter)
    
    #enabling_contents, closing_contents 합체
    mixed_dict = {}

    for content in enabling_contents + closing_contents:
        name = content["name"]
        if name not in mixed_dict:
            mixed_dict[name] = set(content["content_file"])
        else:
            mixed_dict[name].update(content["content_file"])

    # 최종형태로 변환
    contents = [{"name": name, "content_file": list(files)} for name, files in mixed_dict.items()]
    
    return render_template('index.html',contents=contents)


#메인
if __name__ == '__main__':
    open_browser()
    app.run(port=8000)
