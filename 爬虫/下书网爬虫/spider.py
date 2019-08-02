import random
import time

from requests_html import HTMLSession


def get_page_title_and_detial(session, target_url):
    #获取
    r = session.get(target_url)

    return (r.html.xpath("//div[@class='atitle']/h1")[0].text, r.html.xpath("//div[@class='zw']")[0].text)


# 需要改成录入数据库
book_target_url_data_list = []  # [(url, (start, end)), ...]
#启动
session = HTMLSession()
url = 'https://www.shutxt.com/mz/27757/'
page_num = 1424130
def get_book_target_url_range(session, url, page_num, book_target_url_data_list, start_num):
    #获取
    target_url = url + '{}.html'.format(page_num)
    r = session.get(target_url)

    article_title_and_content = get_page_title_and_detial(session, target_url)
    with open('{}.txt'.format(article_title_and_content[0]), 'w', encoding='UTF-8') as f:
        f.writelines(article_title_and_content[1])
        print('写入一篇')

    is_next_page_list = r.html.xpath("//div[@class='np']/a/text()")  # 上一章以及下一章所在列表

    if '下一章' in is_next_page_list:
        # 随机定时
        time.sleep(random.uniform(0.9, 3.1))
        # 如果存在下一章则继续下一页
        page_num += 1
        get_book_target_url_range(session, url, page_num, book_target_url_data_list, start_num)
    else:
        # 这本书或小说的全部章节收取完毕
        book_target_url_data_list.append((url, (start_num, page_num + 1)))

start_num = page_num
get_book_target_url_range(session, url, page_num, book_target_url_data_list, start_num)
print(book_target_url_data_list)
