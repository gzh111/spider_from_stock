import urllib.request as ur
import re
import socket
import pandas as pd
import os
def getHtml(url):
    html = ur.urlopen(url).read()
    html = html.decode('utf-8')
    return html

def getStackCode(html):
    s = r'<a href="https://hq.gucheng.com/[\S]+\(([0-9]+)\)</a>'
    pat = re.compile(s)
    code = pat.findall(html)
    return code

socket.setdefaulttimeout(30)
Url = 'https://hq.gucheng.com/gpdmylb.html'#东方财富网股票数据连接地址
filepath = r'D:\Desktop\卓识投资\data\ '#定义数据文件保存路径
#实施抓取
code = getStackCode(getHtml(Url))
print(code)
#获取所有沪市股票代码（如果想获得全部将item[0]的判断去掉即可）
CodeList = []
for item in code:
    if item[0]=='6':
        CodeList.append(item)
#抓取数据并保存到本地csv文件
for code in CodeList:
    print('正在获取股票%s数据'%code)
    url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
          '&end=20201129&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    try:
        ur.urlretrieve(url, filepath+code+'.csv')
    except socket.timeout:
        count = 1
        while count <= 5: # 对访问超时的网站尝试访问5次
            try:
                try: #防止出现由于网站不存在或者访问限制而产生的直接返回
                    ur.urlretrieve(url, filepath+code+'.csv')
                finally:
                    break
            except socket.timeout:
                err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                print(err_info)
                count += 1
        if count > 5:
            print("Download job failed!")
