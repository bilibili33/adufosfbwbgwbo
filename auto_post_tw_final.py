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
        print("ɾ��˵���ļ��������֣�����sqrmc��飬����jkqk��jkzk���")
        print('==================================================================================\n >>> config checking <<<\n ')
        self.config_file()
        print('==================================================================================')
        self.get_cookies_dict()

    def config_file(self):
        try:
            with open("config.json") as config_f:
                config = json.load(config_f)
        except (UnboundLocalError, FileNotFoundError):
            print("�����ļ������ڻ����ƴ���\n")
            with open("config.json", 'w') as new_config:
                new_config.write('''{
    "account": "",
    "password": "",
    "tw": "36.6"
}''')
            print("�Ѵ����µ������ļ������޸ĺ������ű�")
            self.set_readme()
            os.system('pause')
            sys.exit()

        try:
            self.uname = config['account']
            self.password1 = config['password']
            self.tw = config['tw']
        except KeyError:
            print("���������ļ��ڵ� ��ʽ�Ƿ���ȷ �� Ԫ�����Ƿ�����ģ�")
            self.set_readme()
            os.system('pause')
            sys.exit()
        self.tw_check()
        self.passwd_check()
        if self.uname == "":
            print("�����û�����")
            os.system('pause')
            sys.exit()
        else:
            print("account check pass ���û�����Ϊ��")

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
                print("����ֵ����ȷ����鿴˵��")
                self.set_readme()
                os.system('pause')
                sys.exit()
            print("response:", self.tw)
            print("tw check pass.")
        except ValueError:
            print("�벻Ҫ��tw������ֶ���")
            self.set_readme()
            os.system('pause')
            sys.exit()

    def passwd_check(self):
        if len(self.password1) != 256:
            print("���������ȥ���ܣ�Ҳ������ܶ�����ٸ�����һ��")
            self.set_readme()
            os.system('pause')
            sys.exit()
        else:
            print("password check pass.")

    def set_readme(self):
        with open("readme.txt","w") as info1:
            info1.write('��˵���������ļ�������ʱ����д���벻Ҫ���ڼ�¼��Ҫ���ݣ���������ļ���ը�˸Ĳ�����ɾ������\n\n��һ��ʹ�ñ��ű�������ɺ�ȥ��ҳ��ȷ��һ��\n\n������Ҫ����ȥ���ܣ���ַhttps://bilibili33.github.io/rsa_passwd_for_web_vpn.github.io/\n���·�Χ��36-37���������뱣��һλС��')

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
            print("���糬ʱ�������Ƿ������������������û��")
            os.system('pause')
            sys.exit()
        # ��ȡ execution ����

    def get_cookies_dict(self,debug_mode=False):
        if self.uname == "" or self.password1 == "":
            sys.exit()  # ���Ǳ��մ�ʩ����ȻӦ���ò���
        execution = self.get_execution()
        main_session = requests.session()
        print('==================================================================================\n >>> Login_start <<<\n ')

        url = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421f3f652d234256d43300d8db9d6562d/cas/login'
        payload = f'username={self.uname}&password={self.password1}&execution={execution}&encrypted=true&_eventId=submit&loginType=1&submit=%E7%99%BB%2B%E5%BD%95'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        s = main_session.post(url=url, headers=headers, data=payload)  # ��½�Ự
        # ��¼��鿪ʼ
        try:
            soup_v1 = bs4.BeautifulSoup(s.text, "html.parser")
            value1 = soup_v1.select('div[id="msg"] > h2')[0].get_text()
            print("��ʾ��Ϣ�� ",value1)
            success = '��¼�ɹ�'
            if value1 == success:
                pass
            else:
                print("��¼����û�л�ȡ��html����ֵ����ȷ���˺��������������")
                print("���ȷ���˺�������������ҳ��������¼���뷴��������")
                os.system('pause')
                sys.exit()
        except:
            print("��¼����û�л�ȡ��html����ֵ����ȷ���˺��������������")
            print("���ȷ���˺�������������ҳ��������¼���뷴��������")
            os.system('pause')
            sys.exit()
        # ��¼������
        if debug_mode:
            print("Debug: ��¼������")
            sys.exit()
        # ��ӡ��½ҳ��
        # print('----------------------------------\n'+s.text+'----------------------------------\n')

        # ��ӡԭʼ headers �� cookies
        print(s.headers, '\n')
        print(s.headers.get('Set-Cookie'))

        print('----------------------------------------------------------------------------------')

        # cookies ת�ֵ� Ȼ�����
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        print('origin_dict:  ', cookies_dict)
        cookies_dict['refresh'] = '1'
        cookies_dict['show_vpn'] = '1'
        print('\n')
        print('current_dict:   ', cookies_dict)
        self.main_cookies_dict = cookies_dict
        # ����ȫ��cookies
        print('==================================================================================')
        print('==================================================================================\n >>> 302 <<<\n ')

        url302 = 'https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/jkxxcj.jsp'
        headers302 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://web-vpn.sues.edu.cn/'
        }
        response = requests.get(url=url302, headers=headers302, cookies=self.main_cookies_dict)
        print("�ض���״̬�� ",response.status_code)

        # print(response.text.encode('utf-8'))

        return cookies_dict


    def get_history(self,tjsj=time.strftime("%Y-%m-%d", time.localtime()),sd="����"):

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
            print("��ǰ�ֵ䳤�ȣ�",dict11)
            return True
        except:
            print('δ��ȡ����ǰʱ�ε��ֵ䣺History no data.')
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
        print(f"���������{jkqk}������״����{jkzk}")
        if jkqk != "1" or jkzk != "1":
            print('���棺\n��ǰ��ȡ�������һ�������еĽ�������ͽ���״����������ȷ����ȷ������webvpn�ϵĽ���״������')
            print('���ȷ����ҳ����Ϣ�����⣬����ͣʹ�ñ��ű���Ȼ����ϵ����')
            print("����״��Ĭ��Ϊ 1 ����Ϊ�����á����������Ĭ��Ϊ 1 ����Ϊ�������������")
            print('�������������ִ�У������Ϊ��Ϣȷʵ�����⵼�±�ͨ���������߲�����')
            os.system('pause')
        newList = [self.sqrid,self.sqbmid,self.rysf,self.sqrmc,self.gh,self.sfzh,self.sqbmmc,self.xb,self.lxdh,self.nl,self.xrywz,self.sheng,self.shi,self.qu,self.jtdzinput]
        print("----------")
        print("vvv ������Ϣ vvv")
        for checking in newList:
            print(checking)
        print("----------")

    def update(self,debug_mode=False):
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

        if_check = self.get_history(sd=sd)
        if if_check == True and debug_mode == False:
            if not debug_mode:
                print("��ǰʱ���Ѿ������")
                time.sleep(10)
                sys.exit()
            else:
                print("debug exit")
        else:
            self.history2dict()
            url = "https://web-vpn.sues.edu.cn/https/77726476706e69737468656265737421e7f85397213c6747301b9ca98b1b26312700d3d1/default/work/shgcd/jkxxcj/com.sudytech.work.shgcd.jkxxcj.jkxxcj.saveOrUpdate.biz.ext?vpn-12-o2-workflow.sues.edu.cn"
            if self.sqrmc == "":
                print("δ��ȡ����ȷ��Ϣ��ǿ���˳�")
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
                print("�ύ�ɹ�")
                time.sleep(10)
                return True
            else:
                print(response.text)


qwe = Main()

# qwe.get_history(tjsj="2021-09-09",sd="����")
qwe.update(debug_mode=False)
# qwe.get_Near_history()
# qwe.history2dict()