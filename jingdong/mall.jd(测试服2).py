import requests
from selenium import webdriver

from func_timeout import func_set_timeout
import time
from retrying import retry
import asyncio
import time, random

from pyppeteer.launcher import launch
import tkinter
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

async def pagemaximize(page):
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    # 是页面得宽和高
    await page.setViewport(viewport={'width': width, 'height': height})

def search(html,front,count,end):
    a=html.find(front)+count
    b=html.find(end,a)
    if a!=count-1:
        return html[a:b]
    else:
        return ('')

def searchsku(str):
    line=str.find('-')
    if (str[line-7]==' '):
        return str[(line-6):(line+4)]
    else:
        strsub=str[(line+1):]
        return searchsku(strsub)



def searchall(html,front,count,end):
    c=0
    a=0
    al=[]
    while a!=count-1:
        a=html.find(front,c)+count
        b=html.find(end,a)
        c=b
        d=html[a:b]
        if a!=count-1:
            al.append(d)
    return al

@func_set_timeout(60)
async def write(page,file):
    skus=0
    judge=await(await page.querySelector('#choose-attrs >div')).getProperty('id')
    judge = await judge.jsonValue()
    #print(judge)
    if judge=='choose-attr-1' :
        allstyles=await page.querySelectorAll('#choose-attr-1 > div.dd > div')
        for count in range(len(allstyles)):

            for j in range(3):
                try:
                    await page.click('#choose-attr-1 > div.dd > div:nth-child(%d)'%(count+1))
                    break
                except:
                    if j == 2:
                        print('进入单款式网页失败')
            item=await page.waitForSelector('body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.p-price')
            jdprice=await page.evaluate('item => item.textContent', item)
            item=await page.waitForSelector('body > div:nth-child(9) > div > div.itemInfo-wrap > div.sku-name')
            productname=await page.evaluate('item => item.textContent', item)
            thesku=searchsku(productname)
            html=await page.content()
            suitgroup=search(html,'适用',0,'<')
            cururl=page.url
            try:
                item = await page.querySelector('body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.pricing')
                pastprice = await page.evaluate('item => item.textContent', item)
            except:
                pastprice=''
            file.write(cururl+'sku：'+thesku + ' '+suitgroup+' 京东价：' + jdprice + ' 原价：' + pastprice + '\n')
            skus += 1



    else:
        item = await page.waitForSelector(
            'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.p-price')
        jdprice = await page.evaluate('item => item.textContent', item)
        item = await page.waitForSelector('body > div:nth-child(9) > div > div.itemInfo-wrap > div.sku-name')
        productname = await page.evaluate('item => item.textContent', item)
        thesku = searchsku(productname)
        html = await page.content()
        suitgroup = search(html, '适用人群', 0, '<')
        cururl =page.url
        try:
            item = await page.querySelector(
                'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.pricing')
            pastprice = await page.evaluate('item => item.textContent', item)
        except:
            pastprice = ''
        file.write(cururl+'sku：' + thesku + ' ' + suitgroup + ' 京东价：' + jdprice + ' 原价：' + pastprice + '\n')
        skus += 1
    return skus


@func_set_timeout(5)
async def op(browser,href):
    page = await browser.newPage()
    await page.goto(href)
    return page

@retry(stop_max_attempt_number=3)
@func_set_timeout(10)
async def get(url,page):
    await page.goto(url)

#打开网页获取页数
async def geturls(page):
    html = await page.content()
    pagesum = search(html,'<em>/</em>',13,'</i>')
    pagesum=int(pagesum)
    print('共有页数%d'%pagesum)

    gettime = time.localtime(time.time())
    print(gettime)
    # 获取所有产品url
    urls = []
    for r in range(pagesum):
        for t in range(3):
            try:
                for j in range(10):
                    js = 'window.scrollTo(0,%s)' % (j * 50)
                    await  page.evaluate(js)
                    time.sleep(0.1)
            except:
                pass
            #await page.waitFor(2000)

            try:
                n = await page.Jx ('//*[@id="J_GoodsList"]/ul/li/div/div[1]/a')
                for item in n:
                    href = await (await item.getProperty('href')).jsonValue()
                    urls.append(href)
                print('前%d页产品数量%d' % (r + 1, len(urls)))
                break
            except:
                if t == 2:
                    print('进入该页面失败')
        for y in range(3):
            try:

                await page.click('#J_topPage > a.fp-next')

                for dd in range(5):
                    item=await page.waitForSelector('#J_topPage > span > b')
                    presenpage=await page.evaluate('item => item.textContent', item)
                    presenpage=int(presenpage)
                    if presenpage<r+2:
                        time.sleep(1)
                        if dd==4:
                            await page.click('#J_topPage > a.fp-next')
                            break
                    if presenpage==r+2:
                        break
                break
            except:
                if y == 2:
                    print('点击下一页失败')
    return urls

async def report(urls):
    with open('D://malljd2//urls.txt','w') as reporturls:
        for href in urls:
            reporturls.write(href+'\n')

async def catch(urls):
    with open('D://malljd2//urls.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])

async def intercept_request(req):
    """请求过滤"""
    if req.resourceType in ['media','image']:
        await req.abort()
    else:
        await req.continue_()
#主函数
async def main():
    browser = await launch( {'headless': False,'slowMo': 10, 'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe','devtools': False, "args":["--start-maximized"]})
    page = await browser.newPage()

    await pagemaximize(page)

    await page.setRequestInterception(True)
    page.on('request', intercept_request)

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    totalurl='https://mall.jd.com/view_search-1005989-14942044-99-1-24-1.html'
    await get(totalurl,page)

    #iniurls=await geturls(page)

    #await report(list(set(iniurls)))

    urls=[]

    await catch(urls)

    sku = 0
    num = 0
    starttime = time.localtime(time.time())
    print(starttime)
    with open('D://malljd2//informations.txt','w')as file:
        for href in urls[:30]:
            for k in range(3):
                try:
                    if num !=0:
                        await page.close()
                    page=await browser.newPage()
                    await pagemaximize(page)
                    await page.goto(href)
                    sku+=await write(page,file)
                    num+=1
                    break
                except Exception as e:
                    print(e)
                    await browser.close()
                    print('%d次进入失败'%(k+1))
                    browser = await launch({'headless': False, 'slowMo': 10, 'devtools': False,'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe',"args":["--start-maximized"]})
                    page = await browser.newPage()
                    await pagemaximize(page)
                    if k==2:
                        print('进入单品网页失败'+href)
            if num%20==0:
                print('前%d个产品sku数量为%d' % (num, sku))
                print(time.localtime(time.time()))




if __name__ == '__main__':

    loop=asyncio.new_event_loop()
    print('成功')
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print (e)