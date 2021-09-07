# -*- coding:utf-8 -*-
import re
import io
import os
import json
import requests
import time
import traceback
base_url = 'https://webcache.googleusercontent.com/search?q=cache:https://mohu.rocks/'
base_url2 = 'https://webcache.googleusercontent.com/search?q=cache:https://www.mohu.rocks/'
headers = {
    'User-Agent' : 'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0', # Tor browser
    'Referrer' : 'https://google.com'
}
data={}
proxies = {
    'https' : '127.0.0.1:9910'
}
startpage = 6200
endpage = 6214
for page in range(startpage,endpage):
    time.sleep(5)
    try:
        if not os.path.exists('article/'+str(page)+'.json'):
            req = requests.get(base_url + 'article/' + str(page), headers = headers, proxies = proxies)
            webpage = req.text
            title = re.findall(r'<title>(.*?)</title>',webpage)
            title = ''.join(title)
            uid = re.findall('data-id="\d{1,4}"',webpage)[-1]
            uid = re.findall('\d+', uid)
            uid = "".join(uid)
            uid = int(uid)
            contents = re.findall(r'<div class="content markitup-box">([\s\S]*?)</div>', webpage)
            contents = "".join(contents)
            contents = contents.strip()
            topics = re.findall(r'class="topic-tag" data-id="(.*?)">',webpage)
            topics = [int(i) for i in topics]
            date = re.findall(r'[\d]{4}-[\d]{2}-[\d]{2}',webpage)[0]
            agreeCount = re.findall(r'<b class="count">(.*?)</b>',webpage)[0]
            agreeCount = int(agreeCount)
            discussionCount = re.findall(r'<h2>\d+.[\u4e00-\u9fa5]{3}</h2>',webpage)
            discussionCount = "".join(discussionCount)
            discussionCount = discussionCount[4:discussionCount.index(" ")]
            discussionCount = int(discussionCount)
            data['type'] = "article"
            data['id'] = page
            data['title'] = title
            data['uid'] = uid
            data['topics'] = topics
            data['contents'] = contents
            data['date'] = date
            data['agreeCount'] = agreeCount
            data['discussionCount'] = discussionCount
            jsonString = json.dumps(data,ensure_ascii=False)
            with io.open('article/'+str(page)+'.json',"w",encoding="utf-8") as f:
                f.write(jsonString)
    except Exception as HTTPError:
        traceback.print_exc()
