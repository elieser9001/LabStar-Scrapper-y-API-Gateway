import requests, pickle
import urllib.parse
import re
import hmac, hashlib
import os
from dotenv import load_dotenv
load_dotenv()

class SessionManager:
    def __init__(self):
        self.__username = os.getenv('LABSTAR_USER')
        self.__password = os.getenv('LABSTAR_PASSWORD')
        self.__cookie_filename = 'cookies.dat'
        self.session = requests.Session()
        self.bearer = None
        self.__auth_key = None
        self.initialize()
       
    def is_session_valid(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer ' + self.bearer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36',
            'Sec-Ch-Ua-Platform': '""',
            'Origin': 'https://gro3x.labstar.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://gro3x.labstar.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = self.session.get('https://ls-api.labstar.com', headers=headers)
        
        return response.status_code == 200

    def load_session(self):
        with open(self.__cookie_filename, 'rb') as f:
            self.session.cookies.update(pickle.load(f))
            self.bearer = urllib.parse.unquote(self.session.cookies['gro3x%2Elabstar%2Ecom%5Fjat'])
        
    def save_session(self):
        with open(self.__cookie_filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def __get_auth_key(self):
        headers = {
            'authority': 'gro3x.labstar.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://gro3x.labstar.com/pages/admin/case_flow_management/index.asp',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        response = self.session.get('https://gro3x.labstar.com/site_inc/account_login.asp', headers=headers)
        login_form_html = response.text
        
        pattern = r"var auth = '([^']*)';"
        matches = re.search(pattern, login_form_html)

        if matches:
            auth_seed = matches.group(1)
            auth_key = hmac.new(auth_seed.encode(), auth_seed.encode(), digestmod='MD5').hexdigest().upper()
            
            return auth_key
        else:
            print("Auth seed not found.")
            return None
        
    def login(self):
        md5pass = hashlib.md5(self.__password.encode()).hexdigest().upper()
        
        data = {
            'username': self.__username,
            'password': self.__password,
            'Submit1': 'Login',
            'javascript_enabled': '1',
            'cmd': 'login',
            'md5pass': md5pass,
            'dest': '/pages/admin/case_list.asp?page=manufacture_manager&defaultTab=checkin&client_checked=0&manu_checked=-1',
            'auth_key': self.__auth_key,
        }

        response = self.session.post(
            'https://gro3x.labstar.com/site_inc/account_login.asp',
            data=data,
        )
        
        return response.status_code == 200
    
    def initialize(self):
        self.load_session()
        
        if self.is_session_valid() == False:
            self.__auth_key = self.__get_auth_key()
            is_logged = self.login()
            
            if is_logged:
                self.save_session()
                self.load_session()
