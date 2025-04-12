# Notepad Web Application

**Notepad**는 가볍고 간편하게 웹 기반으로 메모를 작성하고 관리할 수 있는 애플리케이션입니다. 이 프로젝트는 **Flask**를 사용하여 개발되었으며, 사용자가 작성한 메모를 **HTML 파일** 형식으로 저장하고 불러오는 기능을 제공합니다. 또한, 메모는 **3일 후 자동으로 종결**되며, **파일 시스템**을 사용하여 데이터를 관리합니다.

## 주요 기능

- **📄 메모 저장**  
  사용자가 작성한 메모를 **HTML 파일** 형식으로 저장합니다.

- **⏳ 3일 뒤 자동 종결**  
  저장된 메모는 **3일 뒤 자동으로 종결** 상태로 전환됩니다. (파일은 삭제되지 않음)

- **📂 메모 불러오기**  
  저장된 메모를 **자동으로 불러와** 목록에 표시합니다.

- **💾 파일 시스템 기반 저장**  
  데이터베이스 없이 **파일 시스템**을 사용하여 메모를 저장하고 관리합니다. 이는 간단하고 가벼운 프로젝트를 위해 선택한 방식입니다.

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
