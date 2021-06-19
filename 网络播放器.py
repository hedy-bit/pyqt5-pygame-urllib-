# coding:utf-8

# from PyQt5 import QtCore,QtGui,QtWidgets
import sys
from urllib.request import urlretrieve

import pygame
import jsonpath
from mutagen import File
import time
import os
from PIL import Image, ImageDraw, ImageFilter

from PyQt5 import QtGui
from PyQt5.QtWidgets import QListWidget, QLabel, QListWidgetItem,QLineEdit, QComboBox
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
import qtawesome
import threading
import random
import requests

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

class PAThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(PAThread, self).__init__()

    def run(self):
        global urls
        global songs
        global name
        print ('type')
        print ('begin looking')
        url = 'https://defcon.cn/dmusic/'
        name = name
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'

        }
        urls = []
        songs = []
        if  int(page) == '' or int(page) < 1:
            pages = 2
        else:
            pages = int(page)
        print (pages)
        for a in range(1, pages):

            params = {'input': name,
                      'filter': 'name',
                      'type': type,
                      'page': a
                      }

            res = requests.post(url, params, headers=headers)
            html = res.json()

            for i in range(0, 10):
                try:
                    title = jsonpath.jsonpath(html, '$..title')[i]
                    author = jsonpath.jsonpath(html, '$..author')[i]
                    url1 = jsonpath.jsonpath(html, '$..url')[i]  # 取下载网址
                    lrc = jsonpath.jsonpath(html, '$..lrc')[i]  # 取歌词
                    print(title, author)
                    urls.append(url1)
                    songs.append(str(title) + ' - ' + str(author))
                    # self.textEdit.setText(lrc)  # 打印歌词
                    # print(lrc)
                except:
                    pass

        print(urls)
        print(songs)

        self.trigger.emit(str('finish'))


class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()

    def run(self):
        try:
            global number
            global path
            global downloading
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'}

            url1 = urls[num]
            print(url1)
            os.makedirs('music', exist_ok=True)
            number = number +1
            path = 'music\{}.mp3'.format(number)
            urlretrieve(url1, path)  # 下载函数的使用
            downloading = False
            self.trigger.emit(str('finish'))
        except:
            self.trigger.emit(str('nofinish'))


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.start()

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
        self.setFixedSize(960, 700)
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

        self.label = QLabel(self)
        self.label.setText("first line")
        self.label.setStyleSheet("color:white")
        self.label.setMaximumSize(310, 20)

        self.main_layout.addWidget(self.right_widget, 0, 20, 90, 90)  # 22右侧部件在第0行第3列，占8行9列
        self.down_layout.addWidget(self.label, 1, 0, 1, 1)
        self.main_layout.addWidget(self.left_widget, 0, 0, 90, 20)
        self.main_layout.addWidget(self.down_widget, 100, 0, 10, 110)
        self.main_layout.addWidget(self.close_widget, 0, 106, 1, 4)  # 左侧部件在第0行第0列，占1行3列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件


        self.listwidget = QListWidget(self)
        self.listwidget.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.right_layout.addWidget(self.listwidget, 3, 0, 100, 90)
        self.listwidget.setStyleSheet('''background-color:transparent''')

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
        self.left_layout.addWidget(self.label63, 0, 0, 2,1)

        self.shuru2 = QLineEdit("5")
        self.left_layout.addWidget(self.shuru2, 0, 1, 2, 1)
        self.shuru2.setStyleSheet('''
        {background-color:#6DDF6D;
        
        }
        ''')

        self.button_123 = QtWidgets.QPushButton("生效")
        self.button_123.clicked.connect(self.page)
        self.button_123.setStyleSheet(
            '''QPushButton{background:#3C3F41;border-radius:5px;}QPushButton:hover{background:#3C3F41;}''')
        self.left_layout.addWidget(self.button_123, 0, 2, 2, 2)

        self.label2 = QLabel(self)
        self.label2.setText("当前为顺序播放")
        self.label2.setStyleSheet("color:#6DDF6D")
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
        #self.label5.setScaledContents(True)
        pix_img = QtGui.QPixmap('./2.png')
        pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label5.setPixmap(pix)
        #self.label5.setMaximumSize(1,1)
        self.left_layout.addWidget(self.label5,2,0,2,4)

        self.label6 = QLabel(self)
        self.label6.setText("")
        self.label6.setStyleSheet("color:#6DDF6D")
        self.left_layout.addWidget(self.label6, 2, 0, 2, 2)

        self.label23 = QLabel(self)
        self.label23.setText("歌曲名")
        self.label23.setStyleSheet("color:#6DDF6D")
        self.right_layout.addWidget(self.label23, 0, 0, 1, 2)

        self.shuru = QLineEdit("")
        self.right_layout.addWidget(self.shuru, 0, 3, 1, 50)

        self.cb = QComboBox(self)
        #self.cb.setStyleSheet("background:#18171B")
        self.cb.addItems(['酷狗', '网易云','qq' ,'酷我','虾米','百度','一听'])
        self.right_layout.addWidget(self.cb, 0, 50, 1, 20)
        self.cb.currentIndexChanged[int].connect(self.print)
        '''
        self.cb.currentIndexChanged['网易云'].connect(type='netease')
        self.cb.currentIndexChanged['酷狗'].connect(type='kugou')
        self.cb.currentIndexChanged['酷我'].connect(type='kuwo')
        self.cb.currentIndexChanged['虾米'].connect(type='xiami')
        self.cb.currentIndexChanged['百度'].connect(type='baidu')
        self.cb.currentIndexChanged['一听'].connect(type='yiting')
        '''
        self.button_1 = QtWidgets.QPushButton("搜索")
        self.button_1.clicked.connect(self.correct)
        self.button_1.setStyleSheet(
                        '''
                        QPushButton{foreground:white;background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}
                        ''')
        self.right_layout.addWidget(self.button_1, 0, 73, 1, 5)

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
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#3FC89C'), "")
        self.console_button_2.clicked.connect(self.nextion)
        self.console_button_2.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#3FC89C', font=18), "")
        self.console_button_3.clicked.connect(self.pause)
        self.console_button_3.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-down', color='#3FC89C', font=18), "")
        self.console_button_4.clicked.connect(self.voicedown)
        self.console_button_4.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-up', color='#3FC89C', font=18), "")
        self.console_button_5.clicked.connect(self.voiceup)
        self.console_button_5.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.align-center', color='#3FC89C', font=18), "")
        self.console_button_6.clicked.connect(self.playmode)
        self.console_button_6.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

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

        #self.down_layout.addWidget(self.label1, 1, 0, 1, 2)
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
             QPushButton{border:none;color:white;}
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
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-left:1px solid white;
             border-top-left-radius:10px;
             border-bottom-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-right-radius:10px;
             }
             ''')

        self.close_widget.setStyleSheet('''
             QPushButton{border:none;color:white;}
             QPushButton#close_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#close_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#close_widget{
             background:#232C51;
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-left:1px solid white;
             border-top-left-radius:10px;
             border-bottom-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-right-radius:10px;
             }
             ''')
        self.right_widget.setStyleSheet('''
        
             QPushButton{border:none;color:white;}
             QPushButton#right_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#right_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#right_widget{
             color:#232C51;
             background:#191618;
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-right:1px solid white;
             border-top-left-radius:10px;
             border-bottom-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-right-radius:10px;
             }
             ''')

        self.down_widget.setStyleSheet('''
        QWidget#down_widget{
        color:#172940;
        background:#172940;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
        }
        QLabel#down_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    # 以下为窗口控制代码

    def page(self):
        global page
        page = self.shuru2.text()

    def print(self,i):
        global type
        print (i)
        if i ==0:
            type = 'kugou'
        elif i ==1:
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
        print (big)
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
                pygame.mixer.music.stop()
            except:
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
            sys.exit()


        else:
            event.ignore()

    # 以下为功能代码

    def correct(self):
        global name
        seaname = self.shuru.text()
        name = seaname
        print (type)
        print(seaname)
        self.pa(seaname,type)



    def pa(self,name,type):
        self.listwidget.clear()
        self.listwidget.addItem('搜索中')
        self.listwidget.item(0).setForeground(QtCore.Qt.white)
        self.work2 = PAThread()
        self.work2.start()
        self.work2.trigger.connect(self.seafinish)

    def seafinish(self,eds):
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

    def dis(self):
        pass



    def photo(self,num):
        try:
            audio = File(songs[num])
            mArtwork = audio.tags['APIC:'].data
            with open('ls.png', 'wb') as img:
                img.write(mArtwork)
            try:
                lsfile = './ls.png'
                safile = './1.png'
                draw(lsfile,safile)

                pix_img = QtGui.QPixmap('./1.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            except:
                print ('do error')
                pix_img = QtGui.QPixmap('./ls.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
        except:
            print('no picture')
            if  os.path.exists("2.png"):
                pix_img = QtGui.QPixmap('./2.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            else:
                try:
                    req = requests.get('https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fy.gtimg.cn%2Fmusic%2Fphoto_new%2FT001R300x300M000002ztBMe06cOx0.jpg%3Fmax_age%3D2592000&refer=http%3A%2F%2Fy.gtimg.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625464213&t=a30c07bda8c2ab7d8001a59353e936e0')

                    checkfile  = open('ls2.png','w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './ls2.png'
                    safile = './2.png'
                    draw(lsfile,safile)
                except:
                    print ('download error')
                    pix_img = QtGui.QPixmap('./2.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                    pass
                pass



    def bofang(self, num):
        print ('try bofang')
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
                pygame.mixer.stop()
            except:
                pass
            pygame.mixer.init()
            try:
                self.Timer = QTimer()
                self.Timer.start(500)
            except:
                pass


            try:
                self.label.setText('下载中')
                self.work = WorkThread()
                self.work.start()
                self.work.trigger.connect(self.display)
            except:
                print ('song download error')
                downloading = False
                pass




        except:
            time.sleep(0.1)
            print ('system error')
            #self.next()
            pass

    def display(self,sd):
        if sd == 'finish':
            self.label.setText(songs[num])
            print ('music\{}.mp3'.format(number))
            pygame.mixer.music.load('music\{}.mp3'.format(number))  # 载入音乐
            pygame.mixer.music.play()
            # 播放音乐
        else:
            self.label.setText('下载错误')

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
                if not pygame.mixer.music.get_busy() and pause == False and not downloading:
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
            pygame.mixer.music.stop()

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




    def change_func(self, listwidget):
        global num
        item = QListWidgetItem(self.listwidget.currentItem())
        print(item.text())
        # print (item.flags())
        num = int(listwidget.currentRow())
        # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
        self.label.setText(songs[num])
        print(listwidget.currentRow())
        self.bofang(num)

    def pause(self):
        global pause
        if pause:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#3FC89C', font=18))
            pause = False
        else:
            try:
                pygame.mixer.music.pause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.play', color='#F76677', font=18))
            pause = True




    def voiceup(self):
        print('up')
        global voice
        voice += 0.1
        if voice > 1:
            voice = 1
        pygame.mixer.music.set_volume(voice)
        self.label3.setText(str(pygame.mixer.music.get_volume()))

    def voicedown(self):
        print('down')
        global voice
        voice -= 0.1
        if voice < 0:
            voice = 0
        pygame.mixer.music.set_volume(voice)
        self.label3.setText(str(pygame.mixer.music.get_volume()))

    def shui(self):
        global num
        global songs
        q = int(len(songs) - 1)
        num = int(random.randint(1, q))
        try:
            print('shui')
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            self.label.setText(songs[num])
            self.bofang(num) # 播放音乐

        except:
            pass

    def next(self):
        print ('nexting')
        global num
        global songs
        if num == len(songs) - 1:
            print('冇')
            num = 0
        else:
            num = num + 1
        try:
            self.label.setText(songs[num])
            self.bofang(num)
        except:
            print ('next error')
            pass



    def always(self):
        try:
            self.bofang(num)
            self.label.setText(songs[num])

        except:
            pass

    def last(self):
        global num
        global songs
        if num == 0:
            print('冇')
            num = len(songs) - 1
        else:
            num = num - 1
        try:
            self.bofang(num)
            self.label.setText(songs[num])

        except:
            pass

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_A:  # 键盘某个键被按下时调用
            print('surpise')



def crop_max_square(pil_img):
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

def draw(lsfile,safile):
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

#啦啦啦啦啦啦啦啦啦，今天2021/6/1,儿童节快乐鸭[]~(￣▽￣)~*