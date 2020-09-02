import os
import time
import random
import asyncio
import pyppeteer


class LoginTaoBao:

    def __init__(self):
        os.environ['PYPPETEER_CHROMIUM_REVISION'] = '575458'
        pyppeteer.DEBUG = True
        self.page = None

    async def _injection_js(self):
        """
        注入js 突破淘宝封锁
        :return:
        """

        # 这个是关键参数, 主要靠这个
        await self.page.evaluate('''() =>{

                   Object.defineProperties(navigator,{
                     webdriver:{
                       get: () => false
                     }
                   })
                }''')

        await self.page.evaluate('''() => {
            window.navigator.chrome = {
            runtime: {},
            // etc.
            };
            }''')

        await self.page.evaluate('''() => {
                  const originalQuery = window.navigator.permissions.query;
                  return window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                      Promise.resolve({ state: Notification.permission }) :
                      originalQuery(parameters)
                  );
                }
            ''')

        await self.page.evaluate('''() =>{
            Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
                });
            }''')

        await self.page.evaluate('''() =>{
            Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
                });
            }''')

    async def _init(self):
        """
        初始化浏览器
        :return:
        """
        # 设置浏览器参数
        browser = await pyppeteer.launch({'headless': False,
                                          'args': [
                                              '--disable-extensions',
                                              '--hide-scrollbars',
                                              '--disable-bundled-ppapi-flash',
                                              '--mute-audio',
                                              '--no-sandbox',
                                              '--disable-setuid-sandbox',
                                              '--disable-gpu',
                                          ],
                                          'dumpio': True,
                                          })
        # 创建浏览器对象
        self.page = await browser.newPage()
        # 设置浏览器头部
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        # 设置浏览器大小
        await self.page.setViewport({'width': 1080, 'height': 960})

    async def get_cookie(self):
        cookies_list = await self.page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies)
        return cookies

    async def mouse_slider(self):
        """
        滑动滑块
        :return: None 滑动失败 或者 True滑动成功
        """
        await asyncio.sleep(3)
        try:
            await self.page.hover('#nc_1_n1z')
            # 鼠标按下按钮
            await self.page.mouse.down()
            # 移动鼠标
            await self.page.mouse.move(1000, 0, {'steps': 30})
            # 松开鼠标
            await self.page.mouse.up()
            await asyncio.sleep(2)
        except Exception as e:
            print(e, '      :slider login error')
            return None
        else:
            await asyncio.sleep(3)
            # 获取元素内容
            ua = await self.page.evaluate('navigator.webdriver')
            print(ua)
            await self.page.screenshot({'path': './headless-slide-result.png'})
            slider_again = await self.page.querySelectorEval('#nc_1__scale_text', 'node => node.textContent')
            if slider_again != '验证通过':
                return None
            else:
                # 截图
                await self.page.screenshot({'path': './headless-slide-result.png'})
                print('验证通过')
                return True

    async def main(self, username_, pwd_):
        """
        登陆并获取cookie
        :param username_: 账号
        :param pwd_: 密码
        :return: cookie 或 None
        """
        # 初始化浏览器
        await self._init()
        # 打开淘宝登陆页面
        await self.page.goto('https://login.taobao.com')
        # 注入js
        await self._injection_js()
        # 点击密码登陆按钮
        await self.page.click('div.login-switch')
        time.sleep(random.random() * 2)
        # 输入用户名
        await self.page.type('#TPL_username_1', username_, {'delay': random.randint(100, 151) - 50})
        # 输入密码
        await self.page.type('#TPL_password_1', pwd_, {'delay': random.randint(100, 151)})
        time.sleep(random.random() * 2)
        # 获取滑块元素
        slider = await self.page.querySelector('#nc_1__scale_text')
        if slider:
            print('有滑块')
            # 移动滑块
            flag = await self.mouse_slider()
            # 判断滑块是否滑动成功
            if not flag:
                print('滑动滑块失败')
                return None
            time.sleep(random.random() + 0.5)
            # 点击登陆
            await self.page.click('#J_SubmitStatic')
        else:
            print('没滑块')
            # 按下回车
            await self.page.keyboard.press('Enter')
        # 等待
        await self.page.waitFor(20)
        # 等待导航, 等待跳转
        await self.page.waitForNavigation()
        # 判断是否登陆成功
        is_login = await self.page.querySelector('div .member')
        if is_login:
            print('登陆成功')
            cookie = await self.get_cookie()
            return cookie
        else:
            print('账号或密码错误, 登陆失败')
            return None


if __name__ == '__main__':
    username = '韩梅梅'
    pwd = '123456'
    login = LoginTaoBao()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(login.main(username, pwd))
    loop.run_until_complete(task)
    print(task.result())
    """
    目前只能在有头模式下运行
    """
