#encoding: GBK
"""
@project = zentao
@file = bug_statistics
@function = bug统计(接口方式)
@author = Cindy
@create_time = 2018/5/16 11:07
"""

import requests, os
from html.parser import HTMLParser

# 获取禅道bug页面
url = 'http://192.168.2.203/zentao/www/index.php?m=bug&f=browse&root=43&type=byModule&param=2448'
headers = {'Cookie': 'za=daixin; zp=6fe3e7d73ebc99a48c4b4bfd94891bbeb0499aee; sid=d43amsi0mvhrr5bu3f0jg43ur5'}
# headers = {'Host': '192.168.2.203',
#         'Upgrade-Insecure-Requests': '1',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Referer': 'http://192.168.2.203/zentao/www/index.php?m=user&f=login',
#         'Accept-Encoding': 'gzip, deflate, sdch',
#         'Accept-Language': 'zh-CN,zh;q=0.8',
#         'Cookie': 'checkedItem=; productStoryOrder=id_desc; productPlanOrder=end_asc; fbBugOrder=id_desc; fbStoryOrder=id_desc; projectStoryOrder=title_asc; projectTaskOrder=assignedTo_asc; projectTree=hide; lastProject=328; lastProduct=43; qaBugOrder=id_desc; lang=zh-cn; theme=default; keepLogin=on; za=daixin; zp=6fe3e7d73ebc99a48c4b4bfd94891bbeb0499aee; zt_ptcp=1; zt_ptkcx=1; zt_ptfcx=1; zt_ptcs=1; zt_ptother=1; zt_pt542=tg7679%3D0%2Ctg7691%3D0%2Ctg7696%3D0%2Ctg7953%3D0; zt_pt604=tg7626%3D0%2Ctg7627%3D0%2Ctg7628%3D0%2Ctg7629%3D0%2Ctg7630%3D0%2Ctg7631%3D0%2Ctg7632%3D0%2Ctg7633%3D0%2Ctg7634%3D0%2Ctg7635%3D0%2Ctg7636%3D0%2Ctg7667%3D0%2Ctg7675%3D0; zt_pt608=tg7670%3D0%2Ctg7671%3D0%2Ctg7672%3D0; zt_ps623=st7977%3D0%2Cst7782%3D0%2Cst7795%3D0%2Cst7796%3D0%2Cst7646%3D0; zt_pt623=tg7658%3D0%2Ctg7556%3D0%2Ctg7647%3D0%2Ctg7388%3D0%2Ctg7393%3D0%2Ctg7605%3D1%2Ctg7606%3D0%2Ctg7607%3D0%2Ctg7609%3D0%2Ctg7611%3D0%2Ctg7613%3D0%2Ctg7638%3D0%2Ctg7640%3D0%2Ctg7650%3D0%2Ctg7686%3D0%2Ctg7846%3D0%2Ctg7848%3D0%2Ctg7869%3D0; zt_pt563=tg7825%3D0%2Ctg7917%3D0%2Ctg7924%3D0%2Ctg7604%3D0%2Ctg7608%3D0%2Ctg7615%3D0%2Ctg7616%3D0%2Ctg7617%3D0%2Ctg7618%3D0%2Ctg7639%3D0%2Ctg7641%3D0%2Ctg7694%3D0%2Ctg7701%3D0%2Ctg7704%3D0%2Ctg7751%3D0%2Ctg7754%3D0%2Ctg7757%3D0%2Ctg7761%3D0%2Ctg7764%3D0%2Ctg7765%3D0%2Ctg7767%3D0%2Ctg7773%3D0%2Ctg7778%3D0%2Ctg7779%3D0%2Ctg7780%3D0%2Ctg7781%3D0%2Ctg7784%3D0%2Ctg7786%3D0%2Ctg7787%3D0%2Ctg7788%3D0%2Ctg7789%3D0%2Ctg7792%3D0%2Ctg7797%3D0%2Ctg7798%3D0%2Ctg7814%3D0%2Ctg7842%3D0%2Ctg7861%3D0%2Ctg7862%3D0%2Ctg7866%3D0%2Ctg7868%3D0%2Ctg7870%3D0%2Ctg7884%3D0%2Ctg7910%3D0%2Ctg7911%3D0%2Ctg7913%3D0%2Ctg7914%3D0%2Ctg7915%3D0; zt_plan_item=doing_pds_nowSeason; product=plan; zt_ps632=st7919%3D0; zt_pt632=tg7922%3D1; treeview=100; zt_pt523=tg7136%3D0%2Ctg7182%3D0%2Ctg7256%3D0%2Ctg7259%3D0%2Ctg7093%3D0%2Ctg7094%3D0%2Ctg7130%3D0%2Ctg7230%3D0%2Ctg7248%3D0%2Ctg7443%3D0%2Ctg7465%3D0%2Ctg7466%3D0%2Ctg7961%3D0; zt_pt328=tg5159%3D0%2Ctg6110%3D0%2Ctg6111%3D0%2Ctg6132%3D0%2Ctg6157%3D0%2Ctg7349%3D0%2Ctg7677%3D0%2Ctg6792%3D0%2Ctg4735%3D0%2Ctg4736%3D0%2Ctg4737%3D0%2Ctg4738%3D0%2Ctg4739%3D0%2Ctg4741%3D0%2Ctg4742%3D0%2Ctg4744%3D0%2Ctg4745%3D0%2Ctg4750%3D0%2Ctg4754%3D0%2Ctg4755%3D0%2Ctg4756%3D0%2Ctg4757%3D0%2Ctg4758%3D0%2Ctg5567%3D0%2Ctg5728%3D0%2Ctg5986%3D0%2Ctg6219%3D0%2Ctg6223%3D0%2Ctg6238%3D0%2Ctg6240%3D0%2Ctg6322%3D0%2Ctg6821%3D0%2Ctg6861%3D0%2Ctg6862%3D0%2Ctg6898%3D0%2Ctg6899%3D0%2Ctg6900%3D0%2Ctg6901%3D0%2Ctg6902%3D0%2Ctg6903%3D0%2Ctg6909%3D0%2Ctg6914%3D0%2Ctg5646%3D0%2Ctg6248%3D0%2Ctg6312%3D0%2Ctg6907%3D0%2Ctg7235%3D0%2Ctg7325%3D0%2Ctg7365%3D0; zt_ps615=st8060%3D0%2Cst7901%3D0; downloading=1; projectTree=hide; zt_pt615=tg7872%3D0%2Ctg7885%3D0%2Ctg7962%3D0%2Ctg7699%3D0%2Ctg7700%3D0%2Ctg7879%3D0%2Ctg7880%3D0%2Ctg7881%3D0%2Ctg7938%3D0%2Ctg7941%3D0%2Ctg7942%3D0%2Ctg7943%3D0%2Ctg7944%3D0%2Ctg7945%3D0%2Ctg7747%3D0%2Ctg7976%3D0; project=plan; qa=bug; windowWidth=1920; windowHeight=944; sid=d43amsi0mvhrr5bu3f0jg43ur5'
#         }

res = requests.get(url,headers=headers)
page = res.text.encode(res.encoding).decode('utf-8')
# print(page)

# 获取bug列表部分内容
begin = page.find('<tbody>')
end = page.find('</tbody>')
html = page[begin:end].strip()
# print(html)


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        pass
        # print("start tag:", tag)

    def handle_endtag(self, tag):
        pass
        # print("end tag :", tag)

    def handle_data(self, data):
        data = data.strip()
        if data != '':
            # print("data  :", data)
            with open('bug.txt','a',encoding='utf-8') as f:
                f.write(data + '\n')

os.remove('bug.txt')
parser = MyHTMLParser()
parser.feed(html)

with open('bug.txt','r',encoding='utf-8') as f:
    list = []
    for line in f.readlines():
        list.append(line.strip())
    # print(list)

#拆分列表：每个bug字段数不一样，但是都有[已确认]或[未确认]字段，此字段为第4个字段
list.reverse()
# print(list)
lists = []
while list != []:
    for i in list:
        if i.isdigit():
            if int(i) > 1000:
                f = list.index(i)
                print(i)
                lists.append(list[:f + 1])
                list = list[f + 1:]


for j in lists:
    print(j)
