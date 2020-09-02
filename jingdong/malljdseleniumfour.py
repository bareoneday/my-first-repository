from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
from func_timeout import func_set_timeout
import time
import threading
from retrying import retry
from pyppeteer.launcher import launch
import tkinter
import asyncio

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

@func_set_timeout(5)
def op(href,d):
    if href!='blank':
        js = "window.open('" + href + "')"
        d.execute_script(js)
    else:
        js = "window.open()"
        d.execute_script(js)

@func_set_timeout(5)
def turn(pagenum,d):
    cw = d.window_handles
    d.switch_to.window(cw[pagenum])

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
def write(d,filename):
    skus=0
    judge=d.find_element_by_xpath("//div[@id='choose-attrs']/*").get_attribute('id')
    if judge=='choose-attr-1' :
        allstyles = d.find_elements_by_css_selector('#choose-attr-1 > div.dd > div')
        for count in range(len(allstyles)):
            for j in range(3):
                try:
                    d.find_element_by_css_selector('#choose-attr-1 > div.dd > div:nth-child(%d)' % (count + 1)).click()
                    break
                except:
                    if j == 2:
                        print('进入单款式网页失败')
            while True:
                jdprice = d.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]').text
                if jdprice != '￥':
                    break
            jdprice=jdprice.replace('￥','')
            productname = d.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[1]').text
            thesku = searchsku(productname)
            html = d.page_source
            suitgroup = search(html, '适用人群', 0, '<')
            cururl = d.current_url
            try:
                pastprice = d.find_element_by_xpath('//*[@id="page_hx_price"]').text
                pastprice=pastprice.replace('￥','')
            except:
                pastprice = jdprice
            if '鞋' in productname:
                classname='鞋类'
            else:
                classname='非鞋类'
            with open('D://malljd1//' + filename + '.txt', 'a') as file:
                file.write(productname + '|' + classname + '|' + suitgroup[5:] + '|' + thesku + '|' + pastprice + '|' + jdprice + '|' + cururl + '\n')

            skus += 1



    else:
        while True:
            jdprice = d.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]').text
            if jdprice!='￥':
                break

        productname = d.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[1]').text
        thesku = searchsku(productname)
        html=d.page_source
        suitgroup = search(html, '适用人群', 0, '<')
        cururl = d.current_url
        try:
            pastprice=d.find_element_by_xpath('//*[@id="page_hx_price"]').text
            pastprice = pastprice.replace('￥', '')
        except:
            pastprice=jdprice

        jdprice = jdprice.replace('￥', '')
        if '鞋' in productname:
            classname = '鞋类'
        else:
            classname = '非鞋类'

        with open('D://malljd1//' + filename + '.txt', 'a') as file:
            file.write(productname + '|' + classname + '|' + suitgroup[5:] + '|' + thesku + '|' + pastprice + '|' + jdprice + '|' + cururl + '\n')

        skus += 1
    return skus

@retry(stop_max_attempt_number=3)
@func_set_timeout(10)
def get(url):
    d.get(url)

#打开网页获取页数
'''def geturls():
    s=d.find_element_by_xpath('//*[@id="J_topPage"]/span/i')
    b=int(s.text)

    gettime = time.localtime(time.time())
    print(gettime)
    #获取所有产品url
    urls=[]
    for r in range(b):
        for t in range(3):
            try:
                for ii in range(20):
                    js='window.scrollTo(0,%s)' % (ii*100)
                    d.execute_script(js)
                    time.sleep(0.1)
            except:
                pass

            try:
                n = d.find_elements_by_xpath('//*[@id="J_GoodsList"]/ul/li/div/div[1]/a')
                for i in n:
                    href=i.get_attribute("href")
                    urls.append(href)
                print('前%d页产品数量%d'%(r+1,len(urls)))
                break
            except:
                if t==2:
                    print('进入该页面失败')
        for y in range(3):
            try:
                d.find_element_by_link_text('>').click()
                break
            except:
                if y==2:
                    print('点击下一页失败')
    return urls'''

async def pagemaximize(page):
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    # 是页面得宽和高
    await page.setViewport(viewport={'width': width, 'height': height})

async def intercept_request(req):
    """请求过滤"""
    if req.resourceType in ['media','image']:
        await req.abort()
    else:
        await req.continue_()

async def geturls():
    browser = await launch({'headless': False, 'slowMo': 10,
                            'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe',
                            'devtools': False, "args": ["--start-maximized"]})
    page = await browser.newPage()

    await pagemaximize(page)

    await page.setRequestInterception(True)
    page.on('request', intercept_request)

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    await page.goto('https://mall.jd.com/view_search-1005989-14942044-99-1-24-1.html')
    html=await page.content()
    pagesum = search(html,'<em>/</em>',13,'</i>')
    pagesum=int(pagesum)
    print('共有页数%d'%pagesum)

    print(time.localtime(time.time()))
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
    await browser.close()
    report(list(set(urls)))

def report(urls):
    with open('D://malljd1//urls.txt','w') as reporturls:
        for href in urls:
            reporturls.write(href+'\n')

def catch(urls):
    with open('D://malljd1//urls.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])

# try:
#     get('https://mall.jd.com/view_search-1005989-14942044-99-1-24-1.html')
# except:
#     print('总网页进入失败')
#
# if __name__ == '__main__':
#     loop=asyncio.new_event_loop()
#     print('成功')
#     try:
#         loop.run_until_complete(geturls())
#     except Exception as e:
#         print (e)


urls=[]
catch(urls)
urls1=[]
urls2=[]
urls3=[]
urls4=[]
for i in range(len(urls)):
    if i%4==1:
        urls1.append(urls[i])
    if i%4==2:
        urls2.append(urls[i])
    if i%4==3:
        urls3.append(urls[i])
    if i%4==0:
        urls4.append(urls[i])
print(len(urls),len(urls1),len(urls2),len(urls3),len(urls4))

def main(threadname,urls,filename):
    sku = 0
    num = 0
    d = webdriver.Chrome(options=options)
    d.set_page_load_timeout(20)
    d.set_script_timeout(20)
    d.maximize_window()
    starttime = time.localtime(time.time())
    print(starttime)
    for href in urls:
        for k in range(3):
            try:
                op(href,d)
                if num !=0:
                    d.close()
                turn(-1,d)
                sku+=write(d,filename)
                num+=1
                break
            except:
                print(threadname+'%d次进入失败'%(k+1))
                turn(0,d)
                d.quit()
                d = webdriver.Chrome(options=options)
                d.set_page_load_timeout(20)
                d.set_script_timeout(20)
                d.maximize_window()
                op('blank',d)
                turn(-1,d)
                if k==2:
                    print(threadname+'进入单品网页失败'+href)
        if num%50==0:
            print(threadname+'前%d个产品sku数量为%d' % (num, sku))
            print(time.localtime(time.time()))



    print(threadname+'完成')
    print(time.localtime(time.time()))
    d.quit()


t1=threading.Thread(target=main,args=('t1',urls1,'information1'))
t2 = threading.Thread(target=main, args=('t2', urls2, 'information2'))
t3 = threading.Thread(target=main, args=('t3', urls3, 'information3'))
t4 = threading.Thread(target=main, args=('t4', urls4, 'information4'))
t1.start()
t2.start()
t3.start()
t4.start()