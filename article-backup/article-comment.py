# -*- coding:utf-8 -*-
import re
import io
import os
import json
import time
import requests
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
startpage=6170
endpage=6200
for page in range(startpage,endpage):
    time.sleep(10)
    try:
        
        req = requests.get(base_url + 'article/' + str(page), headers = headers, proxies = proxies)

        webpage=req.text
        comment=re.findall(r'<div class="mod-body aw-feed-list aw-replies">([\s\S]*?)<div class="mod-body aw-feed-list aw-replies-fold">',webpage)
        comment="".join(comment).strip()
        total_discussion=comment.count('markitup-box')
        data_item_id=re.findall(r'data-item-id="\d+"',comment)
        data_item_id=[re.findall(r'\d+',i) for i in data_item_id]

        agree_count=re.findall(r'<b class="count">\d+</b>',comment)
        agree_count=[re.findall(r'\d+',i) for i in agree_count]
        date=re.findall(r'[\d]{4}-[\d]{2}-[\d]{2}',comment)
        user_id=re.findall(r'<a class="aw-user-name" data-id="\d+" data-reputation',comment)
        user_id=[re.findall(r'\d+',i) for i in user_id]
        contents=re.findall(r'<div class="markitup-box">([\s\S]*?)</div>',comment)
        contents=[i.strip() for i in contents]
        for i in range(total_discussion):
            data['type']="article_comment"
            tmp_id="".join(data_item_id[i])
            data['id']=int(tmp_id)
            data['parentType']="article"
            data['parentId']=page
            data['uid']=int("".join(user_id[i]))
            data['contents']=contents[i]
            data['date']=date[i]
            data['agreeCount']=int("".join(agree_count[i]))
            data['discussionCount']=0
            jsonString = json.dumps(data,ensure_ascii=False)
            with io.open('article-comment/'+tmp_id+'.json',"w",encoding="utf-8") as f:
                f.write(jsonString)
                f.close()
    except Exception as HTTPError:
        traceback.print_exc()
