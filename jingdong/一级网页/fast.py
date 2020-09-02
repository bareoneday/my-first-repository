from selenium import webdriver
import time


dr = webdriver.ChromeOptions()
dr.add_argument('lang=zh_CN.UTF-8')
dr.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"')
br=webdriver.Chrome(chrome_options=dr)
br.get('https://jordan.tmall.com/category.htm?spm=a1z10.5-b-s.w4011-16722952378.1.64df4b73DyTXR6')

br.find_element_by_class_name('sn-login').click()