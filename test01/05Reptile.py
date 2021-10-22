# 爬虫
"""
urlopen中的方法
geturl()：返回url，用于看是否有重定向
info()：返回元信息，例如HTTP的headers
getcode()：返回回复的HTTP状态码，可以用来检查代理IP的可使用性
error类
URLError类：是OSError的子类，继承OSError，没有自己的任何行为特点，使用URLError类的对象时，可以查看错误的reason
HTTPError类：是URLError的子类，当HTTP发生错误将举出HTTPError，使用HTTPError类的对象时，可以查看状态码，headers等
"""
# 简单练习
# import urllib.request
# import urllib.error
# if __name__ == '__main__':
#     try:
#         headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu;Linux x86_64;rv: 57.0) Gecko / 20100101Firefox / 57.0'}
#         response = urllib.request.Request('http://python.org/', headers=headers)
#         html = urllib.request.urlopen(response)
#         result = html.read().decode('utf-8')
#     except urllib.error.URLError as e:
#         if hasattr(e, 'reason'):
#             print('错误原因是' + str(e.reason))
#     except urllib.error.HTTPError as e:
#         if hasattr(e, 'code'):
#             print('错误状态码是' + str(e.code))
#     else:
#         print('请求成功通过。')

# 豆瓣读书练手爬虫
import requests
from bs4 import BeautifulSoup


# 发出请求获得HTML源码的函数
def get_html(url):
    # 伪装成浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36'} 
    resp = requests.get(url, headers=headers).text

    return resp


# 解析页面，获得数据信息
def html_parse():
    # 调用函数，for循环迭代出所有页面
    for url in all_page():
        # BeautifulSoup的解析
        soup = BeautifulSoup(get_html(url), 'lxml')
        # 书名
        allDiv = soup.find_all('div', class_='pl2')
        names = [a.find('a')['title'] for a in allDiv]
        # 作者
        allP = soup.find_all('p', class_='pl')
        authors = [p.get_text() for p in allP]
        # 评分
        starSpan = soup.find_all('span', class_='rating_nums')
        scores = [s.get_text() for s in starSpan]
        # 多少人评价
        RenSpan = soup.find_all('span', class_='pl')
        nums = [r.get_text() for r in RenSpan]
        # print(nums)  # (\n                    15421人评价\n                )
        # 简介
        describesSpan = soup.find_all('span', class_='inq')
        describes = [i.get_text() for i in describesSpan]
        for name, author, score, num, describe in zip(names, authors, scores, nums, describes):
            name = '书名：' + str(name) + '\n'
            author = '作者：' + str(author) + '\n'
            aa = str(num).splitlines()
            # 取数据，例如'  23445人评价'，并去除前面包含的空格和'评价'这两个字符
            bb = aa[1].strip(' \t\n\r').replace('评价', '')
            # print(aa)
            score = '评分：' + str(score) + '\n'
            ss = '评价人数：' + str(bb) + '\n'
            describe = '简介：' + str(describe) + '\n'
            data = name + author + score + ss + describe
            # 保存数据
            f.writelines(data + '=====================================' + '\n')


# 获得所有页面的函数
def all_page():
    base_url = 'https://book.douban.com/top250?start='
    urlList = []
    # 从0到225，间隔25的数组
    for page in range(0, 250, 25):
        allUrl = base_url + str(page)
        urlList.append(allUrl)

    return urlList


if __name__ == '__main__':
    # 文件名
    filename = '豆瓣图书Top250.txt'
    # 保存文件操作
    f = open(filename, 'w', encoding='utf-8')
    # 调用函数
    html_parse()
    f.close()
    print("保存成功")
