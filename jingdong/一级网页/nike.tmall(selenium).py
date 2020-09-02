from asyncio import sleep, get_event_loop
from pyppeteer import launch
from random import random
from re import compile, S

width, height = 1500, 800


async def init():
    # noinspection PyAttributeOutsideInit
    browser = await launch(headless=False,
                                args=['--disable-infobars', f'--window-size={width},{height}'])
    # noinspection PyAttributeOutsideInit
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/')
    await page.evaluate('()=>{Object.defineProperties(navigator,{webdriver:{get:()=>false}})}')


@staticmethod
async def login():
    await sleep(10)


async def turn():
    #page=await browser.newPage()
    await page.goto('https://nikekids.tmall.com/category.htm?spm=a1z10.5-b-s.w4011-18225450466.1.c5ac1075x4mxoF')


get_event_loop().run_until_complete(init())
get_event_loop().run_until_complete(login())
get_event_loop().run_until_complete(turn())