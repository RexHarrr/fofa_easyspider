import base64
import time

from bs4 import BeautifulSoup  #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定URL，获取网页数据
import xlwt     #进行excel操作


#查询页数（创建正则表达式，表示规则）
findPage = re.compile(r'<span class="el-pagination__total">共(.*)条</span>')
def main(key):
    # baseurl = f"https://fofa.info/result?qbase64={key}&page={pagenum}&page_size=10"
    #爬取网页
    datalist = GetData(key)

    #保存数据
    savepath = "H:\pycharm\Projects\FofaSpider\Fofa爬取.xls"
    saveData(datalist,savepath)

def GetPageNum(key):#获取总页数
    baseurl=f"https://fofa.info/result?qbase64={key}&page=1&page_size=10"
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('span', class_="el-pagination__total"):
        item = str(item)
        Num = re.findall(findPage, item)[0]  # re库通过正则表达式查找指定的字符串
    PageNum = int(Num) //10
    if not PageNum%10 :
        PageNum=PageNum+1

    return PageNum

# findcount = re.compile(r'<div>(.*)</div>')
findurl = re.compile(r'<a href="(.*?)" target="_blank">')
#获取目标信息
def GetData(key):
    datalist = []
    PageNum = GetPageNum(key)
    print("共有%d页内容" %PageNum)
    a = input("从第几页开始爬取：")
    a = int(a)
    b = input("到第几页结束爬取：")
    b = int(b)
    for i in range(a,b+1):  # 调用获取页面信息
        url = f"https://fofa.info/result?qbase64={key}&page={i}&page_size=10"
        # print(url)
        html = askURL(url)  # 保存获取到的网页源码

            # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")

        item = soup.find_all('a',{'target':"_blank"})

        item = str(item)

        sitem = item.split(",")
        for things in sitem:

            result = re.findall(findurl,things)
            datalist.append(result)
        # time.sleep(5)

    print(datalist)
    return datalist



#得到指定一个URL的网页内容
#换成自己的UA头和Cookie
def askURL(url):
    head = {           #模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Cookie": "__fcd=0QrId1OEadKRUaxAF4wiAxX7; _ga=GA1.1.2060238411.1671880931; is_flag_login=0; isRedirect=1; Hm_lvt_19b7bde5627f2f57f67dfb76eedcf989=1672216174,1672294654,1672906412,1672974322; baseShowChange=false; viewOneHundredData=false; befor_router=%2Fresult%3Fqbase64%3DYXBwPSJEb2NjbXMi; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MjA5MjAyLCJtaWQiOjEwMDEyMDUyOCwidXNlcm5hbWUiOiJSZXhIYSIsImV4cCI6MTY3MzIzMzY4N30.0EqQhTq5AbXb0GvFlrx5JehnT9euKJa-LFq4B7XGg1jkn9D7MjNoJJROCTG_4dqA3ApsxZ2CMkE8MCkmdtxBmw; user=%7B%22id%22%3A209202%2C%22mid%22%3A100120528%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22RexHa%22%2C%22nickname%22%3A%22RexHa%22%2C%22email%22%3A%222226836027%40qq.com%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTJPs1AK7yEmictbzC97iaNSvZa4ZxetjFgWpdXxpPCIXgEhZAia83mVYtDx4RZslgGiaZCAsXNSrR1ic9g%2F132%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTJPs1AK7yEmictbzC97iaNSvZa4ZxetjFgWpdXxpPCIXgEhZAia83mVYtDx4RZslgGiaZCAsXNSrR1ic9g%2F132%22%2C%22key%22%3A%22f2dd380503a0a00b87c270aa69004578%22%2C%22rank_name%22%3A%22%E6%B3%A8%E5%86%8C%E7%94%A8%E6%88%B7%22%2C%22rank_level%22%3A0%2C%22company_name%22%3A%22RexHa%22%2C%22coins%22%3A0%2C%22can_pay_coins%22%3A0%2C%22credits%22%3A1%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A0%7D; Hm_lpvt_19b7bde5627f2f57f67dfb76eedcf989=1672987205; _ga_9GWBD260K9=GS1.1.1672986558.13.1.1672987210.0.0.0"

    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:     #异常处理
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

#保存数据至xls
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('Fofa爬取',cell_overwrite_ok=True)
    col = ("id","url")#定义字段名
    for i in range(0,2):
        sheet.write(0,i,col[i]) #列名
    for i in range(len(datalist)):
        print("第%d条"%(i+1))
        data = datalist[i]
        print(data)
        sheet.write(i + 1, 0, i+1)
        sheet.write(i+1,1,data)  #数据

    book.save(savepath) #保存

if __name__=="__main__":  #当程序执行时
    # main()
    INPUT = input("请输入需要查询的语法：")
    key = str(base64.b64encode(INPUT.encode("utf-8")), "utf-8")
    main(key)
    print("爬取完毕！")