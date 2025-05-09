## 소개
**Notepad_1.0**은 Flask 기반의 경량 웹 메모 애플리케이션으로, 브라우저에서 간편하게 메모를 작성하고 관리할 수 있도록 제작


## 개발 목표/ 기획 배경
 - 가볍고 휴대 가능한 웹 메모 도구 개발
 - 개인 메모부터 팀 협업까지 유연하게 사용할 수 있는 구조 설계


## 주요 기능

- **📂 파일 시스템 기반 저장**  
  데이터베이스 없이 **파일 시스템**을 사용하여 로컬디스크에 직접적인 수정과 백업이 가능합니다.

- **💾 JSON 기반 저장**  
  메모는 chapter, mode, id, content_title, modified_time, closing_time, content 필드로 구성되어 저장됩니다.
  
- **🖥️ 모드 전환 기능(개인용/서버용)**  
  사용자는 설정파일을 통해 개인용, 서버용으로 전환이 가능합니다.
  
- **📄 메모 관리**  
  사용자는 메모를 작성, 수정, 삭제, 검색이 가능하며 웹 인터페이스를 통해 쉽게 사용할수 있습니다.

- **⏳ 종결 기능**  
  종결된 메모는 **3일 뒤 자동으로 숨김 처리**가 됩니다. (파일은 closing_list로 이동합니다.)

- **💼 휴대성**  
  별도의 데이터베이스를 없이 사용하여 **USB** 등에 담아 사용할 수 있습니다.

- **⚙ 설정 파일 구성**  
  data/Notepad_1.0.ini 설정파일을 통해 password, port, server 사용유무를 설정할 수 있습니다.

## 기술 스택

- ### Backend 
    Python (Flask)

- ### Frontend 
    HTML, CSS, JavaScript

- ### Storage 
    JSON 파일 기반

- ### Config 
    INI 파일 기반 설정


## 프로젝트 구조

```
Notepad_1.0/
├── data/
│ └── Notepad_1.0.ini               # 설정 파일
├── static/                         # 정적 파일 (CSS, js)
├── enabling_list/                  # 활성화된 메모 저장위치
├── closing_list/                   # 종결된 메모 저장위치
├── templates/
│ ├── main.html                     # 메인 페이지
│ └── login.html                    # 로그인 페이지
├── Notepad_1.0.py                  # Flask 서버 실행 파일
└── README.md                       # 이 파일
```

## 사용 방법

1. data/Notepad_1.0.ini에서 설정을 server, port, password를 설정
   - server = on , server = off 로 설정 가능

2. enabling_list 안에 필요한 chapter를 폴더로 생성(ex #1 참고사항, #2 업무사항 ...)
    - 실행시 자동으로 enabling_list의 폴더가 closing_list에도 생겨 closing_list에 만들 필요 X

3. 실행 후 password 입력

4. 실행 후 +를 누르고 제목 입력

5. 내용 입력 후 저장
    - 이미지 저장가능
    - ctrl + s(저장), **ctrl + b**, *ctrl + i*, ctrl + u(밑줄) 가능

6. 종결 시 내용이 자동으로 닫히고 3일 후 안보임
    - 검색 시 종결된거까지 다 검색
    - content 윗부분 클릭시 닫기, 열기 가능

7. 삭제시 영구 삭제

8. 검색
    - 제목, 내용, 수정일, 종결일, id 등 다 검색 가능
    - red 검색시 종결만 검색(mode = 'red' 이기 때문)

## 실행화면
  - 로그인 화면
![image](https://github.com/user-attachments/assets/6b885b24-ab98-4191-898b-279185ede763)

  - 로그인 후 화면  
![image](https://github.com/user-attachments/assets/50372d02-0d39-4848-ba14-ebecb9503d80)


  - 종결시 빨간색으로 변환(3일 후 아예 안보임)  
![image](https://github.com/user-attachments/assets/520f93a4-c3c6-4003-ae87-6e0213fe0b28)


## 향후 계획
  - 안정성과 속도를 개선한 새로운 기능 추가 계획
  - 보안을 강화하고, 데이터베이스를 도입하여 2.0 버전 개발 고민중..
  
