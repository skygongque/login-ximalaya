import requests
from get_captcha import Captcha
import execjs
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import hashlib
import json
import time
requests.packages.urllib3.disable_warnings()

def get_sessionId():
    jstext = """ 
    function get_sessionId(){
    var t, o;
    var sessionId;
    o = +new Date,
    sessionId = "" + (t || "xm_") + o.toString(36) + Math.random().toString(36).substr(2, 6)
    return sessionId
    }
    """
    ctx = execjs.compile(jstext)
    sessionId = ctx.call('get_sessionId')
    return sessionId

class Ximalaya:
    def __init__(self):
        self.sessionId = get_sessionId()
        # self.sessionId = 'xm_k6ptqdnoapge1w'
        self.nonce_url = 'https://passport.ximalaya.com/web/nonce/'
        self.login_url = 'https://passport.ximalaya.com/web/login/pwd/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }
        self.captcha = Captcha(self.sessionId)
        self.token = None
        self.session = requests.Session()
        self.web_pl_url = "https://mermaid.ximalaya.com/collector/web-pl/v1"
        self.login_headers = {
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '359',
            'Content-Type': 'application/json',
            # 'Cookie': '_xmLog=xm_k6nhsw6tl2n3fq; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1581837776,1581840339,1581850690,1581905520; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1581905520; fds_otp=7400888312179453443',
            'Host': 'passport.ximalaya.com',
            'Origin': 'https://www.ximalaya.com',
            'Referer': 'https://www.ximalaya.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        }
        self.session.headers.update(self.login_headers)

    def captcha_verify(self):
        """ 获得滑动验证通过后的token,最后的登录post需要添加到cookie中 """
        for i in range(10):
            if self.token:
                break
            self.token = self.captcha.check_captcha()
            time.sleep(1)
        time.sleep(1)
    

    def get_nonce(self):
        # 此处cookies可加可不加
        cookies={'fds_otp':self.token}
        # print(cookies)
        response = self.session.get(self.nonce_url+Captcha.get_time(),verify=False)
        return response.json()['nonce']

    def encrypt_password(self,password):
        """ rsa加密密码,并用base64编码 """
        modules = "009585A4773ABEECB949701D49762F2DFAB9599BA19DFE1E1A2FA200E32E0444F426DA528912D9EA8669515F6F1014C454E1343B97ABF7C10FE49D520A6999C66B230E0730C3F802D136A892501FF2B13D699B5C7ECBBFEF428AC36D3D83A5BD627F18746A7FDC774C12A38DE2760A3B95C653C10D7EB7F84722976251F649556B"
        rsa_public_key = RSA.construct((int(modules,16),int('10001',16)))
        cipher_rsa = PKCS1_v1_5.new(rsa_public_key)
        temp = cipher_rsa.encrypt(password.encode())
        return base64.b64encode(temp)

    def get_signature(self,account,nonce,password):
        """ sha1进行签名 """
        # 签名前大写upper()
        raw = f"account={account}&nonce={nonce}&password={password}&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"
        return hashlib.sha1(raw.upper().encode()).hexdigest()


    def get_login_data(self,account,password):
        nonce = self.get_nonce()
        encrypted_password = self.encrypt_password(password)
        encrypted_password = str(encrypted_password,'utf-8')
        post_data = {
            'account': account,
            'password': encrypted_password,
            'nonce': nonce,
            'signature': self.get_signature(account,nonce,encrypted_password),
            'rememberMe': 'false',
        }
        return post_data
        
    def login(self,account,password):
        post_data = self.get_login_data(account,password)
        print(json.dumps(post_data))
        cookies={'fds_otp':self.token}
        # 最核心post请求cookie必须加
        response = self.session.post(self.login_url,data=json.dumps(post_data),cookies=cookies,verify=False)
        if response.status_code==200:
            print(response.json())
        else:
            print(response.text)

    def run(self):
        account = ''
        password = ''
        self.captcha_verify()
        self.login(account,password)
        return self.session.cookies


if __name__ == "__main__":
    t = Ximalaya()
    login_cookie = t.run()
    print(login_cookie)