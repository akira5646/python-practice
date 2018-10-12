import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import xlsxwriter
import json
import math
import configparser
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

config=configparser.ConfigParser()
config.read('D:\py\weibo_account.ini','utf-8-sig')
oid = config['weibo']['oid']
containerid = config['weibo']['containerid']

host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'

headers = {
    'Host': host,
    'Referer': f'https://m.weibo.cn/u/{oid}',
    'User-Agent': user_agent
}


# 按页数抓取数据
def get_single_page(page):
    params = {
        'type': 'uid',
        'value': oid,
        'containerid': containerid,
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)


# 解析页面返回的json数据
def parse_page(json):
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        if item:
            data = {
                'id': item.get('id'),
                'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
                'attitudes': item.get('attitudes_count'),# 点赞数
                'comments': item.get('comments_count'),# 评论数
                'reposts': item.get('reposts_count'), # 转发数
                'rtime' : item.get('created_at'), # 发布时间
            }
            yield data

# 将微博信息写入excel表
def write_weibo_info(weibos):
    workbook = xlsxwriter.Workbook(f"D:\Github\python-practice\selenium练习\output\weibo_list_{oid}.xlsx")
    worksheet = workbook.add_worksheet()
    title_format = workbook.add_format(
        {'bold': True}
    ) 
    #写入标题
    row0 = list(weibos[0].keys())
    for i in range(0,len(row0)):
        worksheet.write(0,i,row0[i],title_format)
    #写入数据
    for i in range(1,len(weibos)+1):
        if(i%10==0):
            print("正在写入第",i,"条微博")
        for j in range(0,len(row0)):
            worksheet.write(i,j,str(weibos[i-1][row0[j]]))
    print("complete")
    workbook.close()

def get_weibos_by_page(page):
    print(f"正在获取第{page}页微博")
    return parse_page(get_single_page(page))

if __name__ == '__main__':
    # 抓取第一页的同时获取微博总数
    weibo = get_single_page(1)
    # total = weibo.get('data').get('cardlistInfo').get('total')
    total = weibo.get('data').get('cardlistInfo').get('total')
    results_page1 = parse_page(weibo)
    # 多线程返回有序结果集
    with ThreadPoolExecutor(max_workers=10) as threadpool:
        # 多线程执行函数pr(n),map有序
        # results = list(threadpool.map(get_weibos_by_page,range(2,math.ceil(total/10))))
        results = list(threadpool.map(get_weibos_by_page,range(2,1000)))
        # 拼接第一页和剩余微博
        weibos = list(results_page1) + sum(list(map(list , results)),[])
    write_weibo_info(weibos)
 
        

