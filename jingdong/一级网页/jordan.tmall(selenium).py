from selenium import webdriver

d=webdriver.Chrome()

d.get('https://jordan.tmall.com/')

r=d.find_elements_by_class_name('c-price')

l=[]
for i in r:
    l.append(i.text)

d.close()