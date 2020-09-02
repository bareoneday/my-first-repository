import time
import asyncio
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
from pyppeteer.launcher import launch
from func_timeout import func_set_timeout
import time
from retrying import retry
import tkinter

async def pagemaximize(page):
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    # 是页面得宽和高
    await page.setViewport(viewport={'width': width, 'height': height})

def catch(urls):
    with open('D://malljd2//urls.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])

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
            suitgroup=search(html,'适用人群',0,'<')
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

urls=[]
catch(urls)


async def goto(href,file,browser):
    for k in range(3):
        try:

            page = await browser.newPage()

            await pagemaximize(page)

            await page.setUserAgent(
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

            await page.goto(href)


            judge = await(await page.querySelector('#choose-attrs >div')).getProperty('id')
            judge = await judge.jsonValue()
            if judge == 'choose-attr-1':
                allstyles = await page.querySelectorAll('#choose-attr-1 > div.dd > div')
                for count in range(len(allstyles)):

                    for j in range(3):
                        try:
                            await page.click('#choose-attr-1 > div.dd > div:nth-child(%d)' % (count + 1))
                            break
                        except:
                            if j == 2:
                                print('进入单款式网页失败')
                    item = await page.waitForSelector(
                        'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.p-price')
                    jdprice = await page.evaluate('item => item.textContent', item)
                    item = await page.waitForSelector(
                        'body > div:nth-child(9) > div > div.itemInfo-wrap > div.sku-name')
                    productname = await page.evaluate('item => item.textContent', item)
                    thesku = searchsku(productname)
                    html = await page.content()
                    suitgroup = search(html, '适用人群', 0, '<')
                    cururl = page.url
                    try:
                        item = await page.querySelector(
                            'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.pricing')
                        pastprice = await page.evaluate('item => item.textContent', item)
                    except:
                        pastprice = ''
                    file.write(
                        cururl + 'sku：' + thesku + ' ' + suitgroup + ' 京东价：' + jdprice + ' 原价：' + pastprice + '\n')

            else:
                item = await page.waitForSelector(
                    'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.p-price')
                jdprice = await page.evaluate('item => item.textContent', item)
                item = await page.waitForSelector('body > div:nth-child(9) > div > div.itemInfo-wrap > div.sku-name')
                productname = await page.evaluate('item => item.textContent', item)
                thesku = searchsku(productname)
                html = await page.content()
                suitgroup = search(html, '适用人群', 0, '<')
                cururl = page.url
                try:
                    item = await page.querySelector(
                        'body > div:nth-child(9) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.pricing')
                    pastprice = await page.evaluate('item => item.textContent', item)
                except:
                    pastprice = ''
                file.write(cururl + 'sku：' + thesku + ' ' + suitgroup + ' 京东价：' + jdprice + ' 原价：' + pastprice + '\n')
            await browser.close()
            break
        except:
            print('第%d次进入失败'%(k+1))



async def br():
    browser = await launch({'headless': False, 'slowMo': 10,
                            'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe',
                            'devtools': False, "args": ["--start-maximized"]})
    return browser

browser=br()

async def main(count1,count2,count3,count4,count5,count6,file,browser):
    await asyncio.gather(goto(urls[count1],file,browser), goto(urls[count2],file,browser), goto(urls[count3],file,browser),goto(urls[count4],file,browser),goto(urls[count5],file,browser),goto(urls[count6],file,browser))

print(time.localtime(time.time()))
with open('D://malljd2//informations.txt','w')as file:
    for i in range(30):
        if i%6==0:
            asyncio.run(main(i,i+1,i+2,i+3,i+4,i+5,file,browser))
print(time.localtime(time.time()))