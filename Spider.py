import time,json,requests,redis,re,os,random,pymysql
from selenium import webdriver
from pprint import pprint

class GzhSpyder:
    def __init__(self,path,userid,pwd,gzlist,stoptime,mysqlinfo):
        self.path = path
        self.userid = userid
        self.pwd = pwd
        self.gzlist = gzlist
        self.stoptime = stoptime
        self.mysqlinfo = mysqlinfo

    def getcookie(self):
        post = {}
        
        driver = webdriver.Chrome(executable_path=self.path)
        driver.get('https://mp.weixin.qq.com/')
        time.sleep(2)
        driver.find_element_by_xpath("./*//input[@name='account']").clear()
        driver.find_element_by_xpath("./*//input[@name='account']").send_keys(self.userid)
        driver.find_element_by_xpath("./*//input[@name='password']").clear()
        driver.find_element_by_xpath("./*//input[@name='password']").send_keys(self.pwd)
        # 在自动输完密码之后记得点一下记住我
        time.sleep(5)
        driver.find_element_by_xpath("./*//a[@title='点击登录']").click()
        # 拿手机扫二维码！
        time.sleep(15)
        driver.get('https://mp.weixin.qq.com/')
        cookie_items = driver.get_cookies()
        for cookie_item in cookie_items:
            post[cookie_item['name']] = cookie_item['value']
        cookie_str = json.dumps(post)
        with open('cookie.txt', 'w+', encoding='utf-8') as f:
            f.write(cookie_str)
        driver.close()

    def get_one_page(self,url,cookie_str):

        for test in range(2000):
            session = requests.session()
            session.keep_alive = False  # 关闭多余连接
            # with open('cookie.txt', 'r', encoding='utf-8') as f:
            #     cookie = f.read()
            cookies = json.loads(cookie_str)                
            session.headers = { "User-Agent":random.choice(["Mozilla/5.0 (Windows NT 10.0; WOW64)",
                    'Mozilla/5.0 (Windows NT 6.3; WOW64)',
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                    #   "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                    #   "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                    #   "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                    #   "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    #   "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    #   "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
                    #   "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
                    #   "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
                    #   "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
                    #   "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
                    #   "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
                    #   "UCWEB7.0.2.37/28/999",
                    #   "NOKIA5700/ UCWEB7.0.2.37/28/999",
                    #   "Openwave/ UCWEB7.0.2.37/28/999",
                    #   "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
                    # iPhone 6：
                    #   "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"
                    ])}
            re = session.get(url, cookies=cookies)
            # print(session.headers)
            # re = requests.get(url,headers)
            # re.encoding = 'GBK'
            if re.status_code == 200:
                response = re.text
                return response
                break
            else:
                if re.status_code == 404:
                    return 0
                    break

    def getcontent(self,url,cookie_str,conn,cursor,tbname):
        try:
            print(url)
            html = self.get_one_page(url,cookie_str)
            # print(html)
            title = re.findall('msg_title(.*?)var',html,re.S)
            title1 = re.findall('\"(.*?)\"',title[0],re.S)
            # print(title1[0])    
            time = re.findall('publish_time = \"(.*?)\"',html,re.S)
            # time1 = re.findall('\"(.*?)\"',time[0],re.S)
            # print(time[0])
            content = re.findall('rich_media_content(.*?)div>',html,re.S)
            # print(len(content))
            content1 = re.findall('(<p.*?p>)',content[1],re.S)
            # print(len(content1))
            contenttext = ''
            for item in content1:
                content2 = re.findall('>(.*?)<',item,re.S)
                # print(content2)
                for item2 in content2:
                    contenttext = contenttext + item2
                contenttext = contenttext + '\n'
            # print(contenttext)

            # 插入一行记录，注意MySQL的占位符是%s:
            cursor.execute('insert into ' + tbname + ' (url, time, title, name) values (%s, %s, %s, %s)', [url,time[0],title1[0],contenttext])
            conn.commit()
            return time[0]
        except:
            print(url+'失败')

    def start(self):

        url = 'https://mp.weixin.qq.com'
        header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
            }

        with open('cookie.txt', 'r', encoding='utf-8') as f:
            cookie_str = f.read()

        # 注意把password设为你的root口令:
        userid = self.mysqlinfo[0]
        pwd = self.mysqlinfo[1]
        db = self.mysqlinfo[2]
        conn = pymysql.connect(user=userid, password=pwd, database=db)
        cursor = conn.cursor()
        print('mysql登陆成功')

        cookies = json.loads(cookie_str)
        response = requests.get(url=url, cookies=cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        for query in self.gzlist:

            # 创建表:
            tbname = query
            try:
                cursor.execute('create table '+ tbname +' (url varchar(5000), time varchar(20), title varchar(200), name varchar(10000))')
                print(query+'数据库正在新建……')
            except:
                print(query+'数据库更新中……')
            
            query_id = {
                'action': 'search_biz',
                'token' : token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': query,
                'begin': '0',
                'count': '5',
            }
            search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
            search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
            lists = search_response.json().get('list')[0]
            fakeid = lists.get('fakeid')
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '0',
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            max_num = appmsg_response.json().get('app_msg_cnt')
            num = int(int(max_num) / 5)
            begin = 0
            while num + 1 > 0 :
                query_id_data = {
                    'token': token,
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                    'random': random.random(),
                    'action': 'list_ex',
                    'begin': '{}'.format(str(begin)),
                    'count': '5',
                    'query': '',
                    'fakeid': fakeid,
                    'type': '9'
                }

                query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
                fakeid_list = query_fakeid_response.json().get('app_msg_list')

                stopvalue = 0
                time1 = '0'
                try:
                    for item in fakeid_list:
                        url = item.get('link')
                        # print(url)
                        # file_handler.write(item.get('link'))
                        time = self.getcontent(url,cookie_str,conn,cursor,tbname)
                        if time != time1:
                            print("\n"+time)
                            time1 = time
                        if time == self.stoptime:
                            stopvalue += 1
                            break
                        # file_handler.write('\n')
                    num -= 1
                    begin = int(begin)
                    begin+=5
                    # time.sleep(2)
                except:
                    break
                if stopvalue == 1:
                    break

        cursor.close()
        conn.close()


a = GzhSpyder('/Users/sure/Downloads/chromedriver','tjwangcs@gmail.com','cs981124',['jrqzhp'],'2019-03-08',['root','asd12345','tset'])
a.getcookie()
a.start()