import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
import re
from bs4 import BeautifulSoup

def get_page_index():
    data = {
        'offset':0,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':20,
        'cur_tab':3,
        'from':'gallery'
    }
    url = "https://www.toutiao.com/search_content/?"+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print("解析错误")
        return None

def parse_page_index(text):
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                 yield item.get('article_url')
    except :
        print("json解析错误")
    finally:
        pass

def parse_page(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    response = requests.get(url,headers= header)
    if response.status_code==200:
        html =BeautifulSoup(response.text,'lxml')
        print(html)
        title = html.find("title").get_text()
        images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
        result = re.search(images_pattern, html.text)
        if result:
            data = json.loads(result.group(1).replace('\\', ''))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
    return {
        'images':images,
        'title':title
    }




def main():
    html = get_page_index()
    urls = parse_page_index(html)
    for url  in urls:
        a =parse_page(url)
        print(a)
if __name__ == '__main__':
    main()