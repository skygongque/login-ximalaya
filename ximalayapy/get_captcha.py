import requests
import time
from discriminate import get_pos
import cv2 as cv
import random
import json

class Captcha:
    def __init__(self,sessionId):
        self.sessionId = sessionId
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }
        self.captcha_url = 'https://mobile.ximalaya.com/captcha-web/check/slide/get'
        self.slide_url = "https://mobile.ximalaya.com/captcha-web/valid/slider"
        
        self.captcha_headers = {
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://www.ximalaya.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.ximalaya.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': '_xmLog=xm_k6nhsw6tl2n3fq; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1581837776,1581840339,1581850690,1581905520; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1581905520; fds_otp=7400888312179453443'
        }
        self.session = requests.Session()
        # self.session.headers.update(self.captcha_headers)
    
    @staticmethod
    def get_time():
        time_url = 'https://www.ximalaya.com/revision/time'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }
        response = requests.get(time_url,headers=headers)
        if response.status_code==200:
            return response.text


    def get_captcha_url(self,sessionId):
        """ 获取captcha_url """
        params = {
            'bpId': '139',
            'sessionId':sessionId ,
        }
        # response = requests.get(self.captcha_url,params=params,headers=self.headers)
        response = self.session.get(self.captcha_url,params=params,headers= self.captcha_headers)
        if response.status_code==200:
            return response.json()

    def downlord_captcha(self,bg_url,bg_name):
        response = requests.get(bg_url,headers=self.headers)
        with open(bg_name,'wb') as f:
            f.write(response.content)
            f.close()
        print('had saved captcha.',bg_name)

    def get_distance(self,bg_name):
        img0 = cv.imread(bg_name)
        result = get_pos(img0)
        # print(result)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return result


    def calculate_captcha_text(self, distance):
        d =float(distance) 
        captcha_text_x = (((0.8*d)+10)*0.9247-9.6)/0.8+44
        return captcha_text_x

    def post_slide(self,captcha_text_X,sessionId):
        text_X = str(int(captcha_text_X))
        post_data = {
            'bpId': '139',
            'sessionId': sessionId,
            'type': "slider",
            'captchaText': text_X+","+str(random.randint(-10,10)),
            'startX': str(500+random.randint(-10,10)),
            'startY': str(180+random.randint(-10,10)),
            'startTime': Captcha.get_time()
        }
        response = self.session.post(self.slide_url,data=json.dumps(post_data),headers=self.captcha_headers)
        if response.status_code==200:
            return response.json()

    def check_captcha(self):
        # sessionId = 'xm_k6oksl4zdvza2u'
        sessionId = self.sessionId
        res_json = self.get_captcha_url(sessionId)
        self.downlord_captcha(res_json['data']['bgUrl'],'captcha_img.jpg')
        distance =  self.get_distance('captcha_img.jpg')
        captcha_text_X = self.calculate_captcha_text(distance)
        check_captcha_res = self.post_slide(captcha_text_X,sessionId)
        if check_captcha_res['result']=='true':
            print('recognized the captcha successfully')
            # return self.session
            return check_captcha_res['token']
        else:
            print('fail to recognized the captcha')    
        

if __name__ == "__main__":
    sessionId = 'xm_k6oksl4zdvza2u'
    t = Captcha(sessionId)
    token = t.check_captcha()
    print(token)

    
        