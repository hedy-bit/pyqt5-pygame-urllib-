

## 全部源码在[https://github.com/hedy-bit/pyqt5-pygame-urllib-](https://github.com/hedy-bit/pyqt5-pygame-urllib-)

先上效果图
![image](https://user-images.githubusercontent.com/78191612/125190340-267e7100-e26f-11eb-84de-3fd6ecee0d4c.png)

之前没事干，看windows10自带的播放器有一(亿)点点不顺眼，然后想写一个播放器，
正好有学了点pyqt5，又正好学了一点爬虫，然后就整了个播音乐播放器，耗时4天，，可以爬网易云，酷狗，qq，酷我，现在差不多也算是最终版本了吧，

这个是爬虫版本：[https://github.com/hedy-bit/pyqt5-pygame-urllib-](https://github.com/hedy-bit/pyqt5-pygame-urllib-)
这个是离线版本：[离线播放器链接](https://blog.csdn.net/oys19812007/article/details/116886015?spm=1001.2014.3001.5501)
如果接下来有时间的话也会继续更新下去






快不多说，先上代码

**首先是爬取搜索的歌曲，歌手和url，由于要使用多线程，所以新开了一个类**
```python
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
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210619203338714.png)
然后就是从爬取的url下载歌曲，由于我设计了两个歌单，所以我写了两个类

```python
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
```
下面就是QListwidge的点击和播放模块

```python
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
                self.label.setText('下载中')#调用开头的多线程下载歌曲
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
	#用于接收返回的信号
    def display(self,sd):
        if sd == 'finish':
            self.label.setText(songs[num])
            print ('music\{}.mp3'.format(number))
            pygame.mixer.music.load('music\{}.mp3'.format(number))  # 载入音乐
            pygame.mixer.music.play()
            # 播放音乐
        else:
            self.label.setText('下载错误')
```
下面是双击播放和上一首还有下一首

```python
	#QlistWidget的双击事件
    def change_func(self, listwidget):
        global num
        item = QListWidgetItem(self.listwidget.currentItem())
        print(item.text())
        
        num = int(listwidget.currentRow())
        
        self.label.setText(songs[num])
        print(listwidget.currentRow())
        self.bofang(num)
		
	#下一首按钮
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

	
```
下面自动播放，有循环，随机和单曲循环，加上下一首，上一首，

```python
	#随机播放
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
	#下一首
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


	#单曲循环
    def always(self):
        try:
            self.bofang(num)
            self.label.setText(songs[num])

        except:
            pass
	#上一首
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
```
下面是播放模式选择和循环判断是否要自动下一首
由于每秒钟判断一次，所以要使用多线程

```python
	'''
		在init里面的循环判断打开方法
	    t1 = threading.Thread(target=self.action)
        t1.setDaemon(True)
        t1.start()
    '''
	#选择播放模式
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
	#循环判断
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
```
**代码介绍在这里就结束了，如果有更好的修改方案请私信我**

最后是全部代码，
[https://github.com/hedy-bit/pyqt5-pygame-urllib-](https://github.com/hedy-bit/pyqt5-pygame-urllib-)
