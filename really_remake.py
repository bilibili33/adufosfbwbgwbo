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
        # print("Ver1.0 createTime:20211205\nӦ��ѧУ��վ���£�������֤���Ӧ���������Ǵ������")
        # print("Ver1.1 crateTime:20211213\n˵�����ҳ������ύʱ�����Ҫ����֤�룬�Լ�����д��һ��")
        # print("Ver1.2 crateTime:20211214\n˵����������֤��ʶ��⣬���ö���װ���")
        print("Ver1.3 crateTime:20211216\n˵��������base64")
    def warn_bubble(self, msg):
        print("Warning: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("��������", msg, icon_path=r'fxxk_tiwen.ico')

    def info_bubble(self, msg):
        print("Info: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("��ʾ��Ϣ", msg, icon_path=r'fxxk_tiwen.ico')

    def printLine(self):
        i = 0
        while i < 100:
            print("=", end='')
            i += 1
        print("")

    def set_readme(self):
        with open("readme.txt", "w") as info1:
            info1.write('''��˵���������ļ�������ʱ����д���벻Ҫ���ڼ�¼��Ҫ���ݣ���������ļ���ը�˸Ĳ�����ɾ������\n\n
            ��һ��ʹ�ñ��ű�������ɺ�ȥ��ҳ��ȷ��һ��\n\n������Ҫ����ȥ���ܣ���ַhttps://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n
            ���·�Χ��36-37���������뱣��һλС��\nrenyuanweizhi����Աλ�ã�1����У��2���ڻ�\nxiaoqu��У����1���ɽ���2�Ǻ�ڣ�3�ǳ���''')

    def web_vpn_state(self):
        self.printLine()
        print(">>> web-vpn state <<<")
        main_url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login"
        response = requests.get(url=main_url)
        if response.ok:
            print("��ǰwebvpnҳ��״̬��", response.status_code)
            return True
        else:
            print("��ǰwebvpnҳ��״̬��", response.status_code)
            print("�޷��������ʣ����Ժ�����")
            return False

    def configCheck(self):
        self.printLine()
        print(">>> Config_Check <<<")
        # try 1 �Ƿ����������ļ�
        try:
            with open("config.json") as config_f:
                config = json.load(config_f)
        except (UnboundLocalError, FileNotFoundError):
            self.warn_bubble("�����ļ������ڻ����ƴ���")
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
            self.info_bubble("�Ѵ����µ������ļ������޸ĺ������ű�")
            self.set_readme()
            return False
        # try 2 Ԫ�ض�Ӧ
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
            self.warn_bubble("���������ļ��ڵ� ��ʽ�Ƿ���ȷ �� Ԫ�����Ƿ�����ģ�")
            self.set_readme()
            return False
        # try 3 ����ֵ���
        try:
            tw = float(self.tw)
            tw = round(tw, 1)
            print("��ǰtw:", tw)
            if tw == 36.0:
                self.tw = 36
            elif tw == 37.0:
                self.tw = 37
            elif 36 <= tw <= 37:
                self.tw = tw
            else:
                self.warn_bubble("����ֵ����ȷ����鿴˵��")
                self.set_readme()
                return False
            print("tw check pass.")
        except ValueError:
            self.warn_bubble("�벻Ҫ��tw������ֶ���")
            self.set_readme()
            return False
        # try 4 ������
        if len(self.password1) != 256:
            self.warn_bubble("���������ȥ���ܣ�Ҳ������ܶ�����ٸ�����һ��")
            self.set_readme()
            return False
        else:
            print("password check pass.")
        # try 5 ��Աλ�ü��
        try:
            if self.renyuanweizhi == "1" or self.renyuanweizhi == "2":
                print("��Աλ��check pass")
            else:
                self.warn_bubble("��Աλ�ü�����������Աλ�õĲ���ֵ")
                return False
        except:
            self.warn_bubble("�벻Ҫ��renyuanweizhi���������1��2����Ĳ���")
            return False
        # try 6 У�����
        try:
            if self.renyuanweizhi == "1":
                if self.xiaoqu == "1" or self.xiaoqu == "2" or self.xiaoqu == "3":
                    print("У��check pass")
                else:
                    self.warn_bubble("У������������У���Ĳ���")
                    return False
        except:
            self.warn_bubble("У���������벻Ҫ��xiaoqu���������1��2��3����Ĳ���")
            return False

        return True

    # def captcha2str(self):
    #     path = f"captcha.jpg"
    #     captcha = Image.open(path)
    #     result = pytesseract.image_to_string(captcha)
    #     print('��֤�룺'+ result.replace('\n', ''))
    #     return result.replace('\n', '')

    def captcha2str_ddddocr(self):
        ocr = ddddocr.DdddOcr()
        with open("captcha.jpg", 'rb') as captcha:
            img1 = captcha.read()
        result = ocr.classification(img1)
        print("��֤�룺", result)
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
            self.warn_bubble("���糬ʱ�������Ƿ������������������û��")
            return False
        # �� cookie
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
            self.warn_bubble("cookiesת��ʧ��")
            return False
        self.main_execution = execution
        return execution

    def getCaptcha(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("δ����getExecution")
            self.getExecution()
        # ��ȡ��֤��ͼƬ
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
        print("��ǰλ�ã�Login ����")
        if self.main_cookies_dict == {}:
            self.warn_bubble("δ����getExecution��getCaptcha")
            return False
        elif self.uname == "" or self.password1 == "":
            self.warn_bubble("�û���������Ϊ��")
            return False
        execution = self.main_execution
        # k�ǵ�¼ѭ����j����֤��ʶ��ѭ������ѭ�����ۼ���֤��ʶ��������
        k = 0
        while k < 3:

            j = 0
            while j < 5:
                try:
                    captcha_str = self.getCaptcha()
                    captcha_str1 = int(captcha_str)
                    # ���и�������֤����Ϊ֮ǰ�õ��� pytesseract
                    print("��ǰcaptcha���ͣ�", type(captcha_str1))
                    print(f"��ǰ��֤��ʶ��ѭ���Σ�{j+1}/5 ���5��")
                    break
                except:
                    print('��ǰ��֤����ȷ������')
                    j += 1
                    time.sleep(1)
                if j == 4:
                    print("��֤���ȡ����")
                    return False
            self.printLine()
            print(">>> Login_start <<<")
            print(f"��ǰ��¼ѭ���Σ�{k+1}/3 ���3��")
            url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
            payload = f'username={self.uname}&password={self.password1}&authcode={captcha_str}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }
            session1 = requests.post(url=url, headers=headers, data=payload, cookies=self.main_cookies_dict)
            # ��ʱӦ����ɵ�¼
            try:
                soup_v1 = bs4.BeautifulSoup(session1.text, "html.parser")
                value1 = soup_v1.select('div[id="msg"] > h2')[0].get_text()
                print(value1)
                # self.info_bubble("ҳ����ʾ��Ϣ��" + value1)
                print("ҳ����ʾ��Ϣ��" + value1)
                if value1 == '��¼�ɹ�':
                    break
                else:
                    print("��������֤�����׼������")
                    time.sleep(1)
            except:
                print("��������֤�����׼������")
                time.sleep(1)

            k += 1
            if k == 2:
                self.warn_bubble("ѭ�����Σ���¼����û�л�ȡ�� html ����ֵ����ȷ���˺��������������")
                self.warn_bubble("���ȷ���˺�������������ҳ��������¼���뷴��������")
                return False

        # 302 �Զ���תʹ cookies ��Ч
        self.printLine()
        print(">>> 302 <<<")
        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=self.main_cookies_dict)
        print("web-vpn��ҳ�ض���״̬��", response.status_code)
        return True
        # ��֪����ʲô�õ���return�˸�True

    # ����涼��֮ǰû�Ĺ���ʺɽ

    def get_history(self,tjsj=time.strftime("%Y-%m-%d", time.localtime()),sd="����"):
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
            print("��ǰ�ֵ䳤�ȣ�",dict11)
            return True
        except:
            print('δ��ȡ����ǰʱ�ε��ֵ䣺History no data.')
            return False

    def get_Near_history(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("δ����getExecution��getCaptcha")
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
        print(f"���������{jkqk}������״����{jkzk}")
        if jkqk != "1" or jkzk != "1":
            print('���棺\n��ǰ��ȡ�������һ�������еĽ�������ͽ���״����������ȷ����ȷ������webvpn�ϵĽ���״������')
            print('���ȷ����ҳ����Ϣ�����⣬����ͣʹ�ñ��ű���Ȼ����ϵ����')
            print("����״��Ĭ��Ϊ 1 ����Ϊ�����á����������Ĭ��Ϊ 1 ����Ϊ�������������")
            # print('�������������ִ�У������Ϊ��Ϣȷʵ�����⵼�±�ͨ���������߲�����')
            time.sleep(30)
            print("\n�˴��ȴ�30��")
            sys.exit()

        newList = [self.sqrid,self.sqbmid,self.rysf,self.sqrmc,self.gh,self.sfzh,self.sqbmmc,self.xb,self.lxdh,self.nl]
        meaning_of_list=["������ID","������MID","��Ա���","����������","����","���֤��","���벿������","ϵ��","��ϵ�绰","����"]
        print("----------")
        print("### ������Ϣ ###")
        for meaning_list,data_list in zip(meaning_of_list,newList):
            print(meaning_list,":",data_list)
        print("----------")

    def get_post_captcha(self):
        self.printLine()
        if self.main_cookies_dict == {}:
            self.warn_bubble("δ����getExecution")
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
        print("captcha_code��", captcha_code)
        return captcha_code

    def update(self, debug_mode=False):
        nowTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        nowHour = int(time.strftime("%H", time.localtime()))
        print("��ǰʱ�䣺 ", nowTime)
        print("��ǰСʱ��", nowHour)
        if 00 <= nowHour < 12:
            sd = "����"
            print(sd)
        else:
            sd = "����"
            print(sd)
        # ʱ�μ��
        if 00 <= nowHour < 3:
            self.info_bubble("ϵͳά��ʱ�䣬��ʱ�޷����н������0-3�㲻���")
            return False

        queryNear = self.get_history(sd=sd)
        if queryNear:
            self.info_bubble("��ǰʱ���Ѿ������")
            time.sleep(10)
            sys.exit()
        #     �������� 1
        else:
            verification_code = self.get_post_captcha()
            self.history2dict()
            if self.sqrmc == "":
                self.warn_bubble("δ��ȡ����ȷ��Ϣ���쳣�˳�")
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
                    self.info_bubble("�ύ�ɹ�")
                    time.sleep(10)
                    return True
                else:
                    print("�ύ���ɹ�")
                    print("Debug: " + response.text)
                    time.sleep(10)
                    return False
            except:
                # ���������ģ������ϲ����ܵ���
                print("������ʱ�β���ȷ")
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
        # ֱ���˳�
        else:
            self.update(debug_mode)
            # self.get_history(tjsj="2021-12-10")
            pass

# update �� debug mode �Ͳ��ύ
do = Main()
do.af(debug_mode=False)
