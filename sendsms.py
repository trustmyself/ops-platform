# -*- coding: utf-8 -*-

import sys
import requests


def send_sms(tel,subject,content,user,passwd):
    sign = '[新美互通]'
    allinfo = '['+subject+']'+'\n\r'+content+'\n\r'+sign
    if len(allinfo)>150:
        allinfo=allinfo[0:150]
    allinfo = allinfo.encode('GBK')
    bodyValue = {"OperID": user, "OperPass": passwd, "DesMobile": tel, "Content": allinfo}
    url = 'http://qxtsms.guodulink.net:8000/QxtSms/QxtFirewall'
    with requests.Session() as s:
        return s.get(url, params=bodyValue)


if __name__ == "__main__":
    phone = sys.argv[1]
    subjectname = sys.argv[2]
    contents = sys.argv[3]
    username = 'xmht'
    password = 'J8ghOP'
    send_sms(phone,subjectname,contents,username,password)

