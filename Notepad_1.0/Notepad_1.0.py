from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime, timedelta
import shutil
import configparser
import json
'''
NP project
ㄴ static
    ㄴ css
        ㄴ style.css
    ㄴ js
        ㄴ script.js
ㄴ data
    ㄴ notepad.ini

ㄴ enabling_list
    ㄴ chapter1
        ㄴ file1
        ㄴ file2
        ㄴ file3
    ㄴ chapter2
        ㄴ file4
        ㄴ file5
        ㄴ file6
ㄴ closing_list
    ㄴ chapter1
        ㄴ file1
        ㄴ file2
        ㄴ file3
    ㄴ chapter2
        ㄴ file4
        ㄴ file5
        ㄴ file6
ㄴ templates
    ㄴ main.html
    ㄴ login.html
ㄴ Notepad_1.0.py
'''

# conf setting
config = configparser.ConfigParser()
config.read('data/Notepad_1.0.ini', encoding='utf-8')
last_id = int(config['config']['last_id'])
port = int(config['config']['port'])
password = config['config']['password']
server = True if config['config']['server'].strip() == 'on' else False

app= Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=1)

#setting path
enabling_list_path = os.path.join(os.getcwd(), 'enabling_list')
closing_list_path = os.path.join(os.getcwd(), 'closing_list')


'''
contents : [
        {name : chapter_name1, content_file[{id:1,chapter:#1참고사항,content_title:제목,content:내용,mode=blue,modified_time:,closingtime:}, file2_content]},
        {name : chapter_name2, content_file[file3_content, file4_content, file5_content]}
        ]
        
        content_file = {id:1,chapter:#1참고사항,content_title:제목,content:내용,mode=blue,modified_time:"0000-00-00 00:00:00",closingtime:""}
'''

# make contents to showing
def make_contents(path):
    contents = []
    for chapter_name in os.listdir(path):
        chapter_result = {'name' : chapter_name,'content_file':[]}
        chapter_path = os.path.join(path,chapter_name)
        if os.path.isdir(chapter_path):
            files_name = os.listdir(chapter_path)
                        
            for file_name in files_name:
                if file_name.endswith('.json'):
                    content_path = os.path.join(chapter_path, file_name)
                    with open(content_path, 'r', encoding='utf-8') as f:
                        file_content = json.load(f)
                    chapter_result['content_file'].append(file_content)            
        chapter_result['content_file'] = sorted(chapter_result['content_file'], key=lambda x: x['id'])
        contents.append(chapter_result)
    return contents
                
def move_old_files(src_dir_path, dst_dir_path):
    # 현재 시간
    now = datetime.now()

    # src_folder 내의 파일을 모두 읽음
    for filename in os.listdir(src_dir_path):
        file_path = os.path.join(src_dir_path, filename)

        if filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data['closing_time']:
                closing_time = datetime.strptime(data['closing_time'], '%Y-%m-%d %H:%M:%S')
                if now - closing_time > timedelta(days=3):
                    # 파일을 dst_folder로 이동
                    shutil.move(file_path, os.path.join(dst_dir_path, filename)) 

@app.route('/login', methods=['POST'])
def login():
    password_input = request.form.get('password')
    if password_input == password:
        session['logged_in'] = True
    return redirect('/')


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    src_dir_path = enabling_list_path
    dst_dir_path = closing_list_path

    for chapter_name in os.listdir(src_dir_path):
        src_chapter_path = os.path.join(src_dir_path, chapter_name)
        dst_chapter_path = os.path.join(dst_dir_path, chapter_name)

        # 폴더인 경우만 처리
        if os.path.isdir(src_chapter_path):
            # 목적지 폴더 없으면 생성
            if not os.path.exists(dst_chapter_path):
                os.makedirs(dst_chapter_path)

            # 3일 지난 파일 이동
            move_old_files(src_chapter_path, dst_chapter_path)
        
    contents=make_contents(enabling_list_path)
    return render_template('main.html',contents=contents)


@app.route('/create/', methods=['POST'])
def create_content():
    # 데이터 받기
    title = request.form.get('content-title')
    chapter = request.form.get('chapter-title')
    content_value = ''
    
    # 시간 초기화
    now = datetime.now()
    modified_time = now.strftime('%Y-%m-%d %H:%M:%S')

    # conf 읽기
    config = configparser.ConfigParser()
    with open('data/notepad.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    
    # id 읽기
    last_id = int(config['config']['last_id'])
    last_id += 1
    

    content_data = {
        "id": last_id,
        "chapter": chapter,
        "content_title": title,
        "content": content_value,
        "mode": "blue",
        "modified_time": modified_time,
        "closing_time": ""
    }

    # enabling_list에 추가
    with open(f'enabling_list/{chapter}/id_{last_id}.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=4, ensure_ascii=False)

    # last_id 수정
    config['config']['last_id'] = str(last_id)
    with open('data/notepad.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    
    return redirect(url_for('index'))

@app.route("/save/", methods=['POST'])
def save():
    #id 초기화
    content_id = request.form.get('id')

    #content 초기화
    updated_content = request.form.get('content')

    # 저장시간 초기화
    now = datetime.now()
    modified_time = now.strftime('%Y-%m-%d %H:%M:%S')

    #mode 설정
    mode = 'blue'

    # 파일 탐색
    found_path = None
    for chapter_name in os.listdir('enabling_list'):
        file_path = os.path.join('enabling_list', chapter_name, f'id_{content_id}.json')
        if os.path.exists(file_path):
            found_path = file_path
            break

    if not found_path:
        for chapter_name in os.listdir('closing_list'):
            file_path = os.path.join('closing_list', chapter_name, f'id_{content_id}.json')
            if os.path.exists(file_path):
                found_path = file_path
                break

    if not found_path:
        return "내용이 비어 있습니다.", 400

    #파일 생성
    with open(found_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['content'] = updated_content
    data['modified_time'] = modified_time
    data['mode'] = mode

    with open(found_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return redirect(url_for('index'))

@app.route("/close/", methods=['POST'])
def close():
    #id 초기화
    content_id = request.form.get('id')
    found_path = None
    
    for chapter_name in os.listdir('enabling_list'):
        file_path = os.path.join('enabling_list', chapter_name, f'id_{content_id}.json')
        if os.path.exists(file_path):
            found_path = file_path
            with open(found_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data['mode'] == 'blue':
                now = datetime.now()
                data['closing_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                data['mode'] = 'red'
            else:
                data['closing_time'] = ''
                data['mode'] = 'blue'

            with open(found_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            break
        
    if not found_path:
        for chapter_name in os.listdir('closing_list'):
            file_path = os.path.join('closing_list', chapter_name, f'id_{content_id}.json')
            if os.path.exists(file_path):
                found_path = file_path
                with open(found_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['closing_time'] = ''
                data['mode'] = 'blue'
                new_path = os.path.join('enabling_list', chapter_name, f'id_{content_id}.json')
                with open(new_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                os.remove(found_path)
                break
    
    return redirect(url_for('index'))

@app.route("/delete/", methods=['POST'])
def delete():
    #id 초기화
    content_id = request.form.get('id')
    found_path = None

    for chapter_name in os.listdir('enabling_list'):
        file_path = os.path.join('enabling_list', chapter_name, f'id_{content_id}.json')
        if os.path.exists(file_path):
            found_path = file_path
            break

    if not found_path:
        for chapter_name in os.listdir('closing_list'):
            file_path = os.path.join('closing_list', chapter_name, f'id_{content_id}.json')
            if os.path.exists(file_path):
                found_path = file_path
                break

    os.remove(found_path)

    return redirect(url_for('index'))


@app.route("/search/", methods=['POST'])
def search():
    
    '''
    contents : [
    {name : chapter_name1, content_file : [file1_content, file2_content]},
    {name : chapter_name2, content_file : [file3_content, file4_content, file5_content]}
    ]
    '''
    contents = []
    
    #target 초기화
    target = request.form.get('target')

    #chapter 목록 받기
    chapter_names = os.listdir('enabling_list')

    # 서치필드
    search_fields = ['id', 'content_title', 'content', 'mode', 'modified_time', 'closing_time']

    for chapter_name in chapter_names:
        chapter_result = {'name': chapter_name, 'content_file': []}
        enabling_chapter = os.path.join('enabling_list', chapter_name)
        closing_chapter = os.path.join('closing_list', chapter_name)

        for filename in os.listdir(enabling_chapter):
            if filename.endswith('.json'):
                file_path = os.path.join(enabling_chapter, filename)
                with open(file_path,'r',encoding='utf-8') as f:
                    data = json.load(f)
                if any(target in str(data[field]) for field in search_fields):
                    chapter_result['content_file'].append(data)
        for filename in os.listdir(closing_chapter):
            if filename.endswith('.json'):
                file_path = os.path.join(closing_chapter, filename)
                with open(file_path,'r',encoding='utf-8') as f:
                    data = json.load(f)
                if any(target in str(data[field]) for field in search_fields):
                    chapter_result['content_file'].append(data)

        # content_file 리스트를 id 기준으로 정렬
        chapter_result['content_file'] = sorted(chapter_result['content_file'], key=lambda x: x['id'])
        contents.append(chapter_result)
                                
    return render_template('main.html',contents=contents)


#메인
if __name__ == '__main__':
    if server:
        #호스트 다 허용
        app.run(host='0.0.0.0',port=port)
    else:
        #실행시킨 pc만 허용
        app.run(port=port)
    
