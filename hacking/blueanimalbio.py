# crawl blueanimalbio.com

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse, unquote


def isValidURL(url):
    p = urlparse(url)
    if p.netloc.find('blueanimalbio.com')==-1:
        return False
    return bool(p.netloc) and bool(p.scheme)

def getFilesOnPage(url,content):
    soup = BeautifulSoup(content, "html.parser")
    files = []
    # images
    for img in tqdm(soup.find_all('img')):
        src = img.attrs.get('src')
        if src:
            src = urljoin(url,src)
            if isValidURL(src):
                files.append(src)
    # CSS
    for css in tqdm(soup.find_all('link')):
        href = css.attrs.get('href')
        if href:
            href = urljoin(url,href)
            if isValidURL(href):
                files.append(href)
    # skip JS
    return list(dict.fromkeys(files))

def getLinksOnPage(url,content):
    soup = BeautifulSoup(content, "html.parser")
    links = []
    for a in tqdm(soup.find_all('a')):
        href = a.attrs.get('href')
        if href:
            href = urljoin(url,href)
            href = href[:(href+'#').find('#')]
            if isValidURL(href):
                links.append(href)
    return list(dict.fromkeys(links))


import os

crawledPages = {}


def saveFile(url):
    filename = "blueanimalbio.com"+unquote(urlparse(url).path)
    if url in crawledPages:
        print("File already exists:", filename)
        return False
    if os.path.exists(filename):
        print("File on disk:", filename)
        crawledPages[filename]=True
        return True
    pathname = filename[:filename.rfind('/')+1]
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    r = requests.get(url)
    if r.status_code!=200:
        print("Error", r.status_code, url)
        return False
    print(url)
    with open(filename, 'wb') as fp:
        for c in r:
            fp.write(c)
    crawledPages[filename]=True
    return True

def crawl(url):
    # if already crawled?
    filename = "blueanimalbio.com"+unquote(urlparse(url).path)
    pathname = filename[:filename.rfind('/')+1]
    s = ""
    if url in crawledPages:
        print("Page already exists:", filename)
        return False
    if os.path.exists(filename):
        print("Page on disk:", filename)
        s = open(filename, "r", encoding='utf-8').read()
    else:
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        r = requests.get(url)
        if r.status_code!=200:
            print("Error:", r.status_code, url)
            return False
        print(url)

        # what a mess
        import re
        r.encoding = "gb2312"
        s = r.content.decode('gb2312',errors='ignore')
        s = s.replace('\r\n','\n')
        s = re.sub("charset=[A-Za-z0-9\-]+","charset=utf-8",s)

    # save page
    open(filename, "w", encoding="utf-8").write(s)
    crawledPages[url]=True

    # save files
    files = getFilesOnPage(url, s)
    for file in files:
        try:
            saveFile(file)
        except:
            print("An exception has occured")

    # crawl page
    pages = getLinksOnPage(url, s)
    for page in pages:
        try:
            crawl(page)
        except:
            print("An exception has occured")


    
    
crawl('http://blueanimalbio.com/index.htm')

