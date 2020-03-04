import uuid, hmac, json, urllib, hashlib
import requests as req

USER_AGENT = 'Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
SIG_KEY = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178'
SIG_VER = '4'

def get_header():
    return {
        'User-Agent': USER_AGENT,
    }

def get_csrftoken(guid):
    url = 'https://i.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid={}'
    sess = req.Session()
    sess.get(url.format(guid), headers=get_header())
    return sess.cookies.get('csrftoken')

def get_device_id(username):
    uhash = hashlib.md5()
    uhash.update(username.encode('utf-8') + str(uuid.uuid4()).encode('utf-8'))
    dhash = hashlib.md5()
    dhash.update(uhash.hexdigest().encode('utf-8') + '12435'.encode('utf-8'))
    return 'android-{}'.format(dhash.hexdigest()[:16])

def login(username, password, csrftoken, guid, device_id):
    url = 'https://i.instagram.com/api/v1/accounts/login/ig_sig_key_version={}&signed_body={}.{}'
    jdata = json.dumps({
        'guid': guid,
        'phone_id': guid,
        '_csrftoken': csrftoken,
        'username': username,
        'device_id': device_id,
        'password': password,
        'login_attempt_count': 0,
    })
    hmac_signed = hmac.new(SIG_KEY.encode('utf-8'), jdata.encode('utf-8'), hashlib.sha256).hexdigest()
    sess = req.Session()
    res = sess.post(url.format(SIG_VER, hmac_signed, urllib.parse.quote(jdata)))
    print(url.format(SIG_VER, hmac_signed, urllib.parse.quote(jdata)))
    print(res)
    with open('res.html', 'w') as f:
        f.write(res.text)

if __name__ == '__main__':
    print('generating guid ... ')
    guid = str(uuid.uuid4())
    print('getting csrf token ... ')
    csrf = get_csrftoken(guid)
    print('setting uname + pwd ... ')
    username = 'matt_moony'
    password = '20iMaPauMorMo03'
    print('getting device-id ... ')
    device_id = get_device_id(username)
    print('logging in ... ')
    login(username, password, csrf, guid, device_id)