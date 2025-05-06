# Notepad Web Application

**Notepad**는 가볍고 간편하게 웹 기반으로 메모를 작성하고 관리할 수 있는 애플리케이션입니다. 이 프로젝트는 **Flask**를 사용하여 개발되었으며, 사용자가 작성한 메모를 **JSON 파일** 형식으로 저장하고 불러오는 기능을 제공합니다. 또한, 메모는 **3일 후 자동으로 숨김처리**되며, **파일 시스템**을 사용하여 데이터를 관리합니다.

## 주요 기능

- **📂 파일 시스템 기반 저장**
  데이터베이스 없이 **파일 시스템**을 사용하여 직접적인 수정과 백업이 가능합니다.

- **💾 JSON 기반 저장**
  메모는 chapter, mode, id, content_title, modified_time, closing_time, content 필드로 구성되어 저장됩니다.
  
- **🖥️ 모드 전환 기능(개🛠⚒인용/서버용)**
  사용자는 data/notepad.ini 설정파일을 통해 개인용, 서버용으로 전환이 가능합니다.
  
- **📄 메모 관리**
  사용자는 메모를 작성, 수정, 삭제, 검색이 가능하며 웹 인터페이스를 통해 쉽게 사용할수 있습니다.

- **⏳ 3일 뒤 자동 숨김**  
  종결된 메모는 **3일 뒤 자동으로 숨김 처리**가 됩니다. (파일은 closing_list로 이동합니다.)

- **💼 휴대성**  
  별도의 데이터베이스를 없이 사용하여 USB 등에 담아 사용할 수 있습니다.

- **⚙ 설정 파일 구성**  
  data/notepad.ini 설정파일을 통해 password, port, server 사용유무를 설정할 수 있습니다.

## 설치 방법

1. 이 프로젝트를 클론합니다:

   ```bash
   git clone https://github.com/yourusername/notepad.git
   cd notepad



///
from flask import Flask, render_template, request, redirect, url_for

import os

from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import shutil

import natsort

import threading

import webbrowser



아래 3개해야함

pip install Flask

pip install beautifulsoup4

pip install natsort


enabling_list 랑 closing_list 폴더만 만들고 안의 내용은 지워도 OK
그리고 enabling_list에 폴더를 생성하면 그게 chapter로 생성되고 closing_list에는 자동으로 생성
data의 last_id.txt로 마지막 id를 정하고 그위치의 2개의 html 파일은 필요없음. 구조를 확인하려고 만든것 이고 프로그램에 영향을 주지는 않음.
영향을 주는 파일은 templates에 들어가 있음. 
///
