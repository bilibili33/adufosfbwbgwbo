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
        # print("Ver1.0 createTime:20211205\nӦ��ѧУ��վ���£�������֤���Ӧ���������Ǵ������")
        # print("Ver1.1 createTime:20211213\n˵�����ҳ������ύʱ�����Ҫ����֤�룬�Լ�����д��һ��")
        # print("Ver1.2 createTime:20211214\n˵����������֤��ʶ��⣬���ö���װ���")
        # print("Ver1.3 createTime:20211216\n˵��������base64")
        # print("Ver1.4 createTime:20211226\n˵�������Ϲ�����ڷ������������ˣ��˰汾������ʹ��")
        print("Ver2.0 createTime:20211229\n˵�����ع�����������ȥ�����ȫ�ֱ���")
        print("Ver2.1 createTime:20211229\n˵����С��һ����֤config�߼�")

    def warn_bubble(self, msg):
        print("Warning: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("��������", msg, icon_path=r'fxxk_tiwen.ico')

    def info_bubble(self, msg):
        print("Info: ", msg)
        toaster = ToastNotifier()
        toaster.show_toast("��ʾ��Ϣ", msg, icon_path=r'fxxk_tiwen.ico')

    def print_line(self):
        i = 0
        while i < 100:
            print("=", end='')
            i += 1
        print("")

    def set_readme(self):
        if not os.path.exists("readme.txt"):
            with open("readme.txt", "w") as info1:
                info1.write('''��˵���������ļ�������ʱ����д���벻Ҫ���ڼ�¼��Ҫ���ݣ���������ļ���ը�˸Ĳ�����ɾ������\n\n
                ��һ��ʹ�ñ��ű�������ɺ�ȥ��ҳ��ȷ��һ��\n\n������Ҫ����ȥ���ܣ���ַhttps://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n
                ���·�Χ��36-37���������뱣��һλС��\nrenyuanweizhi����Աλ�ã�1����У��2���ڻ�\nxiaoqu��У����1���ɽ���2�Ǻ�ڣ�3�ǳ���''')
        else:
            pass

    def web_vpn_state(self):
        self.print_line()
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

    def config_check(self):
        self.print_line()
        print(">>> Config_Check <<<")
        # try 1 �Ƿ����������ļ�
        try:
            with open("config.json", encoding='utf-8') as config_f:
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
            self.warn_bubble("���������ļ��ڵ� ��ʽ�Ƿ���ȷ �� Ԫ�����Ƿ�����ģ�")
            self.set_readme()
            return False
        # try 3 ����ֵ���
        try:
            tw = float(tw)
            tw = round(tw, 1)
            print("��ǰtw:", tw)
            if tw == 36.0:
                current_tw = 36
            elif tw == 37.0:
                current_tw = 37
            elif 36 <= tw <= 37:
                current_tw = tw
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
        if len(password1) != 256:
            self.warn_bubble("���������ȥ���ܣ�Ҳ������ܶ�����ٸ�����һ��")
            self.set_readme()
            return False
        else:
            print("password check pass.")
        # try 5 ��Աλ�ü��
        try:
            if renyuanweizhi == "1" or renyuanweizhi == "2":
                print("��Աλ��check pass")
            else:
                self.warn_bubble("��Աλ�ü�����������Աλ�õĲ���ֵ")
                return False
        except:
            self.warn_bubble("�벻Ҫ��renyuanweizhi���������1��2����Ĳ���")
            return False
        # try 6 У�����
        try:
            if renyuanweizhi == "1":
                if xiaoqu == "1" or xiaoqu == "2" or xiaoqu == "3":
                    print("У��check pass")
                else:
                    self.warn_bubble("У������������У���Ĳ���")
                    return False
        except:
            self.warn_bubble("У���������벻Ҫ��xiaoqu���������1��2��3����Ĳ���")
            return False
        result_dict = {"uname": uname, "password": password1, "tw": current_tw, "renyuanweizhi": renyuanweizhi, 
                       "xiaoqu": xiaoqu, "sheng": sheng, "shi": shi, "qu": qu, "jtdz": jiatindizhi}
        return result_dict

    def captcha2str_ddddocr(self):
        ocr = ddddocr.DdddOcr()
        with open("captcha.jpg", 'rb') as captcha:
            img1 = captcha.read()
        result = ocr.classification(img1)
        print("��֤�룺", result)
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
            self.warn_bubble("���糬ʱ�������Ƿ������������������û��")
            return False
        # �� cookie
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
            self.warn_bubble("cookiesת��ʧ��")
            return False
        main_execution = execution
        return {"main_execution": main_execution, "main_cookies_dict": main_cookies_dict}

    def get_captcha(self, cookie: dict):
        self.print_line()
        # ��ȡ��֤��ͼƬ
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
        print("��ǰλ�ã�Login ����")
        # k�ǵ�¼ѭ����j����֤��ʶ��ѭ������ѭ�����ۼ���֤��ʶ��������
        k = 0
        while k < 3:

            j = 0
            while j < 5:
                try:
                    captcha_str = self.get_captcha(cookie)
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
            self.print_line()
            print(">>> Login_start <<<")
            print(f"��ǰ��¼ѭ���Σ�{k+1}/3 ���3��")
            url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
            payload = f'username={uname}&password={password}&authcode={captcha_str}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }
            session1 = requests.post(url=url, headers=headers, data=payload, cookies=cookie)
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
        self.print_line()
        print(">>> 302 <<<")
        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=cookie)
        print("web-vpn��ҳ�ض���״̬��", response.status_code)
        return True

    def get_history(self, cookie: dict, tjsj=time.strftime("%Y-%m-%d", time.localtime()), sd="����"):
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

            data_dict = {"������ID": sqrid, "������MID": sqbmid, "��Ա���": rysf, "����������": sqrmc, "����": gh,
                         "���֤��": sfzh, "���벿������": sqbmmc, "ϵ��": xb, "��ϵ�绰": lxdh, "����": nl, "�������": jkqk,
                         "����״��": jkzk}
            print("----------")
            print("### �ֵ���Ϣ ###")
            for key, value in data_dict.items():
                print(key, ":", value)
            print("----------")
            result_dict = {"sqrid": sqrid, "sqbmid": sqbmid, "rysf": rysf, "sqrmc": sqrmc, "gh": gh, "sfzh": sfzh,
                           "sqbmmc": sqbmmc, "xb": xb, "lxdh": lxdh, "nl": nl, "jkqk": jkqk, "jkzk": jkzk}
            return result_dict
        except:
            print("�������")
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
        print("captcha_code��", captcha_code)
        return captcha_code

    def get_period(self):
        nowHour = int(time.strftime("%H", time.localtime()))
        print("��ǰСʱ��", nowHour)
        if 00 <= nowHour < 12:
            sd = "����"
        else:
            sd = "����"
        print("��ǰʱ�Σ�", sd)
        return [sd, nowHour]

    def update(self, cookie: dict, renyuanweizhi, xiaoqu, sheng, shi, qu, jtdz, tw, debug_mode=False):
        period = self.get_period()
        if debug_mode:
            print("debug�ѿ���������ʱ�μ��͵�ǰʱ����ʷ���")
        else:
            # ʱ�μ��
            if 00 <= period[1] < 3:
                self.info_bubble("ϵͳά��ʱ�䣬��ʱ�޷����н������0-3�㲻���")
                return False
            # ��ǰʱ������
            if_today = self.get_history(sd=period[0], cookie=cookie)
            try:
                dict11 = len(json.loads(if_today)["resultData"][0])
                print("��ǰ�ֵ䳤�ȣ�", dict11)
                self.info_bubble("��ǰʱ���Ѿ������")
                return True
                # �������� 1
            except:
                print('δ��ȡ����ǰʱ�ε��ֵ䣺History no data.')
                pass

        now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print("��ǰʱ�䣺 ", now_time)
        response = self.get_Near_history(cookie)
        info_dict = self.history2dict(response)
        print("���������{jkqk}������״����{jkzk}".format(jkqk=info_dict["jkqk"], jkzk=info_dict["jkzk"]))

        if info_dict["jkqk"] != "1" or info_dict["jkzk"] != "1":
            print('���棺\n��ǰ��ȡ�������һ�������еĽ�������ͽ���״����������ȷ����ȷ������webvpn�ϵĽ���״������')
            print('���ȷ����ҳ����Ϣ�����⣬����ͣʹ�ñ��ű���Ȼ����ϵ����')
            print("����״��Ĭ��Ϊ 1 ����Ϊ�����á����������Ĭ��Ϊ 1 ����Ϊ�������������")
            # print('�������������ִ�У������Ϊ��Ϣȷʵ�����⵼�±�ͨ���������߲�����')
            print("\n�˴��ȴ�30��")
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

    def get_history_workflow(self, tjsj=time.strftime("%Y-%m-%d", time.localtime()), sd="����"):
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
