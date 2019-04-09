import requests

proxy = {"http": "http://127.0.0.1:3128"}
r = requests.get("http://www.baidu.com", proxies=proxy);
# setting response encoding
r.encoding = 'utf-8'
# print(r)
# print(r.text)


from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "lxml")
# 格式化输出
# print(soup.prettify())
# 打印head信息
# print(soup.head)
# 通过find all查询，支持正则，名称
# print(soup.find_all("div", id="ftCon"))
# 通过选择器查询
# print(soup.select('#lh'))


import re

# match 和 search 区别
# res = r'<a (.*?)>(.*?)</a>'
# findVal =  re.findall(res,r.text,re.I | re.S | re.M)
# for content in findVal:
#     print(content)


# 登录网站
session = requests.session()
# userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
# header = {
#     "Referer": "http://10.249.8.118:8080/queue-web/QueryJobList.do?menuId=joblist",
#     'User-Agent': userAgent
# }

loginUrl = 'http://10.249.8.118:8080/queue-web/ldapAuthServlet.do'
postData = {
    'j_username': 'y00295039',
    'j_password': 'feiye_678',
    'redirectURL': 'http://10.249.8.118:8080/queue-web/QueryJobList.do?menuId=joblist',
    'uid': '',
    'logout': None,
    'loginError': None
}


def login(url, data, proxy):
    r = session.post(url, data=data, proxies=proxy, timeout=30)
    print(r.status_code)
    if r.status_code == 200:
        return True
    else:
        return False


def getHtml(url):
    try:
        r = session.get(url)
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "


def handleData(needLogin,url):
    if needLogin:
        if not login(loginUrl, postData, proxy):
            return
    data = getHtml(url)
    # print(data)
    soup = BeautifulSoup(data, "lxml")
    #这里也可以用find_all方法来查询相应节点
    joblist =  soup.select('#sessionScope.jobDatas tbody tr')
    # print(joblist)
    jobs =  []


    '''
        tr content is :
        <tr class="odd">
            <td>1300041032</td>
            <td title="lwx300030,qwx504158">lwx300030,...</td>
            <td>cloudccp_cloudccp</td>
            <td>Create from ICP-CI.</td>
            <td><font color="#999999"><strong>Completed</strong></font></td>
            <td>Execute 5 minutes</td>
            <td>2019-03-27 18:45:23</td>
            <td>2019-03-27 18:50:50</td>
            <td><input id="jobDetail1300041032" type="hidden" value=""/><a href="javascript:alertDetail('jobDetail1300041032');">Detail</a> | <a href="/queue-web/RestartJob.do?jobId=1300041032&amp;cause=Jobisresetbyadmin" target="_parent">Reset
            Job</a> | <a href="javascript:download('1300041032_e8f904cf-c986-447f-bb8d-e16f71f748e5_log');">Log</a></td>
        </tr>
    '''  

    for tr in joblist:
        job =  {}
        try:
            # 这里如果使用contents[0]获取，下标不太好确定，因为contents数组中有'\r\n'
            job['Task No.']= tr.find_all('td')[0].string
            job['Project Name']=tr.find_all('td')[2].string
            job['Status']=tr.find_all('td')[4].find('strong').string
            job['Time']=tr.find_all('td')[5].string
            jobs.append(job)
        except Exception as error:
            print(error)
    
    return jobs

def writeToFile(list):
    with open('jobs.txt','w') as f:
        for i in list:
            f.write('Task No. {} \t Project Name: {} \t Status: {} \t Time: {} \n'.format(i['Task No.'],i['Project Name'],i['Status'],i['Time']))

if __name__ == '__main__':
    url = 'http://10.249.8.118:8080/queue-web/QueryJobList.do?menuId=joblist'
    writeToFile(handleData(True,url))
    # handleData()
