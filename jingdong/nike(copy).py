#引入必要的包
from selenium import webdriver
import time
import threading
_author_='小强测试品牌 www.xqtesting.com'
def test_search(browser, url):
    if browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    #访问测试帮日记官网，并搜索关键字小强测试品牌
    driver.get(url)
    driver.find_element('id',"words").send_keys('小强测试品牌')
    driver.find_element('class name', 'btn-default').click()
    time.sleep(5)
    driver.quit()
data = {
    "firefox": "http://www.xqtesting.com",
    "chrome": "http://www.xqtesting.com/blog.html"
}
threads = []
for browser, url in data.items():
    #多线程
    t1 = threading.Thread(target=test_search, args=(browser, url,))
    threads.append(t1)
# 启动
for t2 in threads:
    t2.start()
    t2.join()#此处注释掉会同时运行。但同时运行可能会出现遮挡导致有问题哦。