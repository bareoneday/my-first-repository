import asyncio
import time
from pyppeteer.launcher import launch
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


def catch(urls):
    with open('D://malljd2//urls.txt','r') as catch:
        for line in catch.readlines():
            urls.append(line[:-1])
urls = []
catch(urls)

async def br():
    browser = await launch({'headless': False, 'slowMo': 10,
                            'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe',
                            'devtools': False, "args": ["--start-maximized"]})



async def get_pagetext(url):
    browser = await launch({'headless': False, 'slowMo': 10,
                            'executablePath': 'C:/Users/zhijue/AppData/Local/Google/Chrome/Application/chrome.exe',
                            'devtools': False, "args": ["--start-maximized"]})
    print(url,"正在下载。。。")
    page = await browser.newPage()
    await page.goto(url)

# 存放多个任务列表
stacks = []
start = time.time()
for url in urls:
    c = get_pagetext(url)
    # 将方法注册到loop对象中
    task = asyncio.ensure_future(c)
    stacks.append(task)
# 创建loop对象
loop = asyncio.get_event_loop()
# 将任务列表封装到asyncio.wite()中  固定的格式
loop.run_until_complete(asyncio.wait(stacks))
print(time.time()-start)