# coding=gbk
import requests,json,os,time,sys
import bs4

class Main():
    main_cookies_dict = {}

    sqrid = ""
    sqbmid = ""
    rysf = ""
    sqrmc = ""
    gh = ""
    sfzh = ""
    sqbmmc = ""
    xb = ""
    lxdh = ""
    nl = ""
    xrywz = ""
    sheng = ""
    shi = ""
    qu = ""
    jtdzinput = ""

    uname = ""
    password1 = ""
    tw = ""
    def __init__(self):
        print('''
         __________   ___ ___   ___  __  ___             .___________. __  ____    __    ____  _______ .__   __. 
        |   ____\  \ /  / \  \ /  / |  |/  /             |           ||  | \   \  /  \  /   / |   ____||  \ |  | 
        |  |__   \  V  /   \  V  /  |  '  /              `---|  |----`|  |  \   \/    \/   /  |  |__   |   \|  | 
        |   __|   >   <     >   <   |    <                   |  |     |  |   \            /   |   __|  |  . `  | 
        |  |     /  .  \   /  .  \  |  .  \                  |  |     |  |    \    /\    /    |  |____ |  |\   | 
        |__|    /__/ \__\ /__/ \__\ |__|\__\                 |__|     |__|     \__/  \__/     |_______||__| \__| 
                                                                                                                 ''')
        print("Version:0.1.1 CreativeTime:20210916")
        print("删除说明文件里多余的字，加入sqrmc检查，加入jkqk和jkzk检查")
        print('==================================================================================\n >>> config checking <<<\n ')
        self.config_file()
        print('==================================================================================')
        self.get_cookies_dict()

    def config_file(self):
        try:
            with open("config.json") as config_f:
                config = json.load(config_f)
        except (UnboundLocalError, FileNotFoundError):
            print("配置文件不存在或名称错误\n")
            with open("config.json", 'w') as new_config:
                new_config.write('''{
    "account": "",
    "password": "",
    "tw": "36.6"
}''')
            print("已创建新的配置文件，请修改后重启脚本")
            self.set_readme()
            os.system('pause')
            sys.exit()

        try:
            self.uname = config['account']
            self.password1 = config['password']
            self.tw = config['tw']
        except KeyError:
            print("请检查配置文件内的 格式是否正确 或 元素名是否有误改！")
            self.set_readme()
            os.system('pause')
            sys.exit()
        self.tw_check()
        self.passwd_check()
        if self.uname == "":
            print("请填用户名捏")
            os.system('pause')
            sys.exit()
        else:
            print("account check pass ：用户名不为空")

    def tw_check(self):
        try:
            tw = float(self.tw)
            tw = round(tw, 1)
            print("now tw:", tw)
            if tw == 36.0:
                self.tw = 36
            elif tw == 37.0:
                self.tw = 37
            elif 36 <= tw <= 37:
                self.tw = tw
            else:
                print("体温值不正确，请查看说明")
                self.set_readme()
                os.system('pause')
                sys.exit()
            print("response:", self.tw)
            print("tw check pass.")
        except ValueError:
            print("请不要在tw处输入怪东西")
            self.set_readme()
            os.system('pause')
            sys.exit()

    def passwd_check(self):
        if len(self.password1) != 256:
            print("请把密码拖去加密，也许你可能多或者少复制了一点")
            self.set_readme()
            os.system('pause')
            sys.exit()
        else:
            print("password check pass.")

    def set_readme(self):
        with open("readme.txt","w") as info1:
            info1.write('此说明在配置文件检查出错时会重写，请不要用于记录重要内容，如果配置文件改炸了改不回来删掉即可\n\n第一次使用本脚本请在完成后去网页上确认一遍\n\n密码需要先拖去加密，网址https://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n体温范围是36-37，四舍五入保留一位小数')

    def get_execution(self):
        print('==================================================================================\n >>> Execution_start <<<\n ')

        login_url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        try:
            site1 = requests.get(url=login_url, headers=login_headers)
            soup = bs4.BeautifulSoup(site1.text, "html.parser")
            execution = soup.select('input[name="execution"]')[0].attrs['value']
            print(execution)
            print('==================================================================================')
            return execution
        except:
            print("网络超时，可能是服务器错误或者你梯子没关")
            os.system('pause')
            sys.exit()
        # 获取 execution 结束

    def get_cookies_dict(self,debug_mode=False):
        if self.uname == "" or self.password1 == "":
            sys.exit()  # 这是保险措施，虽然应该用不上
        execution = self.get_execution()
        main_session = requests.session()
        print('==================================================================================\n >>> Login_start <<<\n ')

        url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
        payload = f'username={self.uname}&password={self.password1}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        s = main_session.post(url=url, headers=headers, data=payload)  # 登陆会话
        # 登录检查开始
        try:
            soup_v1 = bs4.BeautifulSoup(s.text, "html.parser")
            value1 = soup_v1.select('div[id="msg"] > h2')[0].get_text()
            print("提示信息： ",value1)
            success = '登录成功'
            if value1 == success:
                pass
            else:
                print("登录出错，没有获取到html属性值，请确保账号密码无误后重试")
                print("如果确定账号密码无误且网页能正常登录，请反馈给作者")
                os.system('pause')
                sys.exit()
        except:
            print("登录出错，没有获取到html属性值，请确保账号密码无误后重试")
            print("如果确定账号密码无误且网页能正常登录，请反馈给作者")
            os.system('pause')
            sys.exit()
        # 登录检查结束
        if debug_mode:
            print("Debug: 登录检查结束")
            sys.exit()
        # 打印登陆页面
        # print('----------------------------------\n'+s.text+'----------------------------------\n')

        # 打印原始 headers 和 cookies
        print(s.headers, '\n')
        print(s.headers.get('Set-Cookie'))

        print('----------------------------------------------------------------------------------')

        # cookies 转字典 然后加料
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        print('origin_dict:  ', cookies_dict)
        cookies_dict['refresh'] = '1'
        cookies_dict['show_vpn'] = '1'
        print('\n')
        print('current_dict:   ', cookies_dict)
        self.main_cookies_dict = cookies_dict
        # 定义全局cookies
        print('==================================================================================')
        print('==================================================================================\n >>> 302 <<<\n ')

        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=self.main_cookies_dict)
        print("重定向状态： ",response.status_code)

        # print(response.text.encode('utf-8'))

        return cookies_dict


    def get_history(self,tjsj=time.strftime("%Y-%m-%d", time.localtime()),sd="上午"):

        print('==================================================================================\n >>> Get_history <<<')
        url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryToday.biz.ext?vpn-12-o2-workflow.sues.edu.cn"
        data = {
            'params': {
                'tjsj': tjsj,
                'sd': sd
            }
        }
        headers = {
            'Content-Type': 'text/json',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36',
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), cookies=self.main_cookies_dict)

        # print(len(json.loads(response.text)))
        print(response.text)
        try:
            dict11 = len(json.loads(response.text)["resultData"][0])
            print("当前字典长度：",dict11)
            return True
        except:
            print('未获取到当前时段的字典：History no data.')
            return False


    def get_Near_history(self):

        print('==================================================================================\n >>> Get_history <<<')
        url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear.biz.ext?vpn-12-o2-workflow.sues.edu.cn"

        headers = {
            'Content-Type': 'text/json',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36',
        }

        response = requests.post(url, headers=headers, cookies=self.main_cookies_dict)

        print(response.text)
        return response

    def history2dict(self):
        dict02 = json.loads(self.get_Near_history().text)
        print('==================================================================================\n >>> NearHistory2dict <<<')
        dict01 = dict02["resultData"][0]
        print(dict01)
        self.sqrid = dict01["SQRID"]
        self.sqbmid = dict01["SQBMID"]
        self.rysf = dict01["RYSF"]
        self.sqrmc = dict01["SQRMC"]
        self.gh = dict01["GH"]
        self.sfzh = dict01["SFZH"]
        self.sqbmmc = dict01["SQBMMC"]
        self.xb = dict01["XB"]
        self.lxdh = dict01["LXDH"]
        self.nl = dict01["NL"]
        self.xrywz = dict01["XRYWZ"]
        self.sheng = dict01["SHENG"]
        self.shi = dict01["SHI"]
        self.qu = dict01["QU"]
        self.jtdzinput = dict01["JTDZINPUT"]

        jkqk = dict01["JKQK"]
        jkzk = dict01["JKZK"]
        print(f"健康情况：{jkqk}，健康状况：{jkzk}")
        if jkqk != "1" or jkzk != "1":
            print('警告：\n当前获取到最近的一次数据中的健康情况和健康状况参数不正确，请确定你在webvpn上的健康状况无误')
            print('如果确定网页上信息无问题，请暂停使用本脚本，然后联系作者')
            print("健康状况默认为 1 ，意为“良好”；健康情况默认为 1 ，意为“无特殊情况”")
            print('按任意键将继续执行，如果因为信息确实有问题导致被通报，本作者不负责')
            os.system('pause')
        newList = [self.sqrid,self.sqbmid,self.rysf,self.sqrmc,self.gh,self.sfzh,self.sqbmmc,self.xb,self.lxdh,self.nl,self.xrywz,self.sheng,self.shi,self.qu,self.jtdzinput]
        print("----------")
        print("vvv 所需信息 vvv")
        for checking in newList:
            print(checking)
        print("----------")

    def update(self,debug_mode=False):
        nowTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        nowHour = int(time.strftime("%H", time.localtime()))
        print("当前时间： ", nowTime)
        print("当前小时：", nowHour)
        if 00 <= nowHour < 12:
            sd = "上午"
            print(sd)
        else:
            sd = "下午"
            print(sd)

        if_check = self.get_history(sd=sd)
        if if_check == True and debug_mode == False:
            if not debug_mode:
                print("当前时段已经填过了")
                time.sleep(10)
                sys.exit()
            else:
                print("debug exit")
        else:
            self.history2dict()
            url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn"
            if self.sqrmc == "":
                print("未获取到正确信息，强制退出")
                sys.exit()
            data = {"params": {"sqrid": self.sqrid,
                   "sqbmid": self.sqbmid,
                   "rysf": self.rysf,
                   "sqrmc": self.sqrmc,
                   "gh": self.gh,
                   "sfzh": self.sfzh,
                   "sqbmmc": self.sqbmmc,
                   "xb": self.xb,
                   "lxdh": self.lxdh,
                   "nl": self.nl,
                   "tjsj": nowTime,
                   "xrywz": self.xrywz,
                   "sheng": self.sheng,
                   "shi": self.shi,
                   "qu": self.qu,
                   "jtdzinput": self.jtdzinput,
                   "gj": "",
                   "jtgj": "",
                   "jkzk": "1",
                   "jkqk": "1",
                   "tw": self.tw,
                   "sd": sd,
                   "bz": "",
                   "_ext": "{}"}}

            print(data)
            headers = {
                'Content-Type': 'text/json',
                'Origin': 'https://web-vpn.sues.edu.cn',
                'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
                'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36'
            }

            if debug_mode == True:
                sys.exit()

            print()
            response = requests.post(url, headers=headers, data=json.dumps(data),cookies=self.main_cookies_dict)

            print("Debug: " + response.text)
            if(json.loads(response.text)['result']['success']==True):
                print("提交成功")
                time.sleep(10)
                return True
            else:
                print(response.text)


qwe = Main()

# qwe.get_history(tjsj="2021-09-09",sd="下午")
qwe.update(debug_mode=False)
# qwe.get_Near_history()
# qwe.history2dict()