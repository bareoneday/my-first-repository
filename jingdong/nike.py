import requests
from selenium import webdriver
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
from func_timeout import func_set_timeout
import time
import threading
from retrying import retry


def search(html,front,count,end):
    a=html.find(front)+count
    b=html.find(end,a)
    if a!=count-1:
        return html[a:b]
    else:
        return ('')

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

def geturl(url,classname):

    try:
        d = webdriver.Chrome(options=options)
        d.maximize_window()
        d.execute_script("document.body.style.zoom='1.5'")
        d.set_page_load_timeout(30)
        d.set_script_timeout(30)
        trytimes=0
        for i in range(3):
            try:
                d.get(url)
                break
            except:
                trytimes+=1
                if trytimes==3:
                    print('网页进不去')
                    break
                else:
                    continue
        stop=0
        while True:
            preproductlist = d.find_element_by_xpath(
                '//*[@id="Wall"]/div/div[5]/div[2]/main/section/div').find_elements_by_class_name(
                "product-card__link-overlay")
            div = preproductlist[-1]
            # 滑动滚动条到某个指定的元素
            js4 = "arguments[0].scrollIntoView();"
            # 将下拉滑动条滑动到当前div区域
            d.execute_script(js4, div)
            time.sleep(3)
            postproductlist = d.find_element_by_xpath(
                '//*[@id="Wall"]/div/div[5]/div[2]/main/section/div').find_elements_by_class_name(
                "product-card__link-overlay")
            print(str(len(postproductlist)))
            if (postproductlist != preproductlist):
                stop = 0
            else:
                stop += 1
            if stop > 5:
                break


        n=d.find_element_by_xpath('//*[@id="Wall"]/div/div[5]/div[2]/main/section/div').find_elements_by_class_name("product-card__link-overlay")
        urls = []
        print('%s模块产品个数为%d'%(classname,len(n)))
        for i in n:
            ur=i.get_attribute('href')
            urls.append(ur)
        d.close()
        return urls
    except Exception as e:
        print(e)
        print(classname+'爬取url错误')
        return geturl(url,classname)

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

@retry(stop_max_attempt_number=3)
@func_set_timeout(10)
def get(url,d):
    d.get(url)

def find(informationlist,html,classname,d):
    price = search(html, 'product-price">', len('product-price">'), '<')
    price=price.replace('¥','')
    style=search(html,'款式： ',len('款式： '),'<')
    reducedprice = search(html, 'product-price-reduced">', len('product-price-reduced">'), '<')
    reducedprice = reducedprice.replace('¥', '')
    if reducedprice=='':
        reducedprice='无'
    cururl=d.current_url
    productname=search(search(html,'pdp_product_title',0,'<'),'>',1,'<')
    informationlist.append(productname+'|'+classname[:4]+'|'+style+'|'+price+'|'+reducedprice+'|'+cururl+'\n')

@retry(stop_max_attempt_number=2)
@func_set_timeout(30)
def write(informationlist,d,classname):
    skus = 0
    html=d.page_source
    try:
        d.find_element_by_xpath('//*[@id="nby-buttonclip-path"]')
        informationlist.append('定制商品')
        find(informationlist,html,classname,d)
        skus+=1
    except:
        try:
            stylenum=searchall(html,'colorway-product-overlay',0,'>')
            if len(stylenum)>1:
                stylelist=d.find_elements_by_xpath('//*[@id="ColorwayDiv"]/div/div/div/div')
                for st in stylelist:
                    st.click()
                    html=d.page_source
                    find(informationlist,html,classname,d)
                    skus+=1
            else:
                find(informationlist,html,classname,d)
                skus+=1
        except:
            print('异常产品')
    return skus

def report(filename,urls):
    with open('D://nike//'+filename+'.txt','w') as reporturls:
        for href in urls:
            reporturls.write(href+'\n')

def catch(filename,urls):
    with open('D://nike//'+filename+'.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])


def urlsget(url,classname):
    print(classname + '开始爬url')
    print(time.localtime(time.time()))
    iniurls = list(set(geturl(url, classname)))
    print('总共有产品数量%s' % len(iniurls))
    report(classname + 'urls', iniurls)

#urlsget('https://www.nike.com/cn/w/mens-shoes-nik1zy7ok','男子鞋类')
#urlsget('https://www.nike.com/cn/w/mens-apparel-6ymx6znik1','男子服装')
#urlsget('https://www.nike.com/cn/w/womens-shoes-5e1x6zy7ok','女子鞋类')
#urlsget('https://www.nike.com/cn/w/womens-apparel-5e1x6z6ymx6','女子服装')
#urlsget('https://www.nike.com/cn/w/boys-apparel-1onraz6ymx6','男孩服装')
#urlsget('https://www.nike.com/cn/w/girls-apparel-3aqegz6ymx6','女孩服装')
#urlsget('https://www.nike.com/cn/w/boys-shoes-1onrazy7ok','男孩鞋类')
#urlsget('https://www.nike.com/cn/w/girls-shoes-3aqegzy7ok','女孩鞋类')

'''aparturls=[]

with open('D://nike//男子服装urls.txt','r') as file:
    for i in file.readlines():
        aparturls.append(i)

with open('D://nike//男子服装urls.txt','w') as file:
    for i in aparturls[:710]:
        file.write(i)

with open('D://nike//男子服装1urls.txt','w') as file:
    for i in aparturls[710:]:
        file.write(i)'''

def main(threadname,classname):
    urls=[]
    catch(classname+'urls',urls)

    totalsku = 0
    sum=0

    d = webdriver.Chrome(options=options)
    d.set_page_load_timeout(20)
    d.set_script_timeout(20)
    d.maximize_window()
    print(threadname+'开始爬商品信息')
    print(time.localtime(time.time()))
    informationlist=[]

    for href in urls:
        for k in range(3):
            try:
                op(href,d)
                if sum!=0:
                    d.close()
                turn(-1,d)

                totalsku+=write(informationlist,d,classname)
                sum+=1
                break

            except:
                print(threadname+'%d次进入失败' % (k + 1))
                try:
                    turn(0,d)
                    d.quit()
                except:
                    pass

                d = webdriver.Chrome(options=options)
                d.set_page_load_timeout(20)
                d.set_script_timeout(20)
                d.maximize_window()
                op('blank',d)
                turn(-1,d)
                if k == 2:
                    print(threadname+'进入单品网页失败' + href)
        if sum%50==0:
            print(threadname+'前%d个产品共%d个sku'%(sum,totalsku))
            print(time.localtime(time.time()))

    with open('D://nike//' + classname + 'informations.txt', 'w') as file:
        for information in informationlist:
            file.write(information)

    print(time.localtime(time.time()))

def main2(threadname1,classname1,threadname2,classname2):
    main(threadname1,classname1)
    main(threadname2,classname2)

def main3(threadname1,classname1,threadname2,classname2,threadname3,classname3):
    main(threadname1,classname1)
    main(threadname2,classname2)
    main(threadname3,classname3)


#t1=threading.Thread(target=main,args=('t1','男子鞋类'))
#t2=threading.Thread(target=main,args=('t2','男子服装'))
t567=threading.Thread(target=main3,args=('t5','男孩服装','t6','女孩服装','t7','男孩鞋类'))
# t38=threading.Thread(target=main2,args=('t3','女子鞋类','t8','女孩鞋类'))
# t49=threading.Thread(target=main2,args=('t4','女子服装','t9','男子服装1'))

# t1.start()
# t2.start()
t567.start()
# t38.start()
# t49.start()