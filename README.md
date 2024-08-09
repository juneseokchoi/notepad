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
