![picture](https://img.shields.io/badge/python-v3.7-brightgreen)
# Login-ximalaya
login ximalaya with requests

# Recognize captcha in file discriminate.py
use opencv-python

# Post login/pwd/v1 to login
### password RSA/PKCS1_v1_5/base64encode

`
modules = "009585A4773ABEECB949701D49762F2DFAB9599BA19DFE1E1A2FA200E32E0444F426DA528912D9EA8669515F6F1014C454E1343B97ABF7C10FE49D520A6999C66B230E0730C3F802D136A892501FF2B13D699B5C7ECBBFEF428AC36D3D83A5BD627F18746A7FDC774C12A38DE2760A3B95C653C10D7EB7F84722976251F649556B"
`

`exponent = '10001'`

### Signature upper/sha1

`
raw = f"account={account}&nonce={nonce}&password={password}&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"
`

`signature =hashlib.sha1(raw.upper().encode()).hexdigest()`

### Need to add cookie

`
cookies={'fds_otp':retfromcaptchaverify['token']}
`

# Example
![this is the example](https://github.com/skygongque/login-ximalaya/blob/master/ximalayapy/%E5%96%9C%E9%A9%AC%E6%8B%89%E9%9B%85%E8%B4%A6%E5%8F%B7%E5%AF%86%E7%A0%81%E7%99%BB%E5%BD%95%E7%BA%AA%E5%BF%B5.png)
