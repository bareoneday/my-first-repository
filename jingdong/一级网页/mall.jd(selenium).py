from selenium import webdriver
import time


dr = webdriver.ChromeOptions()
dr.add_argument('lang=zh_CN.UTF-8')
dr.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"')
br=webdriver.Chrome(chrome_options=dr)
br.get('https://mall.jd.com/index-782694.html')
for i in range(100):
    js = 'window.scrollTo(0,%s)'%(i*100)
    br.execute_script(js)
    time.sleep(0.1)
time.sleep(5)
source = br.page_source

price = br.find_element_by_xpath("//span[@class='jdNum']")
print(price)
print(price.text)
#for i in price:
#    print(i.text)
br.close()