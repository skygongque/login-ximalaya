# login-ximalaya
login ximalaya with requests

# recognize captcha in file discriminate.py
use opencv-python

# post login/pwd/v1 to login
password RSA/PKCS1_v1_5/base64encode

`
modules = "009585A4773ABEECB949701D49762F2DFAB9599BA19DFE1E1A2FA200E32E0444F426DA528912D9EA8669515F6F1014C454E1343B97ABF7C10FE49D520A6999C66B230E0730C3F802D136A892501FF2B13D699B5C7ECBBFEF428AC36D3D83A5BD627F18746A7FDC774C12A38DE2760A3B95C653C10D7EB7F84722976251F649556B"

exponent = '10001'

`

signature upper/sha1

`
raw = f"account={account}&nonce={nonce}&password={password}&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"

signature =hashlib.sha1(raw.upper().encode()).hexdigest()

`

need to add cookie

`
cookies={'fds_otp':retfromcaptchaverify['token']}

`

