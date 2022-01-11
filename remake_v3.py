# coding=gbk
import base64
import os.path

import requests
import json
import time
import sys
import bs4
import re
from win10toast import ToastNotifier
import ddddocr


class Main:
    def __init__(self):
        print(r'''
                 __________   ___ ___   ___  __  ___        .___________. __  ____    __    ____  _______ .__   __. 
                |   ____\  \ /  / \  \ /  / |  |/  /        |           ||  | \   \  /  \  /   / |   ____||  \ |  | 
                |  |__   \  V  /   \  V  /  |  '  /         `---|  |----`|  |  \   \/    \/   /  |  |__   |   \|  | 
                |   __|   >   <     >   <   |    <              |  |     |  |   \            /   |   __|  |  . `  | 
                |  |     /  .  \   /  .  \  |  .  \             |  |     |  |    \    /\    /    |  |____ |  |\   | 
                |__|    /__/ \__\ /__/ \__\ |__|\__\            |__|     |__|     \__/  \__/     |_______||__| \__| 
            ''')
        # print("Ver1.0 createTime:20211205\n应对学校网站更新，加了验证码对应方法，但是代码很乱")
        # print("Ver1.1 createTime:20211213\n说明：找出来了提交时候的需要的验证码，以及重新写了一遍")
        # print("Ver1.2 createTime:20211214\n说明：改了验证码识别库，不用额外装软件")
        # print("Ver1.3 createTime:20211216\n说明：加了base64")
        # print("Ver1.4 createTime:20211226\n说明：这个瞎子终于发现问题在哪了，此版本可正常使用")
        print("Ver2.0 createTime:20211229\n说明：重构！！！！！去他妈的全局变量")
        print("Ver2.1 createTime:20211229\n说明：小改一下验证config逻辑")

    def warn_bubble(self, msg):
        print("Warning: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("发生错误", msg, icon_path=r'fxxk_tiwen.ico')

    def info_bubble(self, msg):
        print("Info: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("提示信息", msg, icon_path=r'fxxk_tiwen.ico')

    def print_line(self):
        i = 0
        while i < 100:
            print("=", end='')
            i += 1
        print("")

    def set_readme(self):
        if not os.path.exists("readme.txt"):
            with open("readme.txt", "w") as info1:
                info1.write('''此说明在配置文件检查出错时会重写，请不要用于记录重要内容，如果配置文件改炸了改不回来删掉即可\n\n
                第一次使用本脚本请在完成后去网页上确认一遍\n\n密码需要先拖去加密，网址https://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n
                体温范围是36-37，四舍五入保留一位小数\nrenyuanweizhi是人员位置，1是留校，2是在沪\nxiaoqu是校区，1是松江，2是虹口，3是长宁''')
        else:
            pass

    def web_vpn_state(self):
        self.print_line()
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

    def config_check(self):
        self.print_line()
        print(">>> Config_Check <<<")
        # try 1 是否生成配置文件
        try:
            with open("config.json", encoding='utf-8') as config_f:
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
            uname = config['account']
            password1 = config['password']
            tw = config['tw']
            xiaoqu = config['xiaoqu']
            renyuanweizhi = config['renyuanweizhi']
            sheng = config['sheng']
            shi = config['shi']
            qu = config['qu']
            jiatindizhi = config['jtdz']
        except KeyError:
            self.warn_bubble("请检查配置文件内的 格式是否正确 或 元素名是否有误改！")
            self.set_readme()
            return False
        # try 3 体温值检查
        try:
            tw = float(tw)
            tw = round(tw, 1)
            print("当前tw:", tw)
            if tw == 36.0:
                current_tw = 36
            elif tw == 37.0:
                current_tw = 37
            elif 36 <= tw <= 37:
                current_tw = tw
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
        if len(password1) != 256:
            self.warn_bubble("请把密码拖去加密，也许你可能多或者少复制了一点")
            self.set_readme()
            return False
        else:
            print("password check pass.")
        # try 5 人员位置检查
        try:
            if renyuanweizhi == "1" or renyuanweizhi == "2":
                print("人员位置check pass")
            else:
                self.warn_bubble("人员位置检查出错：请检查人员位置的参数值")
                return False
        except:
            self.warn_bubble("请不要在renyuanweizhi处输入除了1和2以外的参数")
            return False
        # try 6 校区检查
        try:
            if renyuanweizhi == "1":
                if xiaoqu == "1" or xiaoqu == "2" or xiaoqu == "3":
                    print("校区check pass")
                else:
                    self.warn_bubble("校区检查出错：请检查校区的参数")
                    return False
        except:
            self.warn_bubble("校区检查出错：请不要在xiaoqu处输入除了1或2或3以外的参数")
            return False
        result_dict = {"uname": uname, "password": password1, "tw": current_tw, "renyuanweizhi": renyuanweizhi, 
                       "xiaoqu": xiaoqu, "sheng": sheng, "shi": shi, "qu": qu, "jtdz": jiatindizhi}
        return result_dict

    def captcha2str_ddddocr(self):
        ocr = ddddocr.DdddOcr()
        with open("captcha.jpg", 'rb') as captcha:
            img1 = captcha.read()
        result = ocr.classification(img1)
        print("验证码：", result)
        return result

    def get_execution(self):
        self.print_line()
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
        self.print_line()
        print(">>> Set cookies <<<")
        try:
            print(site1.headers.get('Set-Cookie'))
            cookies_dict1 = requests.utils.dict_from_cookiejar(site1.cookies)
            print('origin_dict:  ', cookies_dict1)
            cookies_dict1['show_vpn'] = '1'
            print('current_dict:  ', cookies_dict1)
            main_cookies_dict = cookies_dict1
        except:
            self.warn_bubble("cookies转换失败")
            return False
        main_execution = execution
        return {"main_execution": main_execution, "main_cookies_dict": main_cookies_dict}

    def get_captcha(self, cookie: dict):
        self.print_line()
        # 获取验证码图片
        print(">>> Get captcha <<<")
        pic_url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/captcha.jpg"
        pic_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        res = requests.get(url=pic_url, headers=pic_headers, cookies=cookie)
        pic_data = res.content
        with open('captcha.jpg', 'wb') as f:
            f.write(pic_data)
        captcha_str = self.captcha2str_ddddocr()
        return captcha_str

    def login_ff(self, cookie: dict, execution, uname, password):
        self.print_line()
        print("当前位置：Login 调用")
        # k是登录循环，j是验证码识别循环，大循环不累计验证码识别错误次数
        k = 0
        while k < 3:

            j = 0
            while j < 5:
                try:
                    captcha_str = self.get_captcha(cookie)
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
            self.print_line()
            print(">>> Login_start <<<")
            print(f"当前登录循环次：{k+1}/3 最大3次")
            url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
            payload = f'username={uname}&password={password}&authcode={captcha_str}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }
            session1 = requests.post(url=url, headers=headers, data=payload, cookies=cookie)
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
        self.print_line()
        print(">>> 302 <<<")
        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=cookie)
        print("web-vpn主页重定向状态：", response.status_code)
        return True

    def get_history(self, cookie: dict, tjsj=time.strftime("%Y-%m-%d", time.localtime()), sd="上午"):
        self.print_line()
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
        response = requests.post(url, headers=headers, data=json.dumps(data), cookies=cookie)
        print(response.text)
        return response.text

    def get_Near_history(self, cookie: dict):
        self.print_line()
        print('>>> Get_near_history <<<')
        url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear.biz.ext?vpn-12-o2-workflow.sues.edu.cn"
        headers = {
            'Content-Type': 'text/json',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36',
        }
        response = requests.post(url, headers=headers, cookies=cookie)
        print(response.text)
        return response.text

    def history2dict(self, history_dict: str):
        self.print_line()
        print('>>> History2dict <<<')
        try:
            dict01 = json.loads(history_dict)["resultData"][0]
            print(dict01)
            sqrid = dict01["SQRID"]
            sqbmid = dict01["SQBMID"]
            rysf = dict01["RYSF"]
            sqrmc = dict01["SQRMC"]
            gh = dict01["GH"]
            sfzh = dict01["SFZH"]
            sqbmmc = dict01["SQBMMC"]
            xb = dict01["XB"]
            lxdh = dict01["LXDH"]
            nl = dict01["NL"]

            jkqk = dict01["JKQK"]
            jkzk = dict01["JKZK"]

            data_dict = {"申请人ID": sqrid, "申请人MID": sqbmid, "人员身份": rysf, "申请人名称": sqrmc, "工号": gh,
                         "身份证号": sfzh, "申请部门名称": sqbmmc, "系部": xb, "联系电话": lxdh, "年龄": nl, "健康情况": jkqk,
                         "健康状况": jkzk}
            print("----------")
            print("### 字典信息 ###")
            for key, value in data_dict.items():
                print(key, ":", value)
            print("----------")
            result_dict = {"sqrid": sqrid, "sqbmid": sqbmid, "rysf": rysf, "sqrmc": sqrmc, "gh": gh, "sfzh": sfzh,
                           "sqbmmc": sqbmmc, "xb": xb, "lxdh": lxdh, "nl": nl, "jkqk": jkqk, "jkzk": jkzk}
            return result_dict
        except:
            print("传错参了")
            return False

    def get_update_captcha(self, cookie: dict):
        self.print_line()
        print('>>> get_update_captcha <<<')
        site2_url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        site2_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        }
        site2 = requests.get(url=site2_url, headers=site2_headers, cookies=cookie)
        # print(site2.text)
        re_rule = re.compile(r'{"verification-code".*?}')
        code_str2 = re_rule.findall(site2.text)
        code_json = json.loads(code_str2[0])
        captcha_code = code_json['verification-code']
        print("captcha_code：", captcha_code)
        return captcha_code

    def get_period(self):
        nowHour = int(time.strftime("%H", time.localtime()))
        print("当前小时：", nowHour)
        if 00 <= nowHour < 12:
            sd = "上午"
        else:
            sd = "下午"
        print("当前时段：", sd)
        return [sd, nowHour]

    def update(self, cookie: dict, renyuanweizhi, xiaoqu, sheng, shi, qu, jtdz, tw, debug_mode=False):
        period = self.get_period()
        if debug_mode:
            print("debug已开启，跳过时段检测和当前时段历史检查")
        else:
            # 时段检测
            if 00 <= period[1] < 3:
                self.info_bubble("系统维护时间，暂时无法进行健康填报，0-3点不可填报")
                return False
            # 当前时段填报检测
            if_today = self.get_history(sd=period[0], cookie=cookie)
            try:
                dict11 = len(json.loads(if_today)["resultData"][0])
                print("当前字典长度：", dict11)
                self.info_bubble("当前时段已经填过了")
                return True
                # 正常出口 1
            except:
                print('未获取到当前时段的字典：History no data.')
                pass

        now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print("当前时间： ", now_time)
        response = self.get_Near_history(cookie)
        info_dict = self.history2dict(response)
        print("健康情况：{jkqk}，健康状况：{jkzk}".format(jkqk=info_dict["jkqk"], jkzk=info_dict["jkzk"]))

        if info_dict["jkqk"] != "1" or info_dict["jkzk"] != "1":
            print('警告：\n当前获取到最近的一次数据中的健康情况和健康状况参数不正确，请确定你在webvpn上的健康状况无误')
            print('如果确定网页上信息无问题，请暂停使用本脚本，然后联系作者')
            print("健康状况默认为 1 ，意为“良好”；健康情况默认为 1 ，意为“无特殊情况”")
            # print('按任意键将继续执行，如果因为信息确实有问题导致被通报，本作者不负责')
            print("\n此处等待30秒")
            time.sleep(30)
            sys.exit()

        if renyuanweizhi == "1":
            data = {"sqrid": info_dict["sqrid"],
                    "sqbmid": info_dict["sqbmid"],
                    "rysf": info_dict["rysf"],
                    "sqrmc": info_dict["sqrmc"],
                    "gh": info_dict["gh"],
                    "sfzh": info_dict["sfzh"],
                    "sqbmmc": info_dict["sqbmmc"],
                    "xb": info_dict["xb"],
                    "lxdh": info_dict["lxdh"],
                    "nl": info_dict["nl"],
                    "tjsj": now_time,
                    "xrywz": renyuanweizhi,
                    "xq": xiaoqu,
                    "gj": "",
                    "jtgj": "",
                    "jkzk": "1",
                    "jkqk": "1",
                    "tw": tw,
                    "sd": period[0],
                    "bz": "",
                    "_ext": "{}"}
        else:
            data = {"sqrid": info_dict["sqrid"],
                    "sqbmid": info_dict["sqbmid"],
                    "rysf": info_dict["rysf"],
                    "sqrmc": info_dict["sqrmc"],
                    "gh": info_dict["gh"],
                    "sfzh": info_dict["sfzh"],
                    "sqbmmc": info_dict["sqbmmc"],
                    "xb": info_dict["xb"],
                    "lxdh": info_dict["lxdh"],
                    "nl": info_dict["nl"],
                    "tjsj": now_time,
                    "xrywz": renyuanweizhi,
                    "sheng": sheng,
                    "shi": shi,
                    "qu": qu,
                    "jtdzinput": jtdz,
                    "gj": "",
                    "jtgj": "",
                    "jkzk": "1",
                    "jkqk": "1",
                    "tw": tw,
                    "sd": period[0],
                    "bz": "",
                    "_ext": "{}"}
        print("----------")
        print("uncoded:", data)
        encode_data = base64.b64encode(str(data).encode("utf-8"))
        print("encoded:", encode_data)
        json_data = {"params": encode_data.decode()}
        print("json_data:", json.dumps(json_data))
        print("----------")
        verification_code = self.get_update_captcha(cookie)
        update_url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn?gh={gh}".format(gh=info_dict["gh"])
        headers = {
            'Content-Type': 'text/json',
            'Origin': 'https://web-vpn.sues.edu.cn',
            'Referer': 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 92.0.4515.131Safari / 537.36',
            'verification-code': verification_code
        }
        if debug_mode:
            print(json_data)
            print(update_url)
            sys.exit()
        response = requests.post(update_url, headers=headers, data=json.dumps(json_data), cookies=cookie)
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

    def get_history_workflow(self, tjsj=time.strftime("%Y-%m-%d", time.localtime()), sd="上午"):
        stat1 = self.web_vpn_state()
        if not stat1:
            return False
        config_stat = self.config_check()
        if not config_stat:
            return False
        stat3 = self.get_execution()
        if not stat3:
            return False
        stat4 = self.login_ff(cookie=stat3["main_cookies_dict"], execution=stat3["main_execution"],
                             uname=config_stat["uname"], password=config_stat["password"])
        if not stat4:
            return False
        stat5 = self.get_history(cookie=stat3["main_cookies_dict"], tjsj=tjsj, sd=sd)
        return stat5
    
    def update_workflow(self, debug_mode=False):
        stat1 = self.web_vpn_state()
        if not stat1:
            return False
        config_stat = self.config_check()
        if not config_stat:
            return False
        stat3 = self.get_execution()
        if not stat3:
            return False
        stat4 = self.login_ff(cookie=stat3["main_cookies_dict"], execution=stat3["main_execution"],
                             uname=config_stat["uname"], password=config_stat["password"])
        if not stat4:
            return False
        update_stat = self.update(cookie=stat3["main_cookies_dict"], renyuanweizhi=config_stat["renyuanweizhi"], 
                                  xiaoqu=config_stat["xiaoqu"], tw=config_stat["tw"], sheng=config_stat["sheng"],
                                  shi=config_stat["shi"], qu=config_stat["qu"], jtdz=config_stat["jtdz"],
                                  debug_mode=debug_mode)
        if not update_stat:
            return False
        return True


if __name__ == "__main__":
    run = Main()
    run.update_workflow(debug_mode=False)
