# coding=gbk
import base64

import requests
import json
import time
import sys
import bs4
import re
from win10toast import ToastNotifier
# from PIL import Image
# import pytesseract
import ddddocr

# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class Main:
    def __init__(self):
        self.main_cookies_dict = {}
        self.main_execution = ""

        self.sqrid = ""
        self.sqbmid = ""
        self.rysf = ""
        self.sqrmc = ""
        self.gh = ""
        self.sfzh = ""
        self.sqbmmc = ""
        self.xb = ""
        self.lxdh = ""
        self.nl = ""
        self.xrywz = ""
        self.sheng = ""
        self.shi = ""
        self.qu = ""
        self.jtdzinput = ""

        self.uname = ""
        self.password1 = ""
        self.tw = ""
        self.renyuanweizhi = ""
        self.xiaoqu = ""

        print(r'''
                 __________   ___ ___   ___  __  ___        .___________. __  ____    __    ____  _______ .__   __. 
                |   ____\  \ /  / \  \ /  / |  |/  /        |           ||  | \   \  /  \  /   / |   ____||  \ |  | 
                |  |__   \  V  /   \  V  /  |  '  /         `---|  |----`|  |  \   \/    \/   /  |  |__   |   \|  | 
                |   __|   >   <     >   <   |    <              |  |     |  |   \            /   |   __|  |  . `  | 
                |  |     /  .  \   /  .  \  |  .  \             |  |     |  |    \    /\    /    |  |____ |  |\   | 
                |__|    /__/ \__\ /__/ \__\ |__|\__\            |__|     |__|     \__/  \__/     |_______||__| \__| 
            ''')
        # print("Ver1.0 createTime:20211205\n应对学校网站更新，加了验证码对应方法，但是代码很乱")
        # print("Ver1.1 crateTime:20211213\n说明：找出来了提交时候的需要的验证码，以及重新写了一遍")
        # print("Ver1.2 crateTime:20211214\n说明：改了验证码识别库，不用额外装软件")
        print("Ver1.3 crateTime:20211216\n说明：加了base64")
    def warn_bubble(self, msg):
        print("Warning: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("发生错误", msg, icon_path=r'fxxk_tiwen.ico')

    def info_bubble(self, msg):
        print("Info: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("提示信息", msg, icon_path=r'fxxk_tiwen.ico')

    def printLine(self):
        i = 0
        while i < 100:
            print("=", end='')
            i += 1
        print("")

    def set_readme(self):
        with open("readme.txt", "w") as info1:
            info1.write('''此说明在配置文件检查出错时会重写，请不要用于记录重要内容，如果配置文件改炸了改不回来删掉即可\n\n
            第一次使用本脚本请在完成后去网页上确认一遍\n\n密码需要先拖去加密，网址https://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n
            体温范围是36-37，四舍五入保留一位小数\nrenyuanweizhi是人员位置，1是留校，2是在沪\nxiaoqu是校区，1是松江，2是虹口，3是长宁''')

    def web_vpn_state(self):
        self.printLine()
        print(">>> web-vpn state <<<")
        main_url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login"
        response = requests.get(url=main_url)
        if response.ok:
            print("当前webvpn页面状态：", response.status_code)
            return True
        else:
            print("当前webvpn页面状态：", response.status_code)
            print("无法正常访问，请稍后再试")
            return False

    def configCheck(self):
        self.printLine()
        print(">>> Config_Check <<<")
        # try 1 是否生成配置文件
        try:
            with open("config.json") as config_f:
                config = json.load(config_f)
        except (UnboundLocalError, FileNotFoundError):
            self.warn_bubble("配置文件不存在或名称错误")
            with open("config.json", 'w') as new_config:
                new_config.write('''{
    "account": "",
    "password": "",
    "tw": "36.6",
    "renyuanweizhi": "1",
    "xiaoqu": "2",
    "sheng": "",
    "shi": "",
    "qu": "",
    "jtdz": ""
}''')
            self.info_bubble("已创建新的配置文件，请修改后重启脚本")
            self.set_readme()
            return False
        # try 2 元素对应
        try:
            self.uname = config['account']
            self.password1 = config['password']
            self.tw = config['tw']
            self.renyuanweizhi = config['renyuanweizhi']
            if self.renyuanweizhi == "1":
                self.xiaoqu = config['xiaoqu']
            else:
                self.sheng = config['sheng']
                self.shi = config['shi']
                self.qu = config['qu']
                self.jtdzinput = config['jtdz']
        except KeyError:
            self.warn_bubble("请检查配置文件内的 格式是否正确 或 元素名是否有误改！")
            self.set_readme()
            return False
        # try 3 体温值检查
        try:
            tw = float(self.tw)
            tw = round(tw, 1)
            print("当前tw:", tw)
            if tw == 36.0:
                self.tw = 36
            elif tw == 37.0:
                self.tw = 37
            elif 36 <= tw <= 37:
                self.tw = tw
            else:
                self.warn_bubble("体温值不正确，请查看说明")
                self.set_readme()
                return False
            print("tw check pass.")
        except ValueError:
            self.warn_bubble("请不要在tw处输入怪东西")
            self.set_readme()
            return False
        # try 4 密码检查
        if len(self.password1) != 256:
            self.warn_bubble("请把密码拖去加密，也许你可能多或者少复制了一点")
            self.set_readme()
            return False
        else:
            print("password check pass.")
        # try 5 人员位置检查
        try:
            if self.renyuanweizhi == "1" or self.renyuanweizhi == "2":
                print("人员位置check pass")
            else:
                self.warn_bubble("人员位置检查出错：请检查人员位置的参数值")
                return False
        except:
            self.warn_bubble("请不要在renyuanweizhi处输入除了1和2以外的参数")
            return False
        # try 6 校区检查
        try:
            if self.renyuanweizhi == "1":
                if self.xiaoqu == "1" or self.xiaoqu == "2" or self.xiaoqu == "3":
                    print("校区check pass")
                else:
                    self.warn_bubble("校区检查出错：请检查校区的参数")
                    return False
        except:
            self.warn_bubble("校区检查出错：请不要在xiaoqu处输入除了1或2或3以外的参数")
            return False

        return True

    # def captcha2str(self):
    #     path = f"captcha.jpg"
    #     captcha = Image.open(path)
    #     result = pytesseract.image_to_string(captcha)
    #     print('验证码：'+ result.replace('\n', ''))
    #     return result.replace('\n', '')

    def captcha2str_ddddocr(self):
        ocr = ddddocr.DdddOcr()
        with open("captcha.jpg", 'rb') as captcha:
            img1 = captcha.read()
        result = ocr.classification(img1)
        print("验证码：", result)
        return result

    def getExecution(self):
        self.printLine()
        print(">>> Get execution <<<")
        login_url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        try:
            site1 = requests.get(url=login_url, headers=login_headers)
            soup = bs4.BeautifulSoup(site1.text, "html.parser")
            execution = soup.select('input[name="execution"]')[0].attrs['value']
            print("execution: ", execution)
            print("Length of execution: ", len(execution))
            if len(execution) != 2309:
                print("Execution error: Incorrect length.It should be 2309.")
                return False
        except:
            self.warn_bubble("网络超时，可能是服务器错误或者你梯子没关")
            return False
        # 做 cookie
        self.printLine()
        print(">>> Set cookies <<<")
        try:
            print(site1.headers.get('Set-Cookie'))
            cookies_dict1 = requests.utils.dict_from_cookiejar(site1.cookies)
            print('origin_dict:  ', cookies_dict1)
            cookies_dict1['show_vpn'] = '1'
            print('current_dict:  ', cookies_dict1)
            self.main_cookies_dict = cookies_dict1
            # print(self.main_cookies_dict)
        except:
            self.warn_bubble("cookies转换失败")
            return False
        self.main_execution = execution
        return execution

    def getCaptcha(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("未调用getExecution")
            self.getExecution()
        # 获取验证码图片
        print(">>> Get captcha <<<")
        pic_url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/captcha.jpg"
        pic_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        res = requests.get(url=pic_url, headers=pic_headers, cookies=self.main_cookies_dict)
        pic_data = res.content
        with open('captcha.jpg', 'wb') as f:
            f.write(pic_data)
        captcha_str = self.captcha2str_ddddocr()
        return captcha_str

    def loginFF(self):
        self.printLine()
        print("当前位置：Login 调用")
        if self.main_cookies_dict == {}:
            self.warn_bubble("未调用getExecution和getCaptcha")
            return False
        elif self.uname == "" or self.password1 == "":
            self.warn_bubble("用户名或密码为空")
            return False
        execution = self.main_execution
        # k是登录循环，j是验证码识别循环，大循环不累计验证码识别错误次数
        k = 0
        while k < 3:

            j = 0
            while j < 5:
                try:
                    captcha_str = self.getCaptcha()
                    captcha_str1 = int(captcha_str)
                    # 这有个类型验证是因为之前用的是 pytesseract
                    print("当前captcha类型：", type(captcha_str1))
                    print(f"当前验证码识别循环次：{j+1}/5 最大5次")
                    break
                except:
                    print('传前验证不正确，重试')
                    j += 1
                    time.sleep(1)
                if j == 4:
                    print("验证码获取超次")
                    return False
            self.printLine()
            print(">>> Login_start <<<")
            print(f"当前登录循环次：{k+1}/3 最大3次")
            url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
            payload = f'username={self.uname}&password={self.password1}&authcode={captcha_str}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }
            session1 = requests.post(url=url, headers=headers, data=payload, cookies=self.main_cookies_dict)
            # 此时应已完成登录
            try:
                soup_v1 = bs4.BeautifulSoup(session1.text, "html.parser")
                value1 = soup_v1.select('div[id="msg"] > h2')[0].get_text()
                print(value1)
                # self.info_bubble("页面提示信息：" + value1)
                print("页面提示信息：" + value1)
                if value1 == '登录成功':
                    break
                else:
                    print("可能是验证码错误，准备重试")
                    time.sleep(1)
            except:
                print("可能是验证码错误，准备重试")
                time.sleep(1)

            k += 1
            if k == 2:
                self.warn_bubble("循环超次，登录出错，没有获取到 html 属性值，请确保账号密码无误后重试")
                self.warn_bubble("如果确定账号密码无误且网页能正常登录，请反馈给作者")
                return False

        # 302 自动跳转使 cookies 生效
        self.printLine()
        print(">>> 302 <<<")
        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=self.main_cookies_dict)
        print("web-vpn主页重定向状态：", response.status_code)
        return True
        # 不知道有什么用但是return了个True

    # 这后面都是之前没改过的屎山

    def get_history(self,tjsj=time.strftime("%Y-%m-%d", time.localtime()),sd="上午"):
        self.printLine()
        print('>>> Get_history <<<')
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
        print(response.text)
        try:
            dict11 = len(json.loads(response.text)["resultData"][0])
            print("当前字典长度：",dict11)
            return True
        except:
            print('未获取到当前时段的字典：History no data.')
            return False

    def get_Near_history(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("未调用getExecution和getCaptcha")
            return False
        print('>>> Get_near_history <<<')
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
        self.printLine()
        print('>>> NearHistory2dict <<<')
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

        jkqk = dict01["JKQK"]
        jkzk = dict01["JKZK"]
        print(f"健康情况：{jkqk}，健康状况：{jkzk}")
        if jkqk != "1" or jkzk != "1":
            print('警告：\n当前获取到最近的一次数据中的健康情况和健康状况参数不正确，请确定你在webvpn上的健康状况无误')
            print('如果确定网页上信息无问题，请暂停使用本脚本，然后联系作者')
            print("健康状况默认为 1 ，意为“良好”；健康情况默认为 1 ，意为“无特殊情况”")
            # print('按任意键将继续执行，如果因为信息确实有问题导致被通报，本作者不负责')
            time.sleep(30)
            print("\n此处等待30秒")
            sys.exit()

        newList = [self.sqrid,self.sqbmid,self.rysf,self.sqrmc,self.gh,self.sfzh,self.sqbmmc,self.xb,self.lxdh,self.nl]
        meaning_of_list=["申请人ID","申请人MID","人员身份","申请人名称","工号","身份证号","申请部门名称","系部","联系电话","年龄"]
        print("----------")
        print("### 所需信息 ###")
        for meaning_list,data_list in zip(meaning_of_list,newList):
            print(meaning_list,":",data_list)
        print("----------")

    def get_post_captcha(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("未调用getExecution")
            self.getExecution()
        print('>>> get_post_captcha <<<')
        site2_url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        site2_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        }
        site2 = requests.get(url=site2_url, headers=site2_headers, cookies=self.main_cookies_dict)
        # print(site2.text)
        re_rule = re.compile(r'{"verification-code".*?}')
        code_str2 = re_rule.findall(site2.text)
        code_json = json.loads(code_str2[0])
        captcha_code = code_json['verification-code']
        print("captcha_code：", captcha_code)
        return captcha_code

    def update(self, debug_mode=False):
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
        # 时段检测
        if 00 <= nowHour < 3:
            self.info_bubble("系统维护时间，暂时无法进行健康填报，0-3点不可填报")
            return False

        queryNear = self.get_history(sd=sd)
        if queryNear:
            self.info_bubble("当前时段已经填过了")
            time.sleep(10)
            sys.exit()
        #     正常出口 1
        else:
            verification_code = self.get_post_captcha()
            self.history2dict()
            if self.sqrmc == "":
                self.warn_bubble("未获取到正确信息，异常退出")
                sys.exit()
            if self.renyuanweizhi == "1":
                data = {"sqrid": self.sqrid,
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
                                   "xrywz": self.renyuanweizhi,
                                   "xq": self.xiaoqu,
                                   "gj": "",
                                   "jtgj": "",
                                   "jkzk": "1",
                                   "jkqk": "1",
                                   "tw": self.tw,
                                   "sd": sd,
                                   "bz": "",
                                   "_ext": "{}"}
            else:
                data = {"sqrid": self.sqrid,
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
                       "xrywz": self.renyuanweizhi,
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
                       "_ext": "{}"}

            print("uncoded:", data)
            encode_data = base64.b64encode(str(data).encode("utf-8"))
            print("encoded:", encode_data)
            json_data = {"params": encode_data.decode()}
            print("json_data:", json_data)
            print(json.dumps(json_data))
            update_url = f"https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn?gh={self.gh}"
            headers = {
                'Content-Type': 'text/json',
                'Origin': 'https://web-vpn.sues.edu.cn',
                'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
                'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36',
                'verification-code': verification_code
            }
            if debug_mode:
                print(json_data)
                sys.exit()
            response = requests.post(update_url, headers=headers, data=json.dumps(json_data), cookies=self.main_cookies_dict)
            try:
                if json.loads(response.text)['result']['success']:
                    self.info_bubble("提交成功")
                    time.sleep(10)
                    return True
                else:
                    print("提交不成功")
                    print("Debug: " + response.text)
                    time.sleep(10)
                    return False
            except:
                # 这里防报错的，理论上不会跑到这
                print("可能是时段不正确")
                print("Debug: " + response.text)
                time.sleep(10)
                return False

    def af(self, debug_mode=False):
        stat1 = self.web_vpn_state()
        if not stat1:
            return False
        stat2 = self.configCheck()
        if not stat2:
            return False
        stat3 = self.getExecution()
        if not stat3:
            return False
        stat4 = self.loginFF()
        if not stat4:
            return False
        if self.main_cookies_dict == {}:
            pass
        # 直接退出
        else:
            self.update(debug_mode)
            # self.get_history(tjsj="2021-12-10")
            pass

# update 传 debug mode 就不提交
do = Main()
do.af(debug_mode=False)
