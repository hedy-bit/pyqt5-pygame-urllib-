# coding:utf-8

# from PyQt5 import QtCore,QtGui,QtWidgets
import ctypes
import inspect
import sys
from decimal import Decimal
from shutil import copyfile, rmtree
from urllib.request import urlretrieve

from bs4 import BeautifulSoup
from jsonpath import jsonpath
from mutagen import File
import time
import os
from PIL import Image, ImageDraw, ImageFilter

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QListWidgetItem, QLineEdit, QComboBox
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QMutex
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
import qtawesome
import threading
import random
import requests
from pygame import mixer

path = ''
number = 1
play = 'shun'
stop = False
num = 0
voice = 0.5
pause = False
big = False
music = []
urls = []
songs = []
type = 'kugou'
name = ''
downloading = False
page = 5
id = []
proxies = {}
tryed = 1
songed = []
urled = []
bo = ''
pic = []
picd = []
qmut = QMutex()
os.makedirs('music', exist_ok=True)

class PAThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(PAThread, self).__init__()

    def get_info(self, url):
        global proxies
        global tryed
        print('start get info')
        print(tryed)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/491.10.2623.122 Safari/537.36'
        }
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ranks = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(1)'.format(str(tryed)))
        titles = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(str(tryed)))
        times = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(str(tryed)))
        for rank, title, time in zip(ranks, titles, times):
            data = {
                'IP': rank.get_text(),
                'duan': title.get_text(),
                'time': time.get_text()
            }
            q = str('http://' + str(rank.get_text()) + '/' + str(title.get_text()))
            proxies = {
                'http': q
            }
            print(proxies)

    def run(self):
        qmut.lock()
        try:
            global urls
            global songs
            global name
            global songid
            global proxies
            global pic
            print('type')
            print('begin looking')
            url = 'https://defcon.cn/dmusic/'
            name = name
            self.get_info('https://www.kuaidaili.com/free/inha')
            print(proxies)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'

            }
            urls = []
            songs = []
            pic = []
            if int(page) == '' or int(page) < 1:
                pages = 2
            else:
                pages = int(page)
            print(pages)
            for a in range(1, pages):

                params = {'input': name,
                          'filter': 'name',
                          'type': type,
                          'page': a
                          }

                res = requests.post(url, params, headers=headers, proxies=proxies)
                html = res.json()

                for i in range(0, 10):
                    try:
                        title = jsonpath(html, '$..title')[i]
                        author = jsonpath(html, '$..author')[i]
                        url1 = jsonpath(html, '$..url')[i]  # 取下载网址
                        pick = jsonpath(html, '$..pic')[i]  # 取歌词
                        print(title, author)
                        urls.append(url1)
                        pic.append(pick)
                        songs.append(str(title) + ' - ' + str(author))
                        # self.textEdit.setText(lrc)  # 打印歌词
                        # print(lrc)
                    except:
                        pass

                print(urls)
                print(songs)
                self.trigger.emit(str('finish'))
        except:
            print('pa error')
            self.trigger.emit(str('unfinish'))
        qmut.unlock()


class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()

    def cbk(self, a, b, c):
        '''''回调函数
        @a:已经下载的数据块
        @b:数据块的大小
        @c:远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        # print   ('%.2f%%' % per)
        self.trigger.emit(str('%.2f%%' % per))

    def run(self):
        try:
            global number
            global path
            global downloading
            global pic
            proxies = {
                'http': 'http://124.72.109.183:8118',
                ' Shttp': 'http://49.85.1.79:31666'

            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'}
            try:
                try:
                    try:
                        aq = pic[num]
                        aqq = aq.split('/')

                    except:
                        pass

                    if type == 'kugou' and len(aqq) - 1 == 6:
                        aqqe = str(aqq[0]) + str('//') + str(aqq[2]) + str('/') + str(aqq[3]) + str('/') + str(
                            '400') + str('/') + str(aqq[5]) + str('/') + str(aqq[6])
                        print(aqqe)
                    elif type == 'netease' and len(aqq) - 1 == 4:
                        aqn = aq.split('?')
                        b = '?param=400x400'
                        aqqe = (str(aqn[0]) + str(b))
                        print(aqqe)
                    else:
                        aqqe = pic[num]
                    req = requests.get(aqqe)

                    checkfile = open('./music/ls1.png', 'w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './music/ls1.png'
                    safile = './music/back.png'
                    draw(lsfile, safile)
                except:
                    pass
                url1 = urls[num]
                print(url1)
                os.makedirs('music', exist_ok=True)
                number = number + 1
                path = 'music\{}.临时文件'.format(number)
                urlretrieve(url1, path, self.cbk)  # 下载函数的使用
                to = 'downloadmusic\{}.mp3'.format(songs[num])
                os.makedirs('downloadmusic', exist_ok=True)
            except:
                pass

            try:
                copyfile(path, to)
            except:
                pass
            downloading = False
            self.trigger.emit(str('finish'))

        except:
            self.trigger.emit(str('nofinish'))


class WorkThread2(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()

    def cbk(self, a, b, c):
        '''''回调函数
        @a:已经下载的数据块
        @b:数据块的大小
        @c:远程文件的大小
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        # print   ('%.2f%%' % per)
        self.trigger.emit(str('%.2f%%' % per))

    def run(self):
        try:
            global number
            global path
            global downloading
            proxies = {
                'http': 'http://124.72.109.183:8118',
                'http': 'http://49.85.1.79:31666'

            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'}
            try:

                if type == 'kugou':
                    aq = picd[num]
                    aqq = aq.split('/')
                    aqqe = str(aqq[0]) + str('//') + str(aqq[2]) + str('/') + str(aqq[3]) + str('/') + str('400') + str(
                        '/') + str(aqq[5]) + str('/') + str(aqq[6])
                    print(aqqe)
                else:
                    aqqe = picd[num]
                req = requests.get(aqqe)

                checkfile = open('./music/ls1.png', 'w+b')
                for i in req.iter_content(100000):
                    checkfile.write(i)

                checkfile.close()
                lsfile = './music/ls1.png'
                safile = './music/back.png'
                draw(lsfile, safile)

                url1 = urled[num]
                print(url1)
                os.makedirs('music', exist_ok=True)
                number = number + 1
                path = 'music\{}.临时文件'.format(number)
                urlretrieve(url1, path, self.cbk)  # 下载函数的使用
                to = 'downloadmusic\{}.mp3'.format(songed[num])
                os.makedirs('downloadmusic', exist_ok=True)
            except:
                pass

            try:
                copyfile(path, to)
            except:
                pass
            downloading = False
            self.trigger.emit(str('finish'))

        except:
            self.trigger.emit(str('nofinish'))


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start()

        try:
            icon_path = os.path.join(os.path.dirname(__file__), './logo.ico')

            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))  # 这是对的。
            self.setWindowIcon(icon)
        except:
            pass
        t1 = threading.Thread(target=self.action)
        t1.setDaemon(True)
        t1.start()

    def init_ui(self):
        global type
        self.setFixedSize(1025, 750)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.close_widget = QtWidgets.QWidget()  # 创建关闭侧部件
        self.close_widget.setObjectName('close_widget')
        self.close_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.close_widget.setLayout(self.close_layout)  # 设置左侧部件布局为网格

        self.left_widget = QtWidgets.QWidget()  # 创建左边侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.down_widget = QtWidgets.QWidget()  # 创建下面部件
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QtWidgets.QGridLayout()
        self.down_widget.setLayout(self.down_layout)  # 设置下侧部件布局为网格

        self.up_widget = QtWidgets.QWidget()  # 创建下面部件
        self.up_widget.setObjectName('up_widget')
        self.up_layout = QtWidgets.QGridLayout()
        self.up_widget.setLayout(self.up_layout)  # 设置下侧部件布局为网格

        self.label = QLabel(self)
        self.label.setText("还没有播放歌曲呢╰(*°▽°*)╯")
        self.label.setStyleSheet("color:white")
        self.label.setMaximumSize(310, 20)

        self.main_layout.addWidget(self.up_widget, 0, 0, 1, 110)

        self.main_layout.addWidget(self.left_widget, 1, 0, 90, 20)
        self.main_layout.addWidget(self.right_widget, 1, 20, 90, 90)  # 22右侧部件在第0行第3列，占8行9列
        self.main_layout.addWidget(self.down_widget, 100, 0, 10, 110)
        self.main_layout.addWidget(self.close_widget, 0, 105, 1, 5)  # 左侧部件在第0行第0列，占1行3列


        self.down_layout.addWidget(self.label, 1, 0, 1, 1)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(33, 20, 716, 471))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tab_layout = QtWidgets.QGridLayout()
        self.tab.setLayout(self.tab_layout)
        self.listwidget = QtWidgets.QListWidget(self.tab)
        self.listwidget.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.listwidget.setStyleSheet('''background-color:transparent''')
        self.listwidget.setObjectName("listWidget")
        self.tab_layout.addWidget(self.listwidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "搜索页")

        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab")
        self.tab2_layout = QtWidgets.QGridLayout()
        self.tab2.setLayout(self.tab2_layout)
        self.listwidget2 = QtWidgets.QListWidget(self.tab2)
        self.listwidget2.doubleClicked.connect(lambda: self.change_funcse(self.listwidget2))
        self.listwidget2.setStyleSheet('''background-color:transparent''')
        self.listwidget2.setObjectName("listWidget2")
        self.listwidget2.setContextMenuPolicy(3)
        self.tab2_layout.addWidget(self.listwidget2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "最近播放")

        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab")
        self.tab3_layout = QtWidgets.QGridLayout()
        self.tab3.setLayout(self.tab3_layout)
        self.listwidget3 = QtWidgets.QListWidget(self.tab3)
        self.listwidget3.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.listwidget3.setStyleSheet('''background-color:transparent''')
        self.listwidget3.setObjectName("listWidget3")
        self.tab3_layout.addWidget(self.listwidget3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab3, "喜爱的歌")

        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab")
        self.tab4_layout = QtWidgets.QGridLayout()
        self.tab4.setLayout(self.tab4_layout)
        self.listwidget4 = QtWidgets.QListWidget(self.tab4)
        self.listwidget4.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.listwidget4.setStyleSheet('''background-color:transparent''')
        self.listwidget4.setObjectName("listWidget4")
        self.tab4_layout.addWidget(self.listwidget4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab4, "歌词")

        self.right_layout.addWidget(self.tabWidget, 3, 0, 100, 90)
        self.tabWidget.setStyleSheet('''background-color:#191618;color:balck''')

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_visit.clicked.connect(self.big)
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(self.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.label63 = QLabel(self)
        self.label63.setText("加载页数")
        self.label63.setStyleSheet("color:#6DDF6D")
        self.left_layout.addWidget(self.label63, 0, 0, 2, 1)

        self.shuru2 = QLineEdit("5")
        self.left_layout.addWidget(self.shuru2, 0, 1, 2, 1)
        self.shuru2.setStyleSheet('''
             background-color:#2B2B2B;             
             color:white
        ''')

        self.button_123 = QtWidgets.QPushButton("确定")
        self.button_123.clicked.connect(self.page)
        self.button_123.setStyleSheet(
            '''QPushButton{background:#3C3F41;border-radius:5px;}QPushButton:hover{background:#F2BCAE;}''')
        self.left_layout.addWidget(self.button_123, 0, 2, 2, 2)

        self.label2 = QLabel(self)
        self.label2.setText("当前为顺序播放")
        self.label2.setStyleSheet("color:green")
        self.left_layout.addWidget(self.label2, 4, 0, 2, 2)

        self.label3 = QLabel(self)
        self.label3.setText("")
        self.label3.setStyleSheet("color:white")
        self.down_layout.addWidget(self.label3, 1, 3, 1, 1)

        self.label7 = QLabel(self)
        self.label7.setText("")
        self.label7.setStyleSheet("color:white")

        '''
        self.label1 = QLabel(self)
        self.label1.setText("first line")
        self.label1.setStyleSheet("color:white")
        '''

        self.label5 = QLabel(self)
        # self.label5.setScaledContents(True)
        pix_img = QtGui.QPixmap('./music/backdown.png')
        pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label5.setPixmap(pix)
        # self.label5.setMaximumSize(1,1)
        self.left_layout.addWidget(self.label5, 2, 0, 2, 8)

        self.label6 = QLabel(self)
        self.label6.setText("")
        self.label6.setStyleSheet("color:#6DDF6D")
        self.left_layout.addWidget(self.label6, 2, 0, 2, 2)

        self.label23 = QLabel(self)
        self.label23.setText("                 ")
        self.label23.setStyleSheet("color:#6DDF6D")
        self.up_layout.addWidget(self.label23, 0, 100, 1, 20)

        self.shuru = QLineEdit("")
        self.up_layout.addWidget(self.shuru, 0, 120, 1, 40)
        self.shuru.returnPressed.connect(self.correct)
        self.shuru.setStyleSheet('''
             background-color:#2E2B2D;             
             color:white
        ''')

        self.label23 = QLabel(self)
        self.label23.setText("     软件")
        self.label23.setStyleSheet("color:#6DDF6D")
        self.up_layout.addWidget(self.label23, 0, 160, 1, 10)

        self.label61 = QLabel(self)
        self.label61.setText("")
        self.label61.setStyleSheet("color:#6DDF6D")
        self.up_layout.addWidget(self.label61, 0, 200, 1, 50)

        self.cb = QComboBox(self)
        self.cb.setStyleSheet('''QComboBox{
        background-color:#2E2B2D;
        color:white
        }''')
        self.cb.addItems(['酷狗', '网易云', 'qq', '酷我', '虾米', '百度', '一听'])
        self.up_layout.addWidget(self.cb, 0, 180, 1, 30)
        self.cb.currentIndexChanged[int].connect(self.print)

        '''
        self.cb.currentIndexChanged['网易云'].connect(type='netease')
        self.cb.currentIndexChanged['酷狗'].connect(type='kugou')
        self.cb.currentIndexChanged['酷我'].connect(type='kuwo')
        self.cb.currentIndexChanged['虾米'].connect(type='xiami')
        self.cb.currentIndexChanged['百度'].connect(type='baidu')
        self.cb.currentIndexChanged['一听'].connect(type='yiting')
        '''
        self.button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='white'), "")
        self.button_1.clicked.connect(self.correct)
        self.button_1.setStyleSheet(
            '''
            QPushButton{color:white;border-radius:5px;}QPushButton:hover{background:green;}
            ''')
        self.up_layout.addWidget(self.button_1, 0, 155, 1, 5)

        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_process_bar.setValue(49)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#3FC89C'), "")
        self.console_button_1.clicked.connect(self.last)
        self.console_button_1.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#3FC89C'), "")
        self.console_button_2.clicked.connect(self.nextion)
        self.console_button_2.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#3FC89C', font=18), "")
        self.console_button_3.clicked.connect(self.pause)
        self.console_button_3.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-down', color='#3FC89C', font=18), "")
        self.console_button_4.clicked.connect(self.voicedown)
        self.console_button_4.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-up', color='#3FC89C', font=18), "")
        self.console_button_5.clicked.connect(self.voiceup)
        self.console_button_5.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.align-center', color='#3FC89C', font=18), "")
        self.console_button_6.clicked.connect(self.playmode)
        self.console_button_6.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3.setIconSize(QtCore.QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 1)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 3)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 2)
        self.right_playconsole_layout.addWidget(self.console_button_4, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_5, 0, 4)
        self.right_playconsole_layout.addWidget(self.console_button_6, 0, 5)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

        self.down_layout.addWidget(self.right_process_bar, 0, 0, 1, 4)  # 第0行第0列，占8行3列
        # 第0行第0列，占8行3列

        self.down_layout.addWidget(self.label7, 1, 2, 1, 1)

        # self.down_layout.addWidget(self.label1, 1, 0, 1, 2)
        self.down_layout.addWidget(self.right_playconsole_widget, 1, 0, 1, 4)
        self.right_process_bar.setStyleSheet('''
            QProgressBar::chunk {
                background-color: #F76677;
            }
        ''')

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.left_widget.setStyleSheet('''
             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#left_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#left_widget{
             background:#2B2B2B;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-left:1px solid #222225;

             }
             ''')

        self.up_widget.setStyleSheet('''
             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#left_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#up_widget{
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #AD2121;
             border-left:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             }
             ''')

        self.close_widget.setStyleSheet('''
             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#close_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#close_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#close_widget{
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #AD2121;
             border-left:1px solid #222225;
             border-right:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             }
             ''')
        self.right_widget.setStyleSheet('''

             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#right_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#right_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#right_widget{
             color:#D0D0D0;
             background:#191618;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-right:1px solid #222225;
             }
             ''')

        self.down_widget.setStyleSheet('''
        QWidget#down_widget{
        color:#D0D0D0;
        background:#222225;
        border-bottom:1px solid #222225;
        border-right:1px solid #222225;
        border-top:1px solid #222225;
        border-bottom-right-radius:10px;
        border-bottom-left-radius:10px;
        }
        QLabel#down_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    # 以下为窗口控制代码

    # 创建右键菜单
    def rightMenuShow(self, x, y):
        item = self.listwidget2.itemAt(x, y)
        self.listwidget2.removeItemWidget(self.listwidget2.takeItem(self.listwidget2.row(item)))

    def page(self):
        global page
        page = self.shuru2.text()

    def print(self, i):
        global type
        print(i)
        if i == 0:
            type = 'kugou'
        elif i == 1:
            type = 'netease'
        elif i == 2:
            type = 'qq'
        elif i == 3:
            type = 'kuwo'
        elif i == 4:
            type = 'xiami'
        elif i == 5:
            type = 'baidu'
        elif i == 7:
            type = 'yiting'

    def big(self):
        global big
        print(big)
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False
        # print (windowState())

    def close(self):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'确定退出?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            close = True
            try:
                mixer.music.stop()
            except:
                pass
            try:
                rmtree('music')
            except:
                print ('delete error')
                pass
            sys.exit()

        else:
            pass

    def mini(self):

        self.showMinimized()

    def mousePressEvent(self, event):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        # if event.button()==QtWidgets.QPushButton:
        self.m_flag = True
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        # if QtWidgets.QPushButton and self.m_flag:
        self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = False

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'是否退出?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                mixer.stop()
            except:
                pass
            try:
                rmtree('music')
            except:
                pass
            sys.exit()


        else:
            event.ignore()

    # 以下为功能代码

    def start(self):
        try:
            if not os.path.exists("./music/backdown.png"):
                try:
                    req = requests.get('https://t7.baidu.com/it/u=1620952818,4218424235&fm=193&f=GIF')

                    checkfile = open('./music/ls2.png', 'w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './music/ls2.png'
                    safile = './music/backdown.png'
                    draw(lsfile, safile)
                    pix_img = QtGui.QPixmap('./music/backdown.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                except:
                    print('download error')
                    pass
        except:
            pass

    def correct(self):
        global name

        seaname = self.shuru.text()
        name = seaname
        print(type)
        print(seaname)
        self.pa(seaname, type)

    def pa(self, name, type):
        global tryed
        self.listwidget.clear()
        self.listwidget.addItem('搜索中')
        self.listwidget.item(0).setForeground(QtCore.Qt.white)
        try:
            self.work2 = PAThread()
            self.work2.start()
            self.work2.trigger.connect(self.seafinish)
        except:
            tryed = tryed + 1
            self.listwidget.addItem('貌似没网了呀`(*>﹏<*)′,再试一遍吧~')
            self.listwidget.item(0).setForeground(QtCore.Qt.white)

    def seafinish(self, eds):
        global tryed
        try:
            if eds == 'finish':
                self.listwidget.clear()
                if songs == []:
                    self.listwidget.clear()
                    self.listwidget.addItem('歌曲搜索失败，请再试一下其他的软件选项,建议使用酷狗')
                    self.listwidget.item(0).setForeground(QtCore.Qt.white)
                else:
                    r = 0
                    for i in songs:
                        # self.listwidget.addItem(i)#将文件名添加到listWidget

                        self.listwidget.addItem(i)
                        self.listwidget.item(r).setForeground(QtCore.Qt.white)
                        r = r + 1
            else:
                print('似乎没网了呀`(*>﹏<*)′')
                self.listwidget.clear()
                self.listwidget.addItem('似乎没网了呀`(*>﹏<*)′')
                self.listwidget.item(0).setForeground(QtCore.Qt.white)
                print('tryed:{}'.format(tryed))
                tryed = tryed + 1
                print('tryed:{}'.format(tryed))
        except:
            print('finisherror')
            pass

    def dis(self):
        pass

    def photo(self, num):
        try:
            audio = File(songs[num])
            mArtwork = audio.tags['APIC:'].data
            with open('./music/ls.png', 'wb') as img:
                img.write(mArtwork)
            try:
                lsfile = './music/ls.png'
                safile = './music/1.png'
                draw(lsfile, safile)

                pix_img = QtGui.QPixmap('./music/1.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            except:
                print('do error')
                pix_img = QtGui.QPixmap('./music/ls.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
        except:
            print('no picture')
            if os.path.exists("./music/backdown.png"):
                pix_img = QtGui.QPixmap('./music/backdown.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            else:
                try:
                    req = requests.get('https://t7.baidu.com/it/u=1620952818,4218424235&fm=193&f=GIF')
                    checkfile = open('./music/ls2.png', 'w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './music/ls2.png'
                    safile = './music/backdown.png'
                    draw(lsfile, safile)
                    pix_img = QtGui.QPixmap('./music/backdown.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                except:
                    print('download error')
                    pix_img = QtGui.QPixmap('./music/2.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                    pass
                pass

    def bofang(self, num, bo):
        print('try bofang')
        try:
            import urllib
            global pause
            global songs
            global music
            global downloading
            downloading = True
            self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#F76677', font=18))
            pause = False
            # QMessageBox.information(self, "ListWidget", "你选择了: "+item.text())# 显示出消息提示框
            try:
                mixer.stop()
            except:
                pass
            mixer.init()
            try:
                self.Timer = QTimer()
                self.Timer.start(500)
            except:
                pass

            try:
                self.label.setText('正在寻找文件...')
                if bo == 'boed':
                    self.work = WorkThread2()
                else:
                    self.work = WorkThread()
                self.work.start()
                self.work.trigger.connect(self.display)
            except:
                print('song download error')
                downloading = False
                pass




        except:
            time.sleep(0.1)
            print('system error')
            # self.next()
            pass

    def display(self, sd):
        # print ('zhi',sd)
        global pause
        global songed
        global urled
        if sd == 'finish':
            try:
                if bo == 'boing':
                    self.label.setText(songs[num])
                else:
                    self.label.setText(songed[num])
                try:
                    pix_img = QtGui.QPixmap('./music/back.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                except:
                    pix_img = QtGui.QPixmap('./music/backdown.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                print('music\{}.临时文件'.format(number))
                mixer.music.load('music\{}.临时文件'.format(number))  # 载入音乐
                mixer.music.play()
                self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#F76677', font=18))
                pause = False
                if bo == 'boing':
                    songed.append(songs[num])
                    urled.append(urls[num])
                    picd.append(pic[num])
                    r = 0
                    self.listwidget2.clear()
                    for i in songed:
                        # self.listwidget.addItem(i)#将文件名添加到listWidget

                        self.listwidget2.addItem(i)
                        self.listwidget2.item(r).setForeground(QtCore.Qt.white)
                        r = r + 1
                else:
                    pass
                # 播放音乐
            except:
                pass
        elif sd == 'nofinish':
            self.label.setText('下载错误')
        else:
            self.label.setText('加速下载中,已完成{}'.format(sd))

    def playmode(self):
        global play
        try:
            if play == 'shun':
                play = 'shui'
                print('随机播放')
                self.label2.setText("当前为随机播放")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.random', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')
                    pass

                # self.left_shui.setText('切换为单曲循环')
            elif play == 'shui':
                play = 'always'
                print('单曲循环')
                self.label2.setText("当前为单曲循环")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.retweet', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')

                # self.left_shui.setText('切换为顺序播放')
            elif play == 'always':
                play = 'shun'
                print('顺序播放')
                self.label2.setText("当前为顺序播放")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.align-center', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')

                # self.left_shui.setText('切换为随机播放')
        except:
            print('error')
            pass

    def action(self):
        a = 1
        global num
        while a < 2:
            # print ('checking')
            try:
                time.sleep(1)
                if not mixer.music.get_busy() and pause == False and not downloading:
                    if play == 'shun':
                        print('shuning')
                        self.next()
                    elif play == 'shui':
                        print('shuiing')
                        self.shui()
                    elif play == 'always':
                        print('alwaysing')
                        self.always()

            except:
                print('no')
                pass
        else:
            mixer.music.stop()

    def nextion(self):

        try:
            if play == 'shun':
                print('shuning')
                self.next()
            elif play == 'shui':
                print('shuiing')
                self.shui()
            elif play == 'always':
                print('alwaysing')
                self.next()

        except:
            print('no')
            pass

    def change_funcse(self, listwidget):
        global downloading
        global bo
        bo = 'boed'
        if downloading:
            try:

                print('stoped downloading')
                downloading = False
            except:
                print('stoped downloading')
                downloading = False
                print('can not stop')
                pass
        else:
            try:
                global num
                item = QListWidgetItem(self.listwidget.currentItem())
                print(item.text())
                # print (item.flags())
                num = int(listwidget.currentRow())
                # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
                self.label.setText(songed[num])
                print(listwidget.currentRow())
                self.bofang(num, bo)
            except:
                downloading = False
                pass

    def change_func(self, listwidget):
        global downloading
        global bo
        bo = 'boing'
        if downloading:
            try:
                self.你妈死了.stop()
            except:
                print('can not stop')
                pass
        else:
            try:
                global num
                item = QListWidgetItem(self.listwidget.currentItem())
                print(item.text())
                # print (item.flags())
                num = int(listwidget.currentRow())
                # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
                self.label.setText(songs[num])
                print(listwidget.currentRow())
                self.bofang(num, bo)
            except:
                downloading = False
                pass

    def pause(self):
        global pause
        if pause:
            try:
                mixer.music.unpause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#3FC89C', font=18))
            pause = False
        else:
            try:
                mixer.music.pause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.play', color='#F76677', font=18))
            pause = True

    def voiceup(self):
        try:
            print('up')
            global voice
            voice += 0.1
            if voice > 1:
                voice = 1
            mixer.music.set_volume(voice)
            k = Decimal(voice).quantize(Decimal('0.00'))
            self.label3.setText('音量：{}'.format(str(k * 100) + '%'))
        except:
            pass

    def voicedown(self):
        try:
            print('down')
            global voice
            voice -= 0.1
            if voice < 0:
                voice = 0
            mixer.music.set_volume(voice)
            k = Decimal(voice).quantize(Decimal('0.00'))
            self.label3.setText('音量：{}'.format(str(k * 100) + '%'))
        except:
            pass

    def shui(self):
        global num
        global songs
        if bo == 'boing':
            q = int(len(songs) - 1)
            num = int(random.randint(1, q))
        else:
            q = int(len(songed) - 1)
            num = int(random.randint(0, q))

        try:
            print('shui')
            mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            if bo == 'boing':
                self.label.setText(songs[num])
            else:
                self.label.setText(songed[num])
            self.bofang(num, bo)  # 播放音乐

        except:
            pass

    def next(self):
        print('nexting')
        global num
        global songs
        print(bo)
        if bo == 'boing':
            if num == len(songs) - 1:
                print('冇')
                num = 0
            else:
                num = num + 1
        else:
            if num == len(songed) - 1:
                print('冇')
                num = 0
            else:
                num = num + 1
        try:
            if bo == 'boing':
                self.label.setText(songs[num])
            else:
                self.label.setText(songed[num])
            self.bofang(num, bo)
        except:
            print('next error')
            pass

    def always(self):
        try:
            if bo == 'boing':
                self.label.setText(songs[num])
            else:
                self.label.setText(songed[num])
            self.bofang(num, bo)  # 播放音乐

        except:
            pass

    def last(self):
        global num
        global songs
        if bo == 'boing':
            if num == 0:
                print('冇')
                num = len(songs) - 1
            else:
                num = num - 1
        else:
            if num == 0:
                print('冇')
                num = len(songed) - 1
            else:
                num = num - 1
        try:
            if bo == 'boing':
                self.label.setText(songs[num])
            else:
                self.label.setText(songed[num])
            self.bofang(num, bo)  # 播放音乐

        except:
            pass

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_A:  # 键盘某个键被按下时调用
            print('surpise')


def crop_max_square(pil_img): \
        return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result


def draw(lsfile, safile):
    markImg = Image.open(lsfile)
    thumb_width = 600

    im_square = crop_max_square(markImg).resize((thumb_width, thumb_width), Image.LANCZOS)
    im_thumb = mask_circle_transparent(im_square, 0)
    im_thumb.save(safile)
    os.remove(lsfile)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# 啦啦啦啦啦啦啦啦啦，今天2021/6/1,儿童节快乐鸭[]~(￣▽￣)~*
