import requests
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
from func_timeout import func_set_timeout
import time
from retrying import retry

@func_set_timeout(60)
def write(g):
    skus=0
    with open('D://malljd//'+g+'.txt', 'w') as z:
        kk=d.find_element_by_xpath("//div[@id='choose-attrs']/*")
        aa=kk.get_attribute('id')
        if aa=='choose-attr-1' :
            r = d.find_elements_by_xpath("//div[@id='choose-attr-1']/*/*")
            rr=len(r)
            for u in range(rr):

                for j in range(3):
                    try:
                        r[u].click()
                        break
                    except:
                        if j == 2:
                            print('进入单款式网页失败')
                    r = d.find_elements_by_xpath("//div[@id='choose-attr-1']/*/*")

                    hh=r[u].get_attribute('data-sku')
                    # gg=r[u].get_attribute('data-value')

                    z.write('商品编号：'+hh)

                    v = d.find_element_by_class_name('p-price').text
                    z.write(' 京东价:' + v)

                    try:
                        vv = d.find_element_by_class_name('pricing').text
                        z.write(' 原价：' + vv + '\n')
                    except:
                        z.write('\n')
                skus += 1



        else:
            style=d.find_element_by_xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[2]').text

            z.write(style)

            v = d.find_element_by_class_name('p-price').text
            z.write(' 京东价：'+v)
            try:
                vv = d.find_element_by_class_name('pricing').text
                z.write(' 原价：' + vv + '\n')
            except:
                z.write('\n')
            skus += 1
    return skus


@func_set_timeout(5)
def op(href):
    js = "window.open('" + href + "')"
    d.execute_script(js)



@func_set_timeout(5)
def turn(pagenum):
    cw = d.window_handles
    d.switch_to.window(cw[pagenum])

@retry(stop_max_attempt_number=3)
@func_set_timeout(10)
def get(url):
    d.get(url)

#打开网页获取页数
def geturls():
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
                p=d.find_element_by_link_text('>').click()
                break
            except:
                if y==2:
                    print('点击下一页失败')
    return urls

def report(urls):
    with open('D://malljd//urls.txt','w') as reporturls:
        for href in urls:
            reporturls.write(href+'\n')

def catch(urls):
    with open('D://malljd//urls.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])


#主函数

d = webdriver.Chrome(options=options)
d.set_page_load_timeout(20)
d.set_script_timeout(20)
d.maximize_window()

try:
    get('https://mall.jd.com/view_search-1005989-14942044-99-1-24-1.html')
except:
    print('总网页进入失败')



#iniurls=geturls()


#report(iniurls)

urls=[]

catch(urls)

sku = 0
num = 0
starttime = time.localtime(time.time())
print(starttime)
for href in urls:
    g=href
    g=g.replace('\\','')
    g = g.replace('/', '')
    g = g.replace(':', '')
    g = g.replace('*', '')
    g = g.replace('?', '')
    g = g.replace('"', '')
    g = g.replace('<', '')
    g = g.replace('>', '')
    g = g.replace('|', '')
    for k in range(3):
        try:
            op(href)
            if num !=0:
                d.close()
            turn(-1)
            sku+=write(str(num+1))
            num+=1
            break
        except:
            print('%d次进入失败'%(k+1))
            d = webdriver.Chrome(options=options)
            d.set_page_load_timeout(20)
            d.set_script_timeout(20)
            d.maximize_window()
            if k==2:
                print('进入单品网页失败'+href)
    if num%20==0:
        print('前%d个产品sku数量为%d' % (num, sku))
        print(time.localtime(time.time()))



time.sleep(1)
d.close()