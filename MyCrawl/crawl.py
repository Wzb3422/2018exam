import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify

r1 = requests.get('https://blog.snowstar.org', timeout = 30)
r1.encoding = r1.apparent_encoding
soup = BeautifulSoup(r1.text, "html.parser")
title_list = []
for h2 in soup.find_all(class_="entry-title"):
    title = h2("a")
    title_list.append(title[0].string)
#已经获取所有标题 以列表形式保存

postTime_list = []
for span in soup.find_all(class_="posted-date"):
    postTime_list.append(span.string)
#已经获取所有提交时间 以列表形式保存

summary_list = []
pTags_list =[]
for div in soup.find_all(class_="entry-summary"):
    pTags_list = div("p")
    summary_list.append(pTags_list[0].string)
#已经获取所有文章概述 以列表形式保存

# https://snowstar.org/?s=搜索的url
# 下面是搜索的请求以及解析 代码复用性不高...

app = Flask(__name__)

@app.route("/show")
def showTitle():
    return jsonify({
        "title": title_list,
        "time": postTime_list,
        "summary": summary_list
    })
#这里输出的是JSON列表 前端收到后需要循环按顺序输出
@app.route("/search")
def search():
    keyword = request.json.get("keyword")
    url = 'https://snowstar.org/?'
    kv = {'s': keyword}#这里的keyword搜索关键字需要输入
    r2 = requests.get(url, params = kv)
    r2.encoding = r2.apparent_encoding
    soup2 = BeautifulSoup(r2.text, "html.parser")

    for h2 in soup.find_all(class_="entry-title"):
        title2 = h2("a")
        title_list2.append(title2[0].string)
    #已经获取所有标题 以列表形式保存

    postTime_list2 = []
    for span in soup.find_all(class_="posted-date"):
        postTime_list2.append(span.string)
    #已经获取所有提交时间 以列表形式保存

    summary_list2 = []
    pTags_list2 =[]
    for div in soup.find_all(class_="entry-summary"):
        pTags_list2 = div("p")
        summary_list2.append(pTags_list2[0].string)
        #已经获取所有文章概述 以列表形式保存
    return jsonify({
        "title": title_list2,
        "time":postTime_list2,
        "summary":summary_list2
    })
#这里输出的是JSON列表 前端收到后需要循环按顺序输出

if __name__ == '__main__':
    app.run()