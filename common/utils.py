import base64
import datetime
import json
import os
import random
import sys
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import quote, unquote


def printf(text):
    ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f'[{ti}]: {text}')
    sys.stdout.flush()


def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def getTimestamp():
    return str(int(round(time.time() * 1000)))

def aesEn(content, key, iv):
    key = key[:16].encode('utf-8')
    iv = iv[:16].encode('utf-8')
    content = iso10126pad(content).encode('utf-8')
    cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
    res = cipher.encrypt(content)
    return base64.b64encode(res).decode('utf-8')


def aesDe(content, key, iv):
    key = key[:16].encode('utf-8')
    iv = iv[:16].encode('utf-8')
    content = base64.b64decode(content)
    cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
    res = cipher.decrypt(content)
    res = res[0:-res[-1]]
    return res.decode('utf-8')


def iso10126pad(text):
    byte = 16 - len(text) % 16
    return (text + generate_random_str(byte - 1) + chr(byte))


def getImgByte(url):
    res = requests.get(url).content
    return res


def getMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr, startIndex)
    return content[startIndex:endIndex]


def baseenco(t):
    before_base64 = t.encode()
    after_base64 = base64.b64encode(before_base64)
    right_base64 = str(after_base64, 'utf-8')
    return right_base64


def getAddressCoordinas(userId, uuid, mini_program_token, Cookie):
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'referer': 'https://i.meituan.com/awp/hfe/block/index.html',
            'cookie': Cookie
        }
        fdata = 'data=%7B%22address_type%22%3A1%7D&login_token=' + mini_program_token + '&login_token_type=0'
        res = requests.request("POST",
                               'https://addressapi.meituan.com/v1/address/list?actual_latitude=0&actual_longitude=0&address_sdk_type=h5&address_sdk_version=1.4.27&biz_id=1101&client_id=6&client_version=10.2.200&device_type=h5&device_version=1.4.27&latitude=0&longitude=0&uuid=' + uuid,
                               headers=headers, data=fdata)
        js = json.loads(res.text)
        if js['code'] != 0:
            return '23.087803571853314_113.27314951033465'
        data = js['data']
        addressList = data['address_list']
        if len(addressList) > 0:
            latitude = float('0.' + str(addressList[0]['latitude'])) * 100
            longitude = float('0.' + str(addressList[0]['longitude'])) * 1000
            coordinas = str(latitude) + '_' + str(longitude)
            return coordinas
        else:
            return '23.087803571853314_113.27314951033465'
    except Exception:
        return '23.087803571853314_113.27314951033465'


def getRiskFrom(userId, uuid, mini_program_token, ck):
    userinfo = '{"userid":"' + userId + '","uuid":"' + uuid + '","touchPoint":"1,1","campaignPlatform":3,"partner":2,"cubeCampaignId":172385,"isVisitedPage":0,"location":"' + getAddressCoordinas(
        userId, uuid, mini_program_token, ck) + '","platform":4,"sourceUserid":0,"fingerprint":"' + generate_random_str(
        1250) + '","version":"11.19.203","app":0}'
    riskForm = baseenco(userinfo)
    return riskForm


def runUa():
    phoneModel = generate_random_str(5) + " " + generate_random_str(3)
    adVersion = str(random.randint(4, 13))
    return 'Mozilla/5.0 (Linux; Android ' + adVersion + '; ' + phoneModel + ' Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36 TitansX/20.11.7 KNB/1.2.0 android/' + adVersion + ' mt/com.sankuai.meituan/11.19.203 App/10120/11.19.203 MeituanGroup/11.19.203'


def execCkDatas(path):
    with open(path, 'r', encoding='utf-8') as f:
        cks = f.read()
    ckDatas = cks.split('\n')
    oks = []
    for ck in ckDatas:
        if ck != '' and 'userId' in ck:
            oks.append(ck)
    return oks


def getCkExec(ck):
    userId = getMiddleStr(ck, "userId=", ";")
    uuid = getMiddleStr(ck, "uuid=", ";")
    mini_program_token = getMiddleStr(ck, "token=", ";")
    return userId, uuid, mini_program_token


def getHead(ck):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": ck,
        'User-agent': runUa(),
        'mtoken': mini_program_token,
        'actoken': getAccessToken(ck)[0]
    }
    return head

def checkCkStatus(ck):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://gz.meituan.com/",
        "Cookie": f'lt={mini_program_token}',
        'User-agent': runUa()
    }
    res = requests.get(
        f'https://gz.meituan.com/ptapi/getLoginedUserInfo?timestamp={getTimestamp()}',
        headers=head, timeout=5)
    js = json.loads(res.text)
    if js.__contains__('error'):
        return False
    return True
def getAccessToken(ck):
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": ck,
        'User-agent': runUa()
    }
    userId, uuid, mini_program_token = getCkExec(ck)
    res = requests.get(
        f'https://game.meituan.com/mgc/gamecenter/skuExchange/login?gameType=10139&mtUserId={userId}&mtToken={mini_program_token}&mtDeviceId={uuid}&nonceStr={generate_random_str(16)}&externalStr=%7B%22cityId%22:%2220%22%7D',
        headers=head, timeout=5)
    js = json.loads(res.text)
    # printf(f'获取token[{userId}]{js}')
    if 'token不合法' in res.text or 'accessToken' not in res.text:
        return "", ""
    return js['data']['accessToken'], js['data']['mgcPlayerInfo']['gameNickName']


def getTuanBiBlance(signal, cks):
    dats = []
    for ck in cks:
        token, name = getAccessToken(ck)
        if token == "":
            continue
        res = requests.get(
            f'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=2&gameId=10139',
            headers=getHead(ck),
            timeout=5)
        if '失效' in res.text:
            continue
        js = json.loads(res.text)
        dats.append({
            "name": name,
            "blance": js['data'][0]['resourceName'] + js['data'][0]['count'] + js['data'][0]['resourceUnit'],
            "ck": ck
        })
    signal.emit(dats)


def getAddressList(signal, ck):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa()
    }
    ployd = {
        "data": '{"address_type": 2}',
        "login_token": mini_program_token,
        "login_token_type": 0
    }
    res = requests.post(
        f'https://addressapi.meituan.com/v1/address/list?actual_latitude=0&actual_longitude=0&address_sdk_type=h5&address_sdk_version=1.4.18&biz_id=1135&client_id=6&client_version=12.6.203&device_type=h5&device_version=1.4.18&latitude=0&longitude=0&uuid={uuid}',
        headers=head,
        data=ployd,
        timeout=5)
    js = json.loads(res.text)
    if js['code'] == 0:
        signal.emit(js['data']['address_list'])
    else:
        return signal.emit([])


def delAddress(ck, address_view_id):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa()
    }
    ployd = {
        "data": '{"address_view_id": ' + address_view_id + '}',
        "login_token": mini_program_token,
        "login_token_type": 0
    }
    res = requests.post(
        f'https://addressapi.meituan.com/v1/address/delete?actual_latitude=0&actual_longitude=0&address_sdk_type=h5&address_sdk_version=1.4.18&biz_id=1135&client_id=6&client_version=12.6.203&device_type=h5&device_version=1.4.18&latitude=0&longitude=0&uuid={uuid}',
        headers=head,
        data=ployd,
        timeout=5)
    js = json.loads(res.text)
    printf(js)


def searchAddress(ck, city, keyword):
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa()
    }
    res = requests.get(
        f'https://maf.meituan.com/search?city={quote(city)}&citylimit=true&key=b953f132-26e8-4576-8d1e-017acf3cf676&keyword={quote(keyword)}&location=113.272821%2C23.086925&orderby=DISTANCE&page=0&pagesize=20&radius=1000&region=CITY&scenario=GENERAL',
        headers=head,
        timeout=5)
    js = json.loads(res.text)
    if js['status'] == 200:
        return js['result']['pois']
    else:
        return []


def addAddress(ck, searchData, name, phone, detailedAddress):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa()
    }
    address_admin_list = []
    for it in searchData['addr_info']:
        admin_level = it['admin_level']
        admin_code = it['admin_code']
        mname = it['name']
        level_desc = it['level_desc']
        data = {
            "code": admin_code,
            "name": mname,
            "level_info": {
                "level": admin_level,
                "desc": level_desc
            }
        }
        address_admin_list.append(data)

    location = searchData['location']
    locations = location.split(',')
    latitude = locations[1].replace('.', '')
    longitude = locations[0].replace('.', '')
    source = {
        "recipient_name": name,
        "address_name": searchData['name'],
        "phone": phone,
        "gender": 1,
        "latitude": latitude,
        "longitude": longitude,
        "address_source": 12,
        "address_admin_list": address_admin_list,
        "house_number": detailedAddress,
        "tag_id": 2,
        "address_location": searchData['address'],
        "user_confirmed": False,
        "force_return_success": True,
        "extra": ""
    }

    ployd = {
        "data": json.dumps(source),
        "login_token": mini_program_token,
        "login_token_type": 0
    }
    res = requests.post(
        f'https://addressapi.meituan.com/v1/address/save?actual_latitude=0&actual_longitude=0&address_sdk_type=h5&address_sdk_version=1.4.18&biz_id=1135&client_id=6&client_version=12.6.203&device_type=h5&device_version=1.4.18&latitude=0&longitude=0&uuid={uuid}',
        headers=head,
        data=ployd,
        timeout=5)
    js = json.loads(res.text)
    printf(js)


def getProducts(signal, ck):
    res = requests.get(
        f'https://game.meituan.com/mgc/gamecenter/skuExchange/skus?sceneId=2&gameId=10139&cityIds=20&tabIds=7',
        headers=getHead(ck),
        timeout=5)
    js = json.loads(res.text)
    if js['code'] == 0:
        return signal.emit(js['data'][0]['dataList'])
    else:
        return signal.emit([])

def getImg(signal, datas):
    res = requests.get(url=datas['imgUrl'])
    datas['img'] = res.content
    return signal.emit(datas)

def submitOrderV2(ck, addressData, productData):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = getHead(ck)

    phone = addressData['phone']
    latitude = addressData['latitude']
    longitude = addressData['longitude']
    address_name = addressData['address_name']
    house_number = addressData['house_number']
    recipient_name = addressData['recipient_name']

    addressStr = ''
    for it in addressData['address_admin_list']:
        actName = it['name']
        addressStr = addressStr + actName + ','
    addressStr = addressStr + address_name + house_number

    lvyueGoodsId = 0
    for key in productData.keys():
        item = productData[key]
        goodsIds = item['10031']
        lvyueGoodsId = json.loads(goodsIds)['lvyueGoodsId']


    ployd = {
        "accessToken": head['actoken'],
        "recipientName": recipient_name, "recipientPhone": phone,
        "recipientAddress": addressStr,
        "deviceUuid": uuid, "clientType": 6,
        "appVersion": "12.6.203", "actLongitude": longitude, "actLatitude": latitude, "gameId": "10139",
        "goodsId": lvyueGoodsId, "bizParams": "{}", "goodsImgUrl": "", "remark": "",
        "fingerprint": getRiskFrom(userId, uuid, mini_program_token, ck),
        "channelId": 1}

    res = requests.post(
        f'https://guoyuan.meituan.com/api/order/submitOrderV2',
        headers=head,
        json=ployd,
        timeout=5)
    js = json.loads(res.text)
    printf(js)
    if js['code'] == 200:
        return True, js['outNo']
    else:
        return False, None

def getOrderList(ck):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa(),
        'token': mini_program_token
    }
    res = requests.get(
        f'https://guoyuan.meituan.com/api/order/listByGameType?gameType=10139&pageSize=999',
        headers=head,
        timeout=5)
    js = json.loads(res.text)
    if 'orderList' in res.text:
        if js['orderList'] == None:
            return []
        return js['orderList']
    else:
        return []

def getOrderDetaild(ck, ordNo):
    userId, uuid, mini_program_token = getCkExec(ck)
    head = {
        "Referer": "https://cube.meituan.com/cube/block/4d6b88d1167c/163282/index.html",
        "Cookie": ck,
        'User-agent': runUa(),
        'token': mini_program_token
    }
    res = requests.get(
        f'https://guoyuan.meituan.com/api/order/detail2/{str(ordNo)}?gameType=1',
        headers=head,
        timeout=5)
    js = json.loads(res.text)
    return js
